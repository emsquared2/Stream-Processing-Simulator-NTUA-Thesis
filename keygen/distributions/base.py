class Distribution:
    def __init__(self, keys):
        self.keys = keys

    def generate(self, arrival_rate):
        raise NotImplementedError("This method should be overridden by subclasses")
