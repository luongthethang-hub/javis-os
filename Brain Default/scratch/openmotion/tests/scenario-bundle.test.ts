import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import { designProjectsFor } from '../design-projects.ts';
import { execute, pluginRoot } from '../hyperframes.ts';
import { verificationBinaries } from '../scripts/verify-export.ts';
import type { Service } from '../server.ts';
import { readProjectZip } from '../shared/project-zip.ts';
import { draftSocialPosts } from '../shared/scenario-content.ts';
import { findScenario } from '../shared/scenarios.ts';
import { fixture } from './fixtures.ts';
import { transport } from './http.ts';

async function makePng(dir: string, name = 'hero.png'): Promise<Buffer> {
  const file = path.join(dir, name);
  const result = await execute(
    verificationBinaries().ffmpeg,
    ['-v', 'error', '-f', 'lavfi', '-i', 'color=c=teal:s=48x36', '-frames:v', '1', '-y', file],
    dir,
    20_000,
  );
  assert.equal(result.code, 0, result.stderr);
  return readFile(file);
}

async function callScenario(api: ReturnType<typeof transport>, scenarioArgs: Record<string, unknown>) {
  const res = await api('/motion-api/phase1/call', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'openmotion_assets_use',
      arguments: { action: 'scenario', scenario: scenarioArgs },
    }),
  });
  const body = await res.json();
  assert.equal(res.status, 200, JSON.stringify(body));
  return body;
}

