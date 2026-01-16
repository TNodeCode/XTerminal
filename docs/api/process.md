# Process

Class: `Process`

Purpose: Run a local process, capture stdout/stderr line-by-line, and expose lifecycle events.

Constructor parameters

- `cmd`: command as string or list
- `print_stdout`, `print_stderr`: booleans to print output
- `shell`, `cwd`, `env`, `encoding`, `use_os_env`, `name`, `timeout`

Key methods

- `get_uuid()` — returns the process UUID.
- `run(stop_on_error: bool = True)` — execute the command; returns `(stdout_lines, stderr_lines, exit_code)`.
- `write(value: str)` — write to stdin.
- `get_last_line_from_stdout()` / `get_last_line_from_stderr()` — last received line.
- `get_output()` / `get_error()` — lists of stdout/stderr lines collected.
- `get_exit_code()`, `get_exception()`, `is_finished()`, `get_start()`, `get_end()` — execution metadata.
- Event hooks: subscribe to `on_stdout_readline`, `on_stderr_readline`, `on_process_start`, `on_process_finished` using `register_stdout_readline_handler` and `register_stderr_readline_handler`.

Notes

The class uses threads to read stdout and stderr in parallel. If `stop_on_error` is true and the process returns a non-zero exit code, an exception is raised.
