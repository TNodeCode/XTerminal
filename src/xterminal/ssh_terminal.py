from paramiko import SSHClient
from .ssh_process import SSHProcess


class SSHTerminal():
    def __init__(
            self,
            ssh_client: SSHClient = None,
            print_stdout: bool = True,
            print_stderr: bool = True,
            shell: bool = False,
            cwd: str = "~",
            env: dict = None,
            encoding: str = "utf-8",
            use_os_env: bool = True,
            name: str | None = None,
            timeout: float | None = None,
    ):
        self.ssh_client = ssh_client
        self.print_stdout = print_stdout
        self.print_stderr = print_stderr
        self.shell = shell
        self.cwd = cwd
        self.env = env
        self.encoding = encoding
        self.use_os_env = use_os_env
        self.name = name
        self.timeout = timeout
        self.history: list[SSHProcess] = []

    def run(self, cmd: str, cwd=None):
        if cwd is None:
            cwd = self.cwd
        p = SSHProcess(cmd=f"cd {cwd} && {cmd}", ssh_client=self.ssh_client)
        res = p.run()
        self.history.append(res)
        return res
