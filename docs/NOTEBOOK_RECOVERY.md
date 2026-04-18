# Notebook recovery playbook

Use this when a `.ipynb` won’t open, shows conflict markers, or looks wrong after a merge.

## 1. Stop

- Don’t keep committing on top of a notebook you don’t trust.
- Check whether the problem is **only local** or already on the shared branch (e.g. `main`).

## 2. Triage

| Symptom | Likely cause |
|---------|----------------|
| File won’t open; `validate_notebooks` or JSON parse fails | Corrupt file, bad merge, truncated save |
| `<<<<<<<`, `=======`, `>>>>>>>` in the file | Unfinished or badly resolved Git merge |
| Opens but cells duplicated or out of order | Bad merge; resolve carefully |

## 3. Recover

**Not pushed yet (only your branch / local commits)**  
- Reset to the last known good commit (if you can discard intermediate work), or  
- Restore just the file:  
  `git checkout <good_commit> -- path/to/notebook.ipynb`

**Already pushed or others may have pulled**  
- Prefer **revert** or a **small fix PR** over rewriting shared history unless the whole team agrees.  
- Tell the group: “Don’t base new work on revision X until we fix the notebook.”

**Merge conflict in the notebook**  
- Prefer **one person** resolving it in VS Code (or re-apply one side’s changes manually).  
- After fixing: save, run `python scripts/validate_notebooks.py path/to/notebook.ipynb`, then commit.

## 4. Validate and notify

- Run `pre-commit run --all-files` or `python scripts/validate_notebooks.py` on affected notebooks.
- Message the team when `main` (or your shared branch) is safe to pull again.

## 5. If you must bypass hooks temporarily

- `git commit --no-verify` skips **pre-commit**; it does **not** disable **Git filters** for `nbstripout`.  
- Still avoid committing broken JSON; fix or restore the file first.
