class truck:
    def __init__(self):
        self.packages = []  # Instance variable: each truck has its own package list
        self.travelSpeed = 18
        self.currentLocation = "4001 South 700 East"

    def loadPackages(self, packageList):
        i = 0
        for x in packageList:
            if (((i < 16)) and (len(packageList) > 0)):
                self.packages.append(x)
                i += 1
            else:
                break