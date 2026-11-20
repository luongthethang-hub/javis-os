"""GitHub inside chat: what happens after a turn (github_work.after_turn).

    python tests/run.py github_work      (no network: local fake GitHub and bare repos; needs git and bash)

Phase G2: a turn that changed an attached repo runs the quality gate and posts the result into that chat; a turn that
changed nothing runs nothing; a failing check is reported as a failure; a chat without repos costs nothing.
"""
from _paths import ROOT, SERVER  # noqa: E402,F401
import asyncio
import os
import sys
import tempfile
from pathlib import Path

os.environ["JAVIS_STATE_DIR"] = tempfile.mkdtemp(prefix="javis-ghw-")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from _fake_github import FakeGitHub, GOOD_TOKEN  # noqa: E402

fake = FakeGitHub()
os.environ["JAVIS_GITHUB_API"] = fake.url

import github_repos  # noqa: E402
import github_work  # noqa: E402

_fails = []


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    if not cond:
        _fails.append(name)


posted = []


async def notify(sid, text, ok):
    posted.append((sid, text, ok))


github_work.configure(notify=notify)
BRAIN = tempfile.mkdtemp(prefix="brain-")
fake.add_repo("acme/app", files={
    "README.md": "app\n", "src/a.py": "a = 1\n",
    "check.py": "from pathlib import Path\nimport sys\nsys.exit(0 if 'a = 2' in Path('src/a.py').read_text() else 1)\n",
})
github_repos.connect(GOOD_TOKEN)
view = github_repos.attach("chat", BRAIN, BRAIN, ["acme/app"])
wt = Path(view["repos"][0]["worktree"])
check_command = "python check.py"
github_repos.set_checks(BRAIN, "acme/app", [{"run": check_command}])

run = lambda: asyncio.run(github_work.after_turn("chat", BRAIN))  # noqa: E731

check("a turn that changed nothing runs no gate", run() == [] and posted == [])
(wt / "src/a.py").write_text("a = 3\n", encoding="utf-8")
reps = run()
check("a changed repo is gated after the turn", len(reps) == 1 and reps[0]["full_name"] == "acme/app")
check("criterion 5: the failing check is reported as a failure", reps[0]["ok"] is False and posted[-1][2] is False)
check("the chat message names the repo and the failing command",
      posted[-1][0] == "chat" and "acme/app" in posted[-1][1] and check_command[:120] in posted[-1][1])
n = len(posted)
check("the same state is not gated twice", run() == [] and len(posted) == n)
# A restart forgets which states were gated, so the same red state is gated again. Its fix was already asked for,
# so no new turn starts: the row must not stay "running" (the chat icon pulsed orange forever, owner 2026-11-06).
github_work._last_gate.clear()
run()
check("a re-gated red state whose fix was already asked for is not left running",
      github_work.st().get("chat", "acme/app")["exec"] == "stuck")
(wt / "src/a.py").write_text("a = 2\n", encoding="utf-8")
reps = run()
check("after the fix the gate passes", reps and reps[0]["ok"] is True and posted[-1][2] is True)
check("a chat without repos does nothing", asyncio.run(github_work.after_turn("other-chat", BRAIN)) == [])
check("saved checks are used instead of suggestions", github_repos.get_checks(BRAIN, "acme/app")["custom"] is True)
github_repos.set_checks(BRAIN, "acme/app", None)
check("reset goes back to the suggested checks", github_repos.get_checks(BRAIN, "acme/app")["custom"] is False)
block = github_repos.prompt_block("chat", BRAIN)
check("the prompt asks for a reproducing test and forbids skipping tests", "TÁI HIỆN" in block and "KHÔNG bỏ qua" in block)
(wt / "AGENTS.md").write_text("Always run make lint.\n", encoding="utf-8")
block = github_repos.prompt_block("chat", BRAIN)
check("spec 7.1: the repo's AGENTS.md reaches the prompt of every engine", "Always run make lint." in block)

# ---- the gate diffs against the base of the remote this branch actually pushes to (owner 2026-11-20) ----
# A chat may read from one remote and push to another (a fork stays `origin`, the owner's repo carries the work).
# Grading against `origin/<base>` there compared the branch with an unrelated, much older tree, so the gate reported a
# multi-million-line diff plus "secrets" inside files the chat never touched.
import subprocess  # noqa: E402


def _git_(args, cwd):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, check=True)


def _bare(d, commit, files):
    Path(d).mkdir(parents=True, exist_ok=True)
    _git_(["init", "-q", "-b", "main"], d)
    _git_(["config", "user.email", "t@t"], d)
    _git_(["config", "user.name", "T"], d)
    for name, text in files.items():
        p = Path(d, name)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    _git_(["add", "-A"], d)
    _git_(["commit", "-qm", commit], d)
    return d


push_side = _bare(tempfile.mkdtemp(prefix="push-side-"), "base", {"src/a.py": "a = 0\n", "README.md": "app\n"})
# The other remote: an unrelated tree, exactly what made the old base report a huge diff and phantom secrets.
old_side = _bare(tempfile.mkdtemp(prefix="old-side-"), "old",
                 {"README.md": "old\n" * 200, "key.txt": 'T = "sk-' + "a" * 24 + '"\n',
                  "tests/t_x.py": "def test_old():\n    assert True\n"})
work = tempfile.mkdtemp(prefix="push-wt-")
_git_(["init", "-q", "-b", "main", work], work)
_git_(["config", "user.email", "t@t"], work)
_git_(["config", "user.name", "T"], work)
_git_(["remote", "add", "owner", str(push_side)], work)
_git_(["remote", "add", "origin", old_side], work)
_git_(["fetch", "-q", "owner"], work)
_git_(["fetch", "-q", "origin"], work)
_git_(["checkout", "-q", "-b", "fix/one", "owner/main"], work)
Path(work, "src").mkdir(parents=True, exist_ok=True)
Path(work, "src/a.py").write_text("x = 1\n", encoding="utf-8")
_git_(["add", "-A"], work)
_git_(["commit", "-qm", "one"], work)
_git_(["config", "branch.fix/one.remote", "owner"], work)
_git_(["config", "branch.fix/one.merge", "refs/heads/main"], work)

fake_repo = {"worktree": work, "full_name": "acme/app", "default_branch": "main"}
check("the gate uses the remote this branch pushes to, not a hard-coded origin",
      github_work._base(fake_repo) == "owner/main")
rep2 = github_work.github_gate.run_gate(work, github_work._base(fake_repo), [])
check("a branch pushed to another remote is graded against that remote's base", rep2["diff_lines"] < 20)
check("no phantom secret from a tree this chat never touched", not rep2["secrets"])
check("no phantom merge block from the other remote's files", not rep2["merge_block"])

fake.close()
print()
if _fails:
    print(f"FAIL {len(_fails)} test: " + ", ".join(_fails))
    sys.exit(1)
print("TẤT CẢ PASS")
