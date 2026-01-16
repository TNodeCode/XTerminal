import io
import os
import subprocess
import sys
import uuid
from datetime import datetime
from os import getcwd
from threading import Thread

import reactivex as rx

ON_POSIX = 'posix' in sys.builtin_module_names


class Process:
    def __init__(
            self,
            cmd: list[str] | str,
            print_stdout: bool = True,
            print_stderr: bool = True,
            shell: bool = False,
            cwd: str = None,
            env: dict = None,
            encoding: str = "utf-8",
            use_os_env: bool = True,
            name: str | None = None,
            timeout: float | None = None,
    ):
        self.uuid: uuid.UUID = uuid.uuid4()
        self.cmd = cmd if type(cmd) == list else cmd.split()
        self.cwd = getcwd() if cwd is None else cwd
        self.env = dict() if env is None else env
        self.encoding = encoding
        self.use_os_env = use_os_env
        self.print_stdout = print_stdout
        self.print_stderr = print_stderr
        self.shell = shell
        self.p = None
        self.exit_code: int | None = None
        self.on_stdout_readline = rx.subject.Subject()
        self.on_stderr_readline = rx.subject.Subject()
        self.on_process_start = rx.subject.Subject()
        self.on_process_finished = rx.subject.Subject()
        self.last_line_stdout: str = ""
        self.last_line_stderr: str = ""
        self.name: str | None = name
        self.out: list[str] = []
        self.err: list[str] = []
        self.exception: Exception | None = None
        self.start: datetime | None = None
        self.end: datetime | None = None
        self._env = {}
        self.timeout = timeout
        self.finished: bool = False

    def get_uuid(self) -> uuid.UUID:
        """
        Get the UUID of the process
        :return: process UUID
        """
        return self.uuid

    def stdout_logger(self, p):
        """
        Event handler for stdout that logs stdout to the console
        :param p: process instance
        """
        # Save line from stdout
        self.out.append(p.get_last_line_from_stdout())
        # Print line from stdout
        if self.print_stdout:
            if self.name:
                print(f"[{self.name}]", p.get_last_line_from_stdout())
            else:
                print(p.get_last_line_from_stdout())

    def stderr_logger(self, p):
        """
        Event handler for stderr that logs stderr to the console
        :param p: process instance
        """
        # Save line from stderr
        self.err.append(p.get_last_line_from_stderr())
        # Print line from stderr
        if self.print_stderr:
            if self.name:
                print(f"[{self.name}]", p.get_last_line_from_stderr())
            else:
                print(p.get_last_line_from_stderr())

    def register_stdout_readline_handler(self, f):
        """
        Register an event handler that is called after each line outputted to stdout
        :param f:
        :return:
        """
        self.on_stdout_readline.subscribe(f)

    def register_stderr_readline_handler(self, f):
        """
        Register an event handler that is called after each line outputted to stderr
        :param f:
        :return:
        """
        self.on_stderr_readline.subscribe(f)

    def write(self, value: str):
        """
        Write to stdin
        :param value: string that should be written to stdin
        """
        self.get_stdin().write(value)
        self.get_stdin().flush()

    def get_last_line_from_stdout(self) -> str:
        """
        Get the last line from the output
        :return: The last line from the output
        """
        return self.last_line_stdout

    def get_last_line_from_stderr(self) -> str:
        """
        Get the last line from the output
        :return: The last line from the output
        """
        return self.last_line_stderr

    def get_stdin(self) -> io.BufferedWriter:
        """
        Get stdin of process
        :return: stdin
        """
        return self.p.stdin

    def get_stdout(self) -> io.BufferedReader:
        """
        Get stdout of process
        :return: stdout
        """
        return self.p.stdout

    def get_stderr(self) -> io.BufferedReader:
        """
        Get stderr of process
        :return: stderr
        """
        return self.p.stderr

    def get_output(self) -> list:
        """
        Get output of process. This is available after the process finished.
        The output is formatted as a list where each list element contains one line of the output.
        :return:
        """
        return self.out

    def get_process_env(self):
        """
        Get the environment the process was executed with
        :return:    process environment
        """
        return self._env

    def get_error(self) -> list:
        """
        Get the output of stderr as a list of strings. Each list element contains one line of stderr.
        :return: output of stderr
        """
        return self.err

    def get_exit_code(self) -> int:
        """
        Get exit code of process
        :return: process exit code
        """
        return self.exit_code

    def get_exception(self) -> Exception | None:
        """
        Get process exception if one occurred during the process execution
        :return: process exception
        """
        return self.exception

    def is_finished(self) -> bool:
        """
        Check if process has finished
        :return: true if process has finished, false otherwise
        """
        return self.finished

    def get_start(self) -> datetime:
        """
        Get start time of process
        :return: process start time
        """
        return self.start

    def get_end(self) -> datetime:
        """
        Get end time of process
        :return: process end time
        """
        return self.end

    @staticmethod
    def read_stdout(self):
        """
        Read from stdout
        :param self: Reference to Process object
        """
        for line in iter(self.p.stdout.readline, b''):
            # Decode byte array from stdout
            self.last_line_stdout = line.rstrip().decode(self.encoding, errors="replace")
            # Dispatch event
            self.on_stdout_readline.on_next(self)

    @staticmethod
    def read_stderr(self):
        """
        Read from stderr
        :param self: Reference to Process object
        """
        if self.p.stderr:
            for line in iter(self.p.stderr.readline, b''):
                # Decode byte array from stderr
                self.last_line_stderr = line.rstrip().decode(self.encoding)
                # Dispatch event
                self.on_stderr_readline.on_next(self)

    def _run_process(self):
        # Run process
        self.p = subprocess.Popen(
            self.cmd,
            shell=self.shell,
            cwd=self.cwd,
            env=self._env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

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

            if self.use_os_env:
                self._env.update(os.environ.copy())
                self._env.update(self.env)

            # Run process
            self._run_process()

            # Read from stdout and stderr.
            # This has to be done within threads, because both channels can block if the buffer is full.
            # So both channels have to read in parallel.
            t_stdout = Thread(target=Process.read_stdout, args=[self])
            t_stderr = Thread(target=Process.read_stderr, args=[self])
            t_stdout.start()
            t_stderr.start()
            t_stdout.join()
            t_stderr.join()

            # Get exit code
            self.exit_code = self.p.wait(timeout=30)
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
