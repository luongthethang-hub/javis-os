from concurrent.futures import ThreadPoolExecutor
import argparse
import json
import subprocess

from pilot import CASES, ROOT, cli


RULES = ROOT / "repo" / "skills" / "egm-lite" / "SKILL.md"
SPEC = CASES["retry"]


def run(missing, inline):
    label = "missing" if missing else "ready"
    workspace = ROOT / f"protocol-{label}"
    workspace.mkdir(exist_ok=True)
    subprocess.run(["git", "init", "--quiet", str(workspace)], check=True)
    card = workspace / "egm_lite_checklist.md"
    card.write_text(
        SPEC["card"] + "\n\nBefore/after capture required for the single checklist "
        "target SendGuard.mqh: BEFORE.txt and AFTER.txt in this fixture.\n",
        encoding="utf-8",
    )
    (workspace / "BEFORE.txt").write_text(SPEC["old"], encoding="utf-8")
    if not missing:
        (workspace / "AFTER.txt").write_text(SPEC["new"], encoding="utf-8")
    skill = RULES.read_text(encoding="utf-8")
    section = skill.split("## 4. ADVERSARIAL DIFF REVIEW", 1)[1].split(
        "## 5. POST-REVIEW RESOLUTION GATE", 1
    )[0]
    prompt = (
        "Run the post-implementation EGM Lite diff review described in the supplied "
        "reference section against the synthetic files in your current directory. "
        "The fixture uses before/after text snapshots as its baseline, indicated in "
        "egm_lite_checklist.md. No edits, network, git-based discovery or git writes. "
        "Read only the checklist and exact snapshot paths. For a complete review packet, "
        "use one native child with fork_turns none or fork_context false. Report either "
        "a completed review or INCOMPLETE with the exact missing path. This is a "
        "standalone protocol probe without plugin installation.\n\n"
        "EGM Lite reference section\n" + section
    )
    if inline:
        files = {}
        for filename in ("egm_lite_checklist.md", "BEFORE.txt", "AFTER.txt"):
            try:
                files[filename] = (workspace / filename).read_text(encoding="utf-8")
            except FileNotFoundError:
                files[filename] = None
        prompt = (
            "Run EGM Lite section 4 on the sanitized artifacts actually read by the "
            "parent harness below. A null value means the filesystem read failed "
            "with FileNotFoundError. Do not use shell or other I/O. If any artifact "
            "required by the checklist is missing, stop before delegation and return "
            "INCOMPLETE with the exact missing path. Otherwise launch exactly one "
            "native reviewer with fork_turns none or fork_context false, pass the "
            "complete review input only, and wait for its actual result. Do not claim "
            "to have run compiler or tests.\n\n"
            "Artifact reads:\n" + json.dumps(files, indent=2)
            + "\n\nEGM Lite reference section\n" + section
        )
    suffix = "-inline" if inline else ""
    data = cli(workspace, prompt, ROOT / f"protocol-{label}{suffix}", native=True)
    print(label, data["returncode"], data["message"], flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inline", action="store_true")
    args = parser.parse_args()
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run, missing, args.inline) for missing in (False, True)]
        for future in futures:
            future.result()
