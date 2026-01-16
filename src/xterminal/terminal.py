from .process import Process


class Terminal():
    def __init__(
            self,
            print_stdout: bool = True,
            print_stderr: bool = True,
            shell: bool = False,
            cwd: str | None = None,
            env: dict = None,
            encoding: str = "utf-8",
            use_os_env: bool = True,
            name: str | None = None,
            timeout: float | None = None,
            stop_on_error: bool = False,
    ):
        self.print_stdout = print_stdout
        self.print_stderr = print_stderr
        self.shell = shell
        self.cwd = cwd
        self.env = env
        self.encoding = encoding
        self.use_os_env = use_os_env
        self.name = name
        self.timeout = timeout
        self.stop_on_error = stop_on_error
        self.history: list[Process] = []

    def run(self, cmd: str, cwd=None):
        if cwd is None:
            cwd = self.cwd
        p = Process(
            cmd=cmd,
            cwd=cwd,
            print_stdout=self.print_stdout,
            print_stderr=self.print_stderr,
            shell=self.shell,
            env=self.env,
            encoding=self.encoding,
            use_os_env=self.use_os_env,
            timeout=self.timeout,
            name=self.name,
        )
        res = p.run(stop_on_error=self.stop_on_error)
        self.history.append(res)
        return res
