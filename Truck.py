import csv

class truck:
    def __init__(self):
        self.packages = []  # Instance variable: each truck has its own package list
        self.travelSpeed = 18
        self.currentLocation = "4001 South 700 East"
        self.milesTraveled = 0

    def loadPackage(self, package):
        if ((len(self.packages) < 16)):
            self.packages.append(package)


    def nextClosestPackage(self):
        i = 0
        j=0

        nearestDistance = float(self.findDistance(self.currentLocation, str(self.packages[0]).split(",")[1])) #initializes nearest distance to distance of currentLocation and first package in list [0]
        for x in self.packages:
            if(float(self.findDistance(self.currentLocation, str(x).split(",")[1])) < nearestDistance):
                j=i #stores nearest package index
                nearestDistance = float(self.findDistance(self.currentLocation, str(x).split(",")[1]))

            i += 1
        return self.packages.pop(j)


    def deliverPackage(self):
        pack = str(self.nextClosestPackage()).split(",") #pack[1] will retrieve the package address

        if(pack[6] == ""):  #checks for special note on package
            self.milesTraveled += float(self.findDistance(self.currentLocation, pack[1]))
            self.currentLocation = pack[1]
            # print("delivered package at " + self.currentLocation)
            # print("\n" + str(self.milesTraveled))
        else:
            pass
            # print(len(self.packages))
        packInfo = ""
        for x in pack:
            packInfo += str(x) + ","
        return packInfo + str(self.milesTraveled)

    def findDistance(self, x_address, y_address):
        addressList = []
        with open("WGUPS Distance Table - Sheet1.csv", newline='') as distanceTableData:
            i = 0
            distanceFile = csv.reader(distanceTableData)

            for x in distanceFile:
                addressList.append(((x[1][1:x[1].find("(")]).strip("\n"), i))
                i += 1

        with open("WGUPS Distance Table - Sheet1.csv", newline='') as distanceTableData:
            distanceFile = csv.reader(distanceTableData)

            for x in distanceFile:
                if ((x[1][1:x[1].find("(")]).strip("\n") == x_address):
                    for y in addressList:
                        if (y[0] == y_address):
                            if((x[y[1] + 1]) != ""):
                                return (x[y[1] + 1])
                            else:
                                return (self.findDistance(y_address,x_address))
