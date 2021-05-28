class Sensor:
    def __init__(self, local_id, name, source):
        self.local_id = local_id
        self.name = name
        self.source = source
        self.pollutants = dict()

    def get_dict(self):
        sensor = Sensor(self.local_id, self.name, self.source)
        pollutants = dict()
        for pollutant in self.pollutants.keys():
            pollutants[pollutant] = self.pollutants[pollutant].get_dict()
        sensor.pollutants = pollutants
        return sensor.__dict__
