

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