test('scenario bundle export creates valid ZIP with embedded web assets, idempotent receipts, step filtering and HTTP download', () =>
  fixture(async store => {
    const api = transport(store, { runtimeRoot: pluginRoot } as Service);

    // Create design-full-chain run with brief, landing page, uploaded image, embedded image and social posts
    let run = (await callScenario(api, {
      command: 'create',
      requestId: 'bundle-create',
      scenarioId: 'design-full-chain',
      title: 'Nova Launch',
    })).run;

    run = (await callScenario(api, {
      command: 'update_brief',
      runId: run.id,
      expectedRevision: run.revision,
      requestId: 'bundle-brief',
      brief: {
        idea: 'One workspace for every creative launch',
        productName: 'Nova Launch',
        valueProps: ['Offline starter pages', 'Shared asset pool'],
        cta: 'Try Nova',
      },
    })).run;

    const pngBytes = await makePng(store.directory, 'nova-hero.png');
    const uploadRes = await api('/motion-api/assets/upload?requestId=bundle-upload-hero', {
      method: 'POST',
      headers: { 'Content-Type': 'application/octet-stream', 'X-File-Name': encodeURIComponent('nova-hero.png') },
      body: new Blob([new Uint8Array(pngBytes)]),
    });
    assert.equal(uploadRes.status, 200);
    const asset = (await uploadRes.json()).asset;

    const poolAdd = await callScenario(api, {
      command: 'add_pool',
      runId: run.id,
      expectedRevision: run.revision,
      requestId: 'bundle-add-pool',
      items: [{
        ref: { type: 'asset', assetId: asset.id, versionId: asset.currentVersionId },
        label: 'Nova Hero',
        source: 'upload',
        stepId: 'page-images',
      }],
    });
    run = poolAdd.run;
    const heroPoolId = poolAdd.poolItemIds[0];

    // Pin the image and create an iteration on page-images
    run = (await callScenario(api, {
      command: 'add_iteration',
      runId: run.id,
      expectedRevision: run.revision,
      requestId: 'bundle-img-iter',
      stepId: 'page-images',
      iteration: { source: 'upload', outputs: [{ type: 'pool', poolItemId: heroPoolId }] },
    })).run;

    const createdPage = await callScenario(api, {
      command: 'create_page',
      runId: run.id,
      expectedRevision: run.revision,
      requestId: 'bundle-create-page',
      stepId: 'landing-page',
      mode: 'starter',
    });
    run = createdPage.run;
    const designProjectId = createdPage.project.id;
    const designRevision = (await designProjectsFor(store.directory).get(designProjectId)).revision;

    const embedded = await callScenario(api, {
      command: 'embed_image',
      runId: run.id,
      expectedRevision: run.revision,
      requestId: 'bundle-embed-hero',
      stepId: 'embed-images',
      designProjectId,
      expectedDesignRevision: designRevision,
      poolItemId: heroPoolId,
      target: { kind: 'slot', slot: 'hero' },
      alt: 'Nova Hero Visual',
    });
    run = embedded.run;

    const posts = draftSocialPosts(findScenario('design-full-chain')!, run.brief, ['x', 'instagram'], { variant: 0 });
    run = (await callScenario(api, {
      command: 'add_iteration',
      runId: run.id,
      expectedRevision: run.revision,
      requestId: 'bundle-social',
      stepId: 'social',
      iteration: { source: 'local', outputs: [{ type: 'social', posts }] },
    })).run;

    // Also add an unattached uploaded pool asset (stepId: null, pinned: false)
    const extraPngBytes = await makePng(store.directory, 'unattached-logo.png');
    const extraUploadRes = await api('/motion-api/assets/upload?requestId=bundle-upload-logo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/octet-stream', 'X-File-Name': encodeURIComponent('unattached-logo.png') },
      body: new Blob([new Uint8Array(extraPngBytes)]),
    });
    assert.equal(extraUploadRes.status, 200);
    const extraAsset = (await extraUploadRes.json()).asset;
    run = (await callScenario(api, {
      command: 'add_pool',
      runId: run.id,
      expectedRevision: run.revision,
      requestId: 'bundle-add-unattached-pool',
      items: [{
        ref: { type: 'asset', assetId: extraAsset.id, versionId: extraAsset.currentVersionId },
        label: 'Brand Mark',
        source: 'upload',
        stepId: null,
      }],
    })).run;

    // Full export
    const exported = await callScenario(api, {
      command: 'export',
      runId: run.id,
      requestId: 'bundle-export-full',
      activeOnly: true,
      includeStandaloneHtml: true,
    });
    const receipt = exported.bundle;
    assert.ok(receipt.bundleId);
    assert.ok(receipt.filename.endsWith('.zip'));
    assert.equal(receipt.downloadUrl, `/motion-api/scenarios/bundles/${receipt.bundleId}/file`);

    // Same requestId returns same bundleId
    const replayed = await callScenario(api, {
      command: 'export',
      runId: run.id,
      requestId: 'bundle-export-full',
      activeOnly: true,
      includeStandaloneHtml: true,
    });
    assert.equal(replayed.bundle.bundleId, receipt.bundleId);

    // Inspect ZIP contents strictly via readProjectZip
    const diskBytes = await readFile(receipt.archivePath);
    const entries = readProjectZip(diskBytes);
    const keys = [...entries.keys()];
    const prefix = keys[0].split('/')[0] + '/';

    const manifestBuf = entries.get(`${prefix}manifest.json`);
    assert.ok(manifestBuf, 'manifest.json present');
    const manifest = JSON.parse(manifestBuf.toString('utf8'));
    assert.equal(manifest.schema, 'openmotion.scenario-bundle/1');
    assert.equal(manifest.run.revision, run.revision);
    assert.ok(manifest.steps.length >= 5);

    assert.ok(entries.has(`${prefix}README.md`), 'README.md present');
    assert.ok(entries.has(`${prefix}brief/brief.md`), 'brief/brief.md present');

    const landingHtmlBuf = entries.get(`${prefix}web/landing-page/index.html`);
    assert.ok(landingHtmlBuf, 'web/landing-page/index.html present');
    const landingHtml = landingHtmlBuf.toString('utf8');
    const imgMatch = /src="\.\/(assets\/[^"]+)"/.exec(landingHtml);
    assert.ok(imgMatch, 'HTML references embedded relative ./assets/* image');
    assert.ok(entries.has(`${prefix}web/landing-page/${imgMatch[1]}`), `Referenced image ${imgMatch[1]} exists in ZIP`);
    assert.ok(entries.has(`${prefix}web/landing-page.standalone.html`), 'Standalone HTML snapshot present');

    assert.ok(keys.some(k => k.startsWith(`${prefix}media/images/`) && k.endsWith('.png')), 'media/images/* present');
    assert.ok(
      keys.some(k => k.startsWith(`${prefix}media/images/brand-mark-`) && k.endsWith('.png')),
      `Unattached uploaded pool asset expected in full bundle, got: ${keys.join(', ')}`,
    );
    assert.ok(entries.has(`${prefix}social/posts.json`), 'social/posts.json present');
    assert.ok(entries.has(`${prefix}social/posts.md`), 'social/posts.md present');

    // Passing all stepIds is treated as a full bundle (includes README.md + unattached pool files)
    const allContentStepIds = findScenario('design-full-chain')!.steps.map(step => step.id);
    const allStepsExport = await callScenario(api, {
      command: 'export',
      runId: run.id,
      requestId: 'bundle-export-all-content-steps',
      stepIds: allContentStepIds,
      activeOnly: true,
    });
    const allStepsEntries = readProjectZip(await readFile(allStepsExport.bundle.archivePath));
    const allStepsKeys = [...allStepsEntries.keys()];
    const allStepsPrefix = allStepsKeys[0].split('/')[0] + '/';
    assert.ok(allStepsEntries.has(`${allStepsPrefix}README.md`), 'README.md present when all content steps are selected');
    assert.ok(
      allStepsKeys.some(k => k.startsWith(`${allStepsPrefix}media/images/brand-mark-`) && k.endsWith('.png')),
      'Unattached pool asset present when all content steps are selected',
    );

    // Focused export: single poolItemId exports only manifest.json (with selection) + that asset
    const singlePoolExport = await callScenario(api, {
      command: 'export',
      runId: run.id,
      requestId: 'bundle-export-single-pool-item',
      poolItemIds: [heroPoolId],
    });
    const singleEntries = readProjectZip(await readFile(singlePoolExport.bundle.archivePath));
    const singleKeys = [...singleEntries.keys()];
    const singlePrefix = singleKeys[0].split('/')[0] + '/';
    const singleManifest = JSON.parse(singleEntries.get(`${singlePrefix}manifest.json`)!.toString('utf8'));
    assert.deepEqual(singleManifest.selection, { poolItemIds: [heroPoolId] });
    assert.equal(singleManifest.pool.length, 1);
    assert.equal(singleKeys.length, 2, `Expected manifest + 1 asset, got: ${singleKeys.join(', ')}`);
    assert.ok(singleKeys.some(k => k.startsWith(`${singlePrefix}media/images/nova-hero-`)));

    // Focused export: multi-select poolItemIds exports heterogeneous items (image + Design page)
    const pagePoolItem = run.pool.find((item: { kind: string }) => item.kind === 'page');
    assert.ok(pagePoolItem, 'Design page item present in run pool');
    const multiPoolExport = await callScenario(api, {
      command: 'export',
      runId: run.id,
      requestId: 'bundle-export-multi-pool-items',
      poolItemIds: [heroPoolId, pagePoolItem.id],
      includeStandaloneHtml: true,
    });
    const multiEntries = readProjectZip(await readFile(multiPoolExport.bundle.archivePath));
    const multiKeys = [...multiEntries.keys()];
    const multiPrefix = multiKeys[0].split('/')[0] + '/';
    assert.ok(!multiEntries.has(`${multiPrefix}README.md`), 'Focused pool export omits README.md');
    assert.ok(!multiKeys.some(k => k.startsWith(`${multiPrefix}brief/`)), 'Focused pool export omits brief/');
    assert.ok(!multiKeys.some(k => k.startsWith(`${multiPrefix}social/`)), 'Focused pool export omits social/');
    assert.ok(multiKeys.some(k => k.startsWith(`${multiPrefix}media/images/nova-hero-`)));
    assert.ok(multiKeys.some(k => k.startsWith(`${multiPrefix}web/`) && k.endsWith('/index.html')));

    // Unknown poolItemId rejects with POOL_ITEM_NOT_FOUND
    const badPoolRes = await api('/motion-api/phase1/call', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'openmotion_assets_use',
        arguments: {
          action: 'scenario',
          scenario: {
            command: 'export',
            runId: run.id,
            requestId: 'bundle-export-missing-pool',
            poolItemIds: ['eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee'],
          },
        },
      }),
    });
    assert.equal(badPoolRes.ok, false);
    const badPoolBody = await badPoolRes.json();
    assert.match(String(badPoolBody.error ?? ''), /POOL_ITEM_NOT_FOUND/);

    // Filtered export: stepIds: ['social'] contains only social outputs and manifest
    const socialOnly = await callScenario(api, {
      command: 'export',
      runId: run.id,
      requestId: 'bundle-export-social',
      stepIds: ['social'],
    });
    const socialEntries = readProjectZip(await readFile(socialOnly.bundle.archivePath));
    const socialKeys = [...socialEntries.keys()];
    const socialPrefix = socialKeys[0].split('/')[0] + '/';
    assert.ok(socialEntries.has(`${socialPrefix}manifest.json`));
    assert.ok(socialEntries.has(`${socialPrefix}social/posts.json`));
    assert.ok(socialEntries.has(`${socialPrefix}social/posts.md`));
    assert.ok(
      socialKeys.every(k => k === `${socialPrefix}manifest.json` || k.startsWith(`${socialPrefix}social/`)),
      `Only manifest and social outputs expected, got: ${socialKeys.join(', ')}`,
    );

    // HTTP download returns 200 with RFC 5987 filename* and exact sha256 bytes
    const downloadRes = await api(receipt.downloadUrl);
    assert.equal(downloadRes.status, 200);
    const disposition = downloadRes.headers.get('content-disposition') ?? '';
    assert.match(disposition, /filename\*=UTF-8''/);
    const downloadedBytes = Buffer.from(await downloadRes.arrayBuffer());
    const downloadedSha = createHash('sha256').update(downloadedBytes).digest('hex');
    assert.equal(downloadedSha, receipt.sha256);

    // Unknown bundle id returns 404
    const missingRes = await api('/motion-api/scenarios/bundles/dddddddd-dddd-4ddd-8ddd-dddddddddddd/file');
    assert.equal(missingRes.status, 404);
  }, false));
