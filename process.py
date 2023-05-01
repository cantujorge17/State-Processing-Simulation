class process():
    def __init__(self, at, ct, it, id):
        self.arrivalTime = at
        self.cpuTime = ct
        self.ioTime = it
        self.ioDuration = id
        self.currentState = 'Ready'
    tempArrivalTime = 0
    tempCPUTime = 0
    tempIOTime = 0
    tempIODuration = 0

# This is my first time using classes in python. This was easier than I expected.