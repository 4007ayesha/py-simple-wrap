# Keeping Tests Isolated

A test should check your helper without changing the files or settings that
the next test depends on. Start with a directory made for that test, and let
pytest restore changes to environment variables and the working directory.

## Copy a working example first

Follow the environment setup in [CONTRIBUTING.md](../how-to/contributing.md),
then save this practice file as `tests/test_isolation_demo.py`:

```python
import os
from pathlib import Path

import pytest

from py_simple_package.src.py_simple.easy_config import (
    EasyConfigError,
    create_env_file,
    read_env_file,
)


def test_env_file_uses_a_test_directory(tmp_path):
    env_file = tmp_path / "settings" / ".env"

    create_env_file({"MODE": "practice"}, file_path=str(env_file))

    assert env_file.read_text(encoding="utf-8") == "MODE=practice\n"
    assert read_env_file(str(env_file)) == {"MODE": "practice"}


def test_default_path_and_environment_are_restored(tmp_path, monkeypatch):
    original_directory = Path.cwd()
    original_mode = os.environ.get("PY_SIMPLE_TEST_MODE")

    with monkeypatch.context() as patch:
        patch.chdir(tmp_path)
        patch.setenv("PY_SIMPLE_TEST_MODE", "practice")

        create_env_file({"MODE": os.environ["PY_SIMPLE_TEST_MODE"]})

        assert Path.cwd() == tmp_path
        assert read_env_file() == {"MODE": "practice"}

    assert Path.cwd() == original_directory
    assert os.environ.get("PY_SIMPLE_TEST_MODE") == original_mode


def test_missing_file_does_not_create_it(tmp_path):
    missing_file = tmp_path / "missing.env"

    with pytest.raises(EasyConfigError):
        read_env_file(str(missing_file))

    assert not missing_file.exists()
```

From the repository root, run:

=== "Using uv"
    ```bash
    uv run pytest tests/test_isolation_demo.py -q
    ```

=== "Using pip"
    ```bash
    python -m pytest tests/test_isolation_demo.py -q
    ```

You should see **3 passed**. Remove the practice file afterward. For a real
contribution, add your cases to the matching module's test file instead of
submitting these same examples again.

The helpers here already exist in `easy_config`. `create_env_file` writes a
file, and `read_env_file` returns a dictionary; neither loads values into
`os.environ`. The second test supplies a made-up environment value itself.

## Fill in the parts for your helper

| Part | Replace it with |
| --- | --- |
| `easy_config` and its imports | The module and helper you are testing. Read its signature and implementation first. |
| `tmp_path / "settings" / ".env"` | A path inside `tmp_path` for every input and output file your helper uses. |
| `"MODE": "practice"` | Small, made-up input and the exact result your helper promises. |
| `patch.chdir(tmp_path)` | Keep this when testing relative paths or a default filename. Prefer an explicit test path when possible. |
| `patch.setenv(...)` | The specific environment variables your test or helper reads or changes. |
| `EasyConfigError` | The error your helper actually raises for this input. |

Keep a successful case and an error case. Check the result or file contents,
not just that the call finished. A helper with several input/output paths
needs all of them pointed at the test directory.

## Why the next test stays independent

### Files belong inside `tmp_path`

`tmp_path` gives each test invocation its own `pathlib.Path` directory. It
keeps a practice `.env` away from your real configuration and gives each
parametrized case its own starting point. Create the test's inputs there,
too; do not copy your real `.env` or read files from your home directory.

Files are **not deleted when the test function returns**. Pytest normally
retains temporary directories from recent runs for debugging. Treat their
contents as potentially retained, and use synthetic data only. Pytest's
`--basetemp` option clears the directory you give it before a run, so never
point it at your project or another directory you need to keep.

### Restore environment variables and the working directory

`monkeypatch` is a pytest fixture, just like `tmp_path`. Its `setenv`,
`delenv` and `chdir` methods record the previous state and restore it during
teardown, including when an assertion fails. To simulate a missing variable,
use `monkeypatch.delenv("PY_SIMPLE_TEST_MODE", raising=False)`.

The example uses `monkeypatch.context()` so restoration happens at the end
of the `with` block. That lets the assertions afterward check it in the
same test, without depending on which test runs next. Calling
`monkeypatch.chdir(...)` or `monkeypatch.setenv(...)` directly instead keeps
the change until that fixture's teardown.

The original working directory and the presence or value of the example
variable are preserved. Do not print the original value: it might come
from the person running the test.

### Register changes made by the code under test

Monkeypatch only undoes changes it manages. It does not automatically watch
every assignment to `os.environ` or every call to `os.chdir`.

If a helper directly assigns an environment variable, first register that
exact key with `patch.setenv(key, "test value")` inside the context, then
call the helper there. Teardown restores the value or absence recorded
before `setenv`, even if the helper overwrites or deletes the key. Register
every key the helper can change, not only the ones you assert on. Likewise,
call `patch.chdir(tmp_path)` before a helper that changes the working
directory, and keep any destination it uses inside the test area.

Do not clear the whole environment to isolate one key. If the helper's
contract requires a different cleanup step, such as closing a file or
database connection, use its context manager or `try`/`finally`. Restoring
process state does not close resources or delete files for you.

## Before opening your PR

- Keep all example data synthetic, including environment values and files.
- Run the affected tests alone and with the rest of the suite, as described
  in [CONTRIBUTING.md](../how-to/contributing.md). Tests should not need a
  particular order or a leftover file from an earlier run.
- Run the repository's [pinned hooks](pre_commit_template.md).

For basic assertions and parametrized errors, see the
[Testing Tutorial](tests_template.md). For fake HTTP responses, use the
[Network Test Template](network_tests_template.md); a temporary directory
does not prevent a real network request.
