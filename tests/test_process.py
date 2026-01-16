from tnc_process import Process


def test_process_constructor():
    """
    Test the constructor of the process class
    """
    p = Process(["python", "--version"])
    assert type(p).__name__ == "Process"


def test_process_run_success():
    """
    Try running python command which should be return 0 as exit code
    """
    p = Process(["python", "--version"])
    p.run()
    assert p.get_exit_code() == 0
    assert p.get_exception() is None


def test_process_run_error():
    """
    Try running a command that not exists and assert that the exit code is 1
    """
    p = Process(["abcdef"])
    try:
        p.run(stop_on_error=False)
    except FileNotFoundError:
        assert p.get_exit_code() == 1
        assert type(p.get_exception()).__name__ == "FileNotFoundError"
