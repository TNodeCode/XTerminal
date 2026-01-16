# MultiClientSSHTerminal

Class: `MultiClientSSHTerminal`

Purpose: Run the same command across multiple `SSHTerminal` instances (multiple `paramiko.SSHClient`s) and collect results.

Constructor parameters

- `ssh_clients`: list of `paramiko.SSHClient` instances

Key methods

- `run(cmd: str)` — executes `cmd` on each configured SSH client; returns a mapping `{client_name: (stdout, stderr, exit_code)}` and records history per client.
