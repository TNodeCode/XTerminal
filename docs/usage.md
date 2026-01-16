# Usage

Below are quick examples demonstrating common usage patterns.

## Process (local)

```python
from xterminal import Process

p = Process(cmd='echo hello')
out, err, code = p.run()
```

## Terminal (stateful wrapper)

```python
from xterminal import Terminal

t = Terminal()
t.run('ls -la')
```

## SSHProcess (single SSH command)

```python
from paramiko import SSHClient
from xterminal import SSHProcess

client = SSHClient()
# configure client (set_missing_host_key_policy, connect...)
p = SSHProcess(cmd='uname -a', ssh_client=client)
p.run()
```

## SSHTerminal (convenience wrapper around SSHProcess)

```python
from xterminal import SSHTerminal

terminal = SSHTerminal(ssh_client=client)
terminal.run('uptime')
```

## MultiClientSSHTerminal (run on multiple clients)

```python
from xterminal import MultiClientSSHTerminal

mc = MultiClientSSHTerminal([client1, client2])
mc.run('df -h')
```

## BackgroundProcesses (run Process in background thread)

```python
from xterminal import BackgroundProcesses, Process

p = Process(cmd='sleep 5 && echo done')
bg = BackgroundProcesses(p)
bg.run()
```
