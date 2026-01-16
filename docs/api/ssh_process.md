# SSHProcess

Class: `SSHProcess` (subclass of `Process`)

Purpose: Run a command on a remote host using an existing `paramiko.SSHClient` or by creating one from connection parameters.

Constructor parameters

- `cmd`: command as string or list
- `ssh_client`: an existing `paramiko.SSHClient` instance (optional)
- `hostname`, `port`, `username`, `password`, `missing_host_key_policy`
- other `Process` options like `print_stdout`, `encoding`, `name`, `timeout`

Key methods / behavior

- `get_ssh_client(...)` — convenience static method to create and connect an `SSHClient`.
- `run(stop_on_error: bool = True)` — runs command on remote host using `ssh_client.exec_command`, streams stdout/stderr, and returns `(stdout_lines, stderr_lines, exit_code)`.

Notes

`SSHProcess` overrides the reading of stdout/stderr to iterate the remote channels. The command is executed as `cd {cwd} && {cmd}` so the `cwd` argument is used to set the remote working directory.
