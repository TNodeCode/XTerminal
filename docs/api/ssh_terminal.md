# SSHTerminal

Class: `SSHTerminal`

Purpose: Thin convenience wrapper around `SSHProcess` that keeps a `history` of executed remote commands and applies terminal defaults.

Constructor parameters

- `ssh_client`, `print_stdout`, `print_stderr`, `shell`, `cwd`, `env`, `encoding`, `use_os_env`, `name`, `timeout`

Key methods

- `run(cmd: str, cwd=None)` — creates an `SSHProcess` with the terminal's `ssh_client` and runs the command (prepended with `cd {cwd}`), appending the result to `history`.
