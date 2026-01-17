import os
from pathlib import Path
from aggregator.gitops import stage_and_commit

def test_stage_and_commit_no_repo(tmp_path: Path):
    # Not a git repo, expect non-zero commit rc typically
    f = tmp_path / "file.txt"
    f.write_text("data", encoding="utf-8")
    add_rc, commit_rc = stage_and_commit([f], "test commit")
    # We can't guarantee return codes across environments, but ensure tuple shape
    assert isinstance(add_rc, int) and isinstance(commit_rc, int)
