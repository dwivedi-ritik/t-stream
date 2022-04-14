import sys
import time
import threading
import random

spinners = [ ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"] , ["✶","✸","✹", "✺", "✹", "✷"] , ["⠄","⠆","⠇","⠋","⠙", "⠸","⠰","⠠","⠰","⠸","⠙","⠋","⠇","⠆"]]

fav = random.choice(spinners)


class Spinner:
    busy = False
    delay = 0.2

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in fav: yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        sys.stdout.write("\033[?25l\u001b[35;1m")
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()
        sys.stdout.write("\u001b[0m\033[?25h")

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

