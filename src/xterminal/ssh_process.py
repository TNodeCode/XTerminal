import paramiko
from paramiko import SSHClient
from datetime import datetime
from .process import Process
from threading import Thread


class SSHProcess(Process):
    def __init__(
            self,
            cmd: list[str] | str,
            ssh_client: SSHClient = None,
            hostname: str = None,
            port: int = 22,
            username: str = None,
            password: str = None,
            missing_host_key_policy=paramiko.AutoAddPolicy(),
            print_stdout: bool = True,
            print_stderr: bool = True,
            shell: bool = False,
            cwd: str = None,
            env: dict = None,
            encoding: str = "utf-8",
            use_os_env: bool = True,
            name: str | None = None,
            timeout: float | None = None,
    ) -> None:
        super(SSHProcess, self).__init__(
            cmd=cmd,
            print_stdout=print_stdout,
            print_stderr=print_stderr,
            shell=shell,
            cwd=cwd,
            env=env,
            encoding=encoding,
            use_os_env=use_os_env,
            name=name,
            timeout=timeout
        )
        self.cwd = "~" if cwd is None else cwd
        if type(ssh_client) == SSHClient:
            self.ssh_client: SSHClient = ssh_client
        else:
            self.ssh_client = SSHProcess.get_ssh_client(
                hostname=hostname,
                port=port,
                username=username,
                password=password,
                missing_host_key_policy=missing_host_key_policy
            )

    @staticmethod
    def get_ssh_client(
        hostname: str = None,
        port: int = 22,
        username: str = None,
        password: str = None,
        name=None,
        missing_host_key_policy=paramiko.AutoAddPolicy(),
    ) -> SSHClient:
        ssh_client = SSHClient()
        if name is not None:
            ssh_client.name = name
        else:
            ssh_client.name = hostname
        if missing_host_key_policy:
            ssh_client.set_missing_host_key_policy(missing_host_key_policy)
            ssh_client.connect(
                hostname=hostname,
                port=port,
                username=username,
                password=password
            )
        return ssh_client

    @staticmethod
    def read_stdout(self):
        """
        Read from stdout
        :param self: Reference to Process object
        """
        for line in self.p[1]:
            # Decode byte array from stdout
            self.last_line_stdout = line.strip()
            # Dispatch event
            self.on_stdout_readline.on_next(self)

    @staticmethod
    def read_stderr(self):
        """
        Read from stderr
        :param self: Reference to Process object
        """
        if self.p[2]:
            for line in self.p[2]:
                # Decode byte array from stderr
                self.last_line_stderr = line.strip()
                # Dispatch event
                self.on_stderr_readline.on_next(self)

    def run(self, stop_on_error: bool = True):
        """
        Run the process
        :param stop_on_error: flag to catch errors that occur during script execution or to let them through
        :return: Triple (stdout, stderr, exit_code)
        """
        # Check if Process was already executed
        if self.finished:
            return self.out, self.err, self.exit_code

        # Register event handlers
        self.register_stdout_readline_handler(self.stdout_logger)
        self.register_stderr_readline_handler(self.stderr_logger)

        # Start Process
        self.on_process_start.on_next(None)
        self.on_process_start.on_completed()

        try:
            # Log start time
            self.start = datetime.now()

            # if self.use_os_env:
            #    self._env.update(os.environ.copy())
            #    self._env.update(self.env)

            # Run process
            cmd = self.cmd if type(self.cmd) == str else " ".join(self.cmd)
            cmd = f"cd {self.cwd} && {cmd}"
            self.p = self.ssh_client.exec_command(
                command=cmd,
                timeout=self.timeout,
                environment=self._env
            )

            # Read from stdout and stderr.
            # This has to be done within threads, because both channels can block if the buffer is full.
            # So both channels have to read in parallel.
            t_stdout = Thread(target=SSHProcess.read_stdout, args=[self])
            t_stderr = Thread(target=SSHProcess.read_stderr, args=[self])
            t_stdout.start()
            t_stderr.start()
            t_stdout.join()
            t_stderr.join()

            # Get exit code
            self.exit_code = self.p[1].channel.recv_exit_status()
            self.end = datetime.now()
            self.finished = True

            self.on_stdout_readline.on_completed()
            self.on_process_finished.on_next(None)
            self.on_process_finished.on_completed()
        except FileNotFoundError as err:
            self.exception = err
            self.exit_code = 1
            if stop_on_error:
                err.filename = self.cmd[0] if isinstance(
                    self.cmd, list) else self.cmd
                raise err

        if stop_on_error and self.exit_code > 0:
            raise OSError('\n'.join(self.err))

        return self.out, self.err, self.exit_code
