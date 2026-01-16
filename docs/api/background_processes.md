# BackgroundProcesses

Class: `BackgroundProcesses`

Purpose: Run a `Process` instance in a background thread and query its status.

Constructor parameters

- `p`: a `Process` instance

Key methods

- `run()` — starts the provided `Process` in a daemon thread; no-op if already running.
- `get_thread()` — returns the `threading.Thread` executing the process, or `None`.
- `get_status()` — returns `"running"` or `"finished"`.
- `is_finished()` / `is_running()` — convenience status checks.
- `wait_for_completion(timeout: float = None)` — join the background thread; returns `True` if completed.
