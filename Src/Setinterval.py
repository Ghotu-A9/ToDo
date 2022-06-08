class SetInterval:
    def __init__(self, fun, *arg1, **arg2):
        self.timer = None
        self.interval = 1
        self.function = fun
        self.arg1 = arg1
        self.arg2 = arg2
        self.running = False
        self.start()

    def run(self):
        self.running = False
        self.function(*self.arg1, **self.arg2)
        self.start()

    def start(self):
        if not self.running:
            self.timer = Timer(self.interval, self.run)
            self.timer.start()
            self.running = True

    def stop(self):
        self.timer.cancel()
        self.running = False