# Terminal

Class: `Terminal`

Purpose: Simple wrapper around `Process` that keeps a `history` of executed commands and applies default options.

Constructor parameters

- `print_stdout`, `print_stderr`, `shell`, `cwd`, `env`, `encoding`, `use_os_env`, `name`, `timeout`, `stop_on_error`

Key methods

- `run(cmd: str, cwd=None)` — runs `cmd` via a `Process` instance configured from the terminal defaults. Appends the result to `history` and returns the `(stdout, stderr, exit_code)` tuple.
