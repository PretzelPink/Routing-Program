import csv
import datetime


class truck:
    def __init__(self, truckid):
        self.packages = []  # Instance variable: each truck has its own package list
        self.travelSpeed = 18
        self.currentLocation = "4001 South 700 East"
        self.milesTraveled = 0
        self.truckID = truckid
        self.timeDeployed = datetime.timedelta(hours=int(0),minutes=int(0))

    def atHub(self):
        if(self.currentLocation == "4001 South 700 East"):
            return True
        else:
            return False

    def backToHub(self):
        miles = self.findDistance(self.currentLocation, "4001 South 700 East")
        self.currentLocation = "4001 South 700 East"
        return (datetime.timedelta(minutes=(float(miles) / 18) * 60))

    def loadPackage(self, package):
        if ((len(self.packages) < 16)):
            self.packages.append(package)


    def nextClosestPackage(self):
        i = 0
        j=0
        nearestDistance = float(self.findDistance(self.currentLocation, str(self.packages[0]).split(",")[1])) #initializes nearest distance to distance of currentLocation and first package in list [0]
        for x in self.packages:
            if ((float(self.findDistance(self.currentLocation, str(x).split(",")[1])) < nearestDistance)):
                j = i
                nearestDistance = float(self.findDistance(self.currentLocation, str(x).split(",")[1]))
            # if((":" in str(x).split(",")[5]) and ("EOD" in str(self.packages[j]).split(",")[5])):
            #     j=i
            #     nearestDistance = float(self.findDistance(self.currentLocation, str(x).split(",")[1]))
            #
            # elif((":" in str(x).split(",")[5]) and (":" in str(self.packages[j]).split(",")[5])):
            #     if(int(str(x).split(",")[5].split(":")[0]) < int(str(self.packages[j]).split(",")[5].split(":")[0])):
            #         j=i #stores nearest package index
            #         nearestDistance = float(self.findDistance(self.currentLocation, str(x).split(",")[1]))
            #
            #     elif (int(str(x).split(",")[5].split(":")[0]) == int(str(self.packages[j]).split(",")[5].split(":")[0])):
            #         if((float(self.findDistance(self.currentLocation, str(x).split(",")[1])) < nearestDistance)):
            #             j=i
            #             nearestDistance = float(self.findDistance(self.currentLocation, str(x).split(",")[1]))

            i += 1
        return self.packages.pop(j)

    # def nextPackage(self):
    #     if(len(self.packages)>0):
    #         nextPackage = self.packages.pop(0)
    #         return nextPackage

    def deliverPackage(self, currentTime):
        pack = (str(self.nextClosestPackage()).split(","))#pack[1] will retrieve the package address
        routeDistance = 0.0
        #print(pack)
        #print(pack)
        routeDistance = float(self.findDistance(self.currentLocation, pack[1]))
        self.milesTraveled += routeDistance
        self.currentLocation = pack[1]

        packInfo = ""
        for x in pack:
            packInfo += str(x) + ","

        packInfo += str(round(self.milesTraveled, 2)) + "," + str(datetime.timedelta(minutes=(routeDistance / 18) * 60)) + "," + self.truckID
        return packInfo


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
