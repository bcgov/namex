import threading

class email_notification_debouncer:
    """
    A class to handle debouncing of email notifications. This ensures that email notifications are sent 
    only after a certain period of inactivity, avoiding multiple emails being sent in quick succession.
    """

    def __init__(self):
        self.five_minutes = 300
        self.timer = None  
        self.lock = threading.Lock() 

    def debounce(self, callback, *args, **kwargs):
        """
        Debounces the execution of the callback function. If this method is called multiple times within the debounce 
        period, the previous timer is canceled and a new timer is started for the new email notification.
        """
        with self.lock:
            if self.timer:
                self.timer.cancel() 
            self.timer = threading.Timer(self.five_minutes, self._execute, [callback, *args], kwargs)
            self.timer.start()

    def _execute(self, callback, *args, **kwargs):
        """
        Executes the callback function (sending the email) with the provided arguments. This method
        is called when the timer expires.
        """
        callback(*args, **kwargs)
