## What does this PR do?

<!-- A sentence or two is plenty. If it fixes an issue, link it: Fixes #123 -->

## Type of change

<!-- Check what applies — this also roughly matches how the guild-crediting
     workflow sorts contributions, so it's worth getting right. -->

- [ ] New module (`easy_*.py`)
- [ ] New function(s) in an existing module
- [ ] Bug fix
- [ ] Tests
- [ ] Documentation (README, tutorial, docstrings)
- [ ] Infra / CI / tooling

## Before you submit

Nobody expects this to be perfect on the first try — see
[CONTRIBUTING.md](https://github.com/sara-czasak/py-simple-wrap/blob/main/CONTRIBUTING.md) if any of this is unclear, and
just say so in the PR if you're stuck on one of these. This checklist
exists so review comments are about the *idea*, not formatting nits.

- [ ] Every new/changed public function has a docstring in the
      [project's shape](https://sara-czasak.github.io/py-simple-wrap/docs/contributor-hub/docstring_template/) —
      Args/Returns (if applicable) + an Example block with both the
      "Py_simple Way" and "Traditional Way" tabs.
- [ ] Tests were added or updated for what changed.
- [ ] I ran the existing test suite locally and it passes.
- [ ] If this adds a new module: it has a module-level docstring
      (`"""easy_<name> is meant to simplify ..."""`), a tutorial page in
      `docs/tutorial/`, and an entry in `mkdocs.yml`'s nav.
- [ ] This passes the [Simple Philosophy](../CONTRIBUTING.md#the-simple-philosophy)
      check: *does this make a complex task easier for a beginner?*

## Anything else the reviewer should know?

<!-- Design decisions, things you're unsure about, questions — this is
     a good place to flag "I wasn't sure if X was the right call." -->
