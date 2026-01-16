import threading
import time
from .process import Process
from typing import Optional

class BackgroundProcesses:
    def __init__(self, p: Process):
        """
        Initialize the BackgroundProcesses manager.
        
        Args:
            p: Process instance to run in background
        """
        self.process = p
        self.thread = None
        self.is_running = False
        self.thread_lock = threading.Lock()
    
    def run(self):
        """
        Run the process by calling its "run" method in a separate thread.
        """
        with self.thread_lock:
            if self.is_running:
                return  # Already running
            
            def target():
                try:
                    self.process.run()
                finally:
                    with self.thread_lock:
                        self.is_running = False
            
            self.thread = threading.Thread(target=target)
            self.thread.daemon = True  # Dies when main thread dies
            self.thread.start()
            
            self.is_running = True
    
    def get_thread(self) -> Optional[threading.Thread]:
        """
        Get the thread that executes the process.
        
        Returns:
            The threading.Thread object or None if not running
        """
        with self.thread_lock:
            return self.thread
    
    def get_status(self) -> str:
        """
        Returns whether process has finished or is still running.
        
        Returns:
            "running" if process is still executing, "finished" if completed
        """
        with self.thread_lock:
            if not self.is_running:
                return "finished"
            elif self.thread and self.thread.is_alive():
                return "running"
            else:
                return "finished"
    
    def is_finished(self) -> bool:
        """
        Check if the process has finished execution.
        
        Returns:
            True if process has finished, False otherwise
        """
        return self.get_status() == "finished"
    
    def is_running(self) -> bool:
        """
        Check if the process is currently running.
        
        Returns:
            True if process is running, False otherwise
        """
        return self.get_status() == "running"
    
    def wait_for_completion(self, timeout: float = None) -> bool:
        """
        Wait for the process to complete.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if process completed, False if timeout occurred
        """
        if self.thread:
            self.thread.join(timeout)
            return not self.thread.is_alive()
        return True
