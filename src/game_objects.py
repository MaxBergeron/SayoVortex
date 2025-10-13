class HitObject:
    def __init__(self, key, duration, time):
        self.key = int(key)
        self.duration = float(duration)
        self.time = float(time)

    def __repr__(self):
        return f"HitObject(key={self.key}, duration={self.duration}, time={self.time})"


class LaserObject:
    def __init__(self, continue_chain, position, time):
        self.continue_chain = bool(int(continue_chain))
        self.position = int(position)
        self.time = float(time)

    def __repr__(self):
        return f"LaserObject(chain={self.continue_chain}, pos={self.position}, time={self.time})"