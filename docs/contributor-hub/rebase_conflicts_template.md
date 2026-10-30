# Rebase Conflicts on Shared Files

Several pull requests in this project often touch the same tail of a
file: `__init__.py`, `mkdocs.yml`, `MODULES.md`, or the README badge
table. After `main` moves, a rebase can stop on those files. This page
is the copy-paste path through that stop.

## Copy this checklist

```text
[ ] git fetch origin
[ ] git rebase origin/main
[ ] Open each conflicted file.
[ ] Keep the code that already landed on main.
[ ] Keep your addition too. Do not drop either side.
[ ] git add the resolved files
[ ] git rebase --continue
[ ] Run pytest on the module you changed.
[ ] git push --force-with-lease
```

If you are on a fork, `origin` may be your fork. Fetch and rebase from
the upstream remote that points at `sara-czasak/py-simple-wrap` instead.

## What a conflict looks like

Git wraps both versions in markers:

```text
<<<<<<< HEAD
    hash_file,
=======
    your_helper,
>>>>>>> your-commit
```

`HEAD` during a rebase is **current `main`**. The other side is **your
commit**. The resolved block should include both names, in the same
style as the rest of the list:

```python
from .easy_hash import (
    hash_file,
    your_helper,
)
```

The same rule applies to:

- a new line in `mkdocs.yml` under `Project-Based Tutorials` or
  `Contributor Hub`
- a new row in `MODULES.md`
- a new badge cell in the README table

If `main` grew an extra empty table row, keep that row. Sara has asked
for that before when the README table conflicted.

## After the markers are gone

```bash
git add py_simple_package/src/py_simple/__init__.py
git rebase --continue
```

Repeat for each stop. Then:

```bash
pytest tests/test_<module>.py
git push --force-with-lease
```

`--force-with-lease` updates the already-pushed branch after a rebase.
Plain `git push` will be rejected because the history changed.

## What not to do

- Do not delete `main`'s new helper to make your rebase "simpler."
- Do not start a second copy of the `from .easy_<module> import (`
  block. Edit the existing one.
- Do not rebase `main` itself.

The [Pull Request Workflow Guide](pr_workflow_template.md) covers the
rest of opening and updating a pull request.
