class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2 # Исправлено: увеличиваем дистанцию на скорость, а не на удвоенную скорость

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name

class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        time = 0
        while self.participants:
            time += 1
            for participant in self.participants[:]:  # Используем копию списка для итерации
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[time] = participant
                    self.participants.remove(participant)
        return finishers

