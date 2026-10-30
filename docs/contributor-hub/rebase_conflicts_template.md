# Rebase Conflicts on Shared Files

Several pull requests in this project often touch the same tail of a
file: `__init__.py`, `mkdocs.yml`, `MODULES.md`, or the README badge
table. After `main` moves, a rebase can stop on those files. This page
is the copy-paste path through that stop.

Most people work from a **fork**. In that setup, `origin` is your copy
and `upstream` is `sara-czasak/py-simple-wrap`. The commands below use
those names, the same way as the
[Pull Request Workflow Guide](pr_workflow_template.md).

## Copy this checklist

Add the upstream remote once, if you do not have it yet:

```bash
git remote add upstream https://github.com/sara-czasak/py-simple-wrap.git
```

Then:

```text
[ ] git fetch upstream
[ ] git rebase upstream/main
[ ] Open each conflicted file.
[ ] Keep the code that already landed on main.
[ ] Keep your addition too. Do not drop either side.
[ ] Delete every leftover conflict marker: <<<<<<<, =======, and >>>>>>>.
[ ] Check the list for duplicate names, duplicate nav lines, or a
    second copy of the same import block.
[ ] git add the resolved files
[ ] git rebase --continue
[ ] Run pytest on the module you changed.
[ ] git push --force-with-lease origin HEAD
```

If `git remote add` says the remote already exists, skip that line and
fetch `upstream` as usual. Do not rebase onto `origin/main` unless
`origin` is the `sara-czasak/py-simple-wrap` repo itself.

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

None of the three marker lines should remain. A leftover `<<<<<<< HEAD`
will break the file, and a name listed twice (two `hash_file,` lines, or
the same tutorial listed twice in `mkdocs.yml`) is also wrong.

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
git push --force-with-lease origin HEAD
```

`--force-with-lease` updates the already-pushed **fork** branch after a
rebase. Plain `git push` will be rejected because the history changed.

## What not to do

- Do not delete `main`'s new helper to make your rebase "simpler."
- Do not start a second copy of the `from .easy_<module> import (`
  block. Edit the existing one.
- Do not leave conflict markers in the file, even in a comment.
- Do not rebase `main` itself.

The [Pull Request Workflow Guide](pr_workflow_template.md) covers the
rest of opening and updating a pull request.
