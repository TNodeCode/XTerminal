from paramiko import SSHClient
from .ssh_process import SSHProcess
from .ssh_terminal import SSHTerminal


class MultiClientSSHTerminal():
    def __init__(self, ssh_clients: list[SSHClient]):
        self.terminals = []
        self.history = {}
        for client in ssh_clients:
            self.terminals.append(SSHTerminal(ssh_client=client))
            self.history |= {client.name: []}

    def run(self, cmd: str):
        results = {}
        for terminal in self.terminals:
            result = terminal.run(cmd)
            self.history[terminal.ssh_client.name].append(result)
            results |= {terminal.ssh_client.name: result}
        return results
