
class Pollutant:
    def __init__(self, notation, concentration):
        self.notation = notation
        self.concentration = concentration
        self.measurements = []

    def get_dict(self):
        measurements = []
        pollutant = Pollutant(self.notation, self.concentration)
        for measurement in self.measurements:
            measurements.append(measurement.__dict__)
        pollutant.measurements = measurements
        return pollutant.__dict__
