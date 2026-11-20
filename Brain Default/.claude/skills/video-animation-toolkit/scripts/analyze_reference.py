"""Run the pinned local rea-video pilot on a reference MP4/MOV inside this brain."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from uuid import uuid4


ARTIFACTS = ('VIDEO.md', 'breakdown.json', 'storyboard.jpg', 'report.md', 'report.html')
# The pinned CLI can try to fetch YuNet even with --no-vlm. Block Python network
# access before importing the CLI; upstream falls back to local Haar or skips faces.
LOCAL_ENTRY = '''
import sys

def deny_network(event, _args):
    if event in {"socket.connect", "socket.getaddrinfo", "socket.gethostbyname"}:
        raise OSError("network disabled in the Javis reference video pilot")

sys.addaudithook(deny_network)
from rea_video.cli import main
raise SystemExit(main())
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', help='MP4/MOV path relative to the brain, or absolute inside it')
    args = parser.parse_args()
    brain = Path(__file__).resolve().parents[3]
    output = None
    try:
        source = (brain / args.video).resolve(strict=True)
        if not source.is_relative_to(brain) or not source.is_file() or source.suffix.lower() not in {'.mp4', '.mov'}:
            raise ValueError('Input must be an MP4/MOV file inside this brain; URLs are not accepted.')
        local_data = os.environ.get('LOCALAPPDATA')
        if not local_data:
            raise ValueError('The Windows pilot needs LOCALAPPDATA.')
        python = Path(local_data) / 'Javis' / 'rea-video-pilot' / '131d152' / 'venv' / 'Scripts' / 'python.exe'
        if not python.is_file():
            raise ValueError(f'Pinned pilot interpreter is missing: {python}')
        for tool in ('ffmpeg.exe', 'ffprobe.exe'):
            if not shutil.which(tool):
                raise ValueError(f'{tool} is missing from PATH.')
        root = (brain / 'attachments' / 'video-reference-pilot').resolve()
        if not root.is_relative_to(brain):
            raise ValueError('Output directory resolves outside this brain.')
        root.mkdir(parents=True, exist_ok=True)
        output = root / uuid4().hex[:12]
        output.mkdir()
        with tempfile.TemporaryDirectory(prefix='rea-video-pilot-') as scratch:
            # Keep the CLI away from existing prefs, .env overrides and model/API keys.
            env = {k: v for k, v in os.environ.items() if k.upper() in {
                'SYSTEMROOT', 'SYSTEMDRIVE', 'WINDIR', 'PATH', 'PATHEXT', 'TEMP', 'TMP',
            }}
            env['REA_VIDEO_HOME'] = scratch
            env['USERPROFILE'] = scratch  # Path.home() is evaluated by upstream even with REA_VIDEO_HOME set.
            empty_env = Path(scratch) / 'empty.env'
            empty_env.touch()
            command = [str(python), '-I', '-X', 'utf8', '-c', LOCAL_ENTRY, '--env-file', str(empty_env),
                       'decompose', str(source), '-o', str(output), '--lang', 'en', '--workers', '1',
                       '--no-vlm', '--no-ocr', '--no-asr', '--no-stems', '--no-speakers',
                       '--no-survey', '--no-moments', '--no-packaging']
            with (output / 'cli.log').open('wb') as log:
                subprocess.run(command, cwd=scratch, env=env, stdout=log, stderr=subprocess.STDOUT,
                               timeout=300, check=True)
        for name in ARTIFACTS:
            artifact = output / name
            if not artifact.is_file() or not artifact.stat().st_size:
                raise ValueError(f'Expected output missing or empty: {name}')
        breakdown = json.loads((output / 'breakdown.json').read_text(encoding='utf-8'))
        summary = breakdown['summary']
        if not isinstance(summary.get('shots'), int) or summary['shots'] < 1:
            raise ValueError('No valid shot count in breakdown.json.')
        vlm = breakdown['analysis']['vlm']
        if vlm.get('status') != 'off' or vlm.get('used') is not False or vlm.get('requested') is not False:
            raise ValueError('Expected a local-only result with VLM disabled.')
        print(json.dumps({'shots': summary['shots'], 'vlm': False,
                          'artifacts': {name: (output / name).relative_to(brain).as_posix()
                                        for name in ARTIFACTS}}, ensure_ascii=True))
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        parser.exit(1, f'Pilot failed: {exc}\n' +
                    (f'Run directory (may contain partial output): {output}\n' if output else ''))


if __name__ == '__main__':
    main()
