# Process Execution Library

This module provides a nicer interface to the Python subprocess library.

## How to use this library

### Running processes

```python
from xterminal import Process

# Run a process and get stdout, stderr and exit code of the process
p = Process("ifconfig")
stdout, stderr, exit_code = p.run()

# Print stdout when executing process
p = Process("ifconfig", print_stdout=True)
stdout, stderr, exit_code = p.run()

# Use a shell (this is necessary if you want to execute shell scripts on Linux or Batch scripts on Windows)
p = Process("ifconfig", shell=True)
stdout, stderr, exit_code = p.run()
```

## Extract information from Process object

```python
p = Process("ifconfig")
p.run()

# Get UUID of the process object
print(p.uuid)
print(p.get_uuid())

# Get stdout as list of lines
print(p.out)
print(p.get_output())

# Get error (if there was any)
print(p.err)
print(p.get_error())

# Get the environment variables of the process
print(p._env)
print(p.get_process_env())

# Check if process is finished
print(p.is_finished())
print(p.finished)

# Get exit code
print(p.get_exit_code())
print(p.exit_code)

# Get start time of process execution
print(p.get_start())
print(p.start)

# Get time when process was finished
print(p.get_end())
print(p.end)
```

## Interact with stdout and stderr

```python
def log_stdout(p: Process):
    """
    This function is called everytime a line is read from stdout of the process
    :param p: Process object
    """
    print(f"[STDOUT] {p.get_last_line_from_stdout()}")

def log_stderr(p: Process):
    """
    This function is called everytime a line is read from stderr of the process
    :param p: Process object
    """
    print(f"[STDOUT] {p.get_last_line_from_stderr()}")

p = Process("ifconfig")
p.register_stdout_readline_handler(log_stdout)
p.register_stderr_readline_handler(log_stderr)
p.run()
```

### Even more interactivity: Write to stdin during process execution

```python
def handle_questions(p: Process):
    """
    This function is called everytime a line is read from stdout of the process
    :param p: Process object
    """
    if p.get_last_line_from_stdout() == "How old are you?":
        p.write("30")
    if p.get_last_line_from_stdout() == "Which country are you from?":
        p.write("Germany")

p = Process("my_programm")
p.register_stdout_readline_handler(handle_questions)
p.run()
```

## Running multiple commands via a terminal

```python
from xterminal import Terminal

# Create a terminal
terminal = Terminal()

# Run commands
terminal.run("uname -a")
terminal.run("ls")
terminal.run("pwd")

# Inspect command history
for stdout, stderr, exitcode in terminal.history:
    print("STDOUT:", stdout)
    print("STDERR:", stderr)
    print("EXITCODE:", exitcode)

# Run command in a different directory
terminal.run("ls", cwd="/")

# Run command with custom environment variables
terminal.run("printenv MY_VAR", env={"MY_VAR": "Hello World"})

# Run command with shell
terminal.run("echo $SHELL", shell=True)

# Run command without using OS environment variables
terminal.run("printenv", use_os_env=False)

# Run command with custom encoding
terminal.run("my_programm", encoding="utf-16")

# Run command with timeout
terminal.run("sleep 10", timeout=5)

# Run command and print stdout and stderr
terminal.run("ifconfig", print_stdout=True, print_stderr=True)

# Run command without printing stdout and stderr
terminal.run("ifconfig", print_stdout=False, print_stderr=False)

# Run command with a name
terminal.run("ifconfig", name="Network Configuration")

# Run command and inspect the Process object
process = terminal.run("ifconfig")
print("Process UUID:", process.get_uuid())
```

## Running remote processes via SSH

```python
from xterminal import SSHProcess

# Create an SSH client
client = SSHProcess.get_ssh_client(hostname="172.0.0.1", port=22, username="root", password="root")

# Create a process
process = SSHProcess(cmd="uname -a", ssh_client=client)

# Run the process
stdout, stderr, exitcode = process.run()
```

#### Run process in a different directory

```python
# Run command 'ls' in directory '/'
process = SSHProcess(cmd="ls", cwd="/", ssh_client=client)
```

## Create a SSH terminal to run multiple commands

```python
from xterminal import SSHProcess, SSHTerminal

# Create an SSH client
client = SSHProcess.get_ssh_client(hostname="172.0.0.1", port=22, username="root", password="root")

# Create a terminal
terminal = SSHTerminal(ssh_client=client)

# Run commands
terminal.run("uname -a")
terminal.run("ls")
```

#### Inspect command history

All commands that were run in the terminal are saved in the `history` attribute of the terminal. This attribute contains a list of tuples `(stdout, stderr, exitcode)`.

```python
# Run commands
terminal.run("uname -a")
terminal.run("ls")

# Get history
terminal.history
```

## Multi Client SSH Terminal

```python
from xterminal import SSHProcess, MultiClientSSHTerminal

# Create an SSH client
client1 = SSHProcess.get_ssh_client(hostname="172.0.0.1", port=22, username="root", password="root")
client2 = SSHProcess.get_ssh_client(hostname="172.0.0.2", port=22, username="root", password="root")

# Create a terminal with multiple clients
terminal = MultiClientSSHTerminal(ssh_clients=[client1, client2])
```
