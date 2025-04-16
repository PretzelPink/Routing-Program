import csv
import datetime


class truck:

    #constructor initializes truck name (truckID), and location starting at hub
    def __init__(self, truckid):
        self.packages = []  # Instance variable, each truck has its own package list
        self.travelSpeed = 18
        self.currentLocation = "4001 South 700 East"
        self.milesTraveled = 0
        self.truckID = truckid
        self.timeDeployed = datetime.timedelta(hours=int(0),minutes=int(0))

    #gets if truck at hub to determine if a driver is available
    def atHub(self):
        if(self.currentLocation == "4001 South 700 East"):
            return True
        else:
            return False

    #called line 41 (main.py) when truck has no more packages, returns to hub
    def backToHub(self):
        miles = self.findDistance(self.currentLocation, "4001 South 700 East")
        self.currentLocation = "4001 South 700 East"
        #returns travel time to hub
        return (datetime.timedelta(minutes=(float(miles) / 18) * 60))

    #appends package object to packages list if length of list < 16
    def loadPackage(self, package):
        if ((len(self.packages) < 16)):
            self.packages.append(package)

    #O(n), greedy algorithm, selects next closest delivery location
    def nextClosestPackage(self):
        i = 0
        j=0
        nearestDistance = float(self.findDistance(self.currentLocation, str(self.packages[0]).split(",")[1])) #initializes nearest distance to distance of currentLocation and first package in list [0]
        for x in self.packages:
            #x package id,location,city,state,deadline split(",") results in list x[1] == package address
            if ((float(self.findDistance(self.currentLocation, str(x).split(",")[1])) < nearestDistance)):
                j = i #if x distance is closer, the new i index is set to j
                nearestDistance = float(self.findDistance(self.currentLocation, str(x).split(",")[1]))

        #Prioritizes earliest deadline and nearest distance, proved less efficient
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

    #O(n), moves truck to new package address and generates, new package infor string
    #calculates route time and miles traveled, returns new package info in string to be split(",")
    def deliverPackage(self):
        pack = (str(self.nextClosestPackage()).split(","))#pack[1] will retrieve the package address

        routeDistance = float(self.findDistance(self.currentLocation, pack[1]))
        self.milesTraveled += routeDistance
        self.currentLocation = pack[1]

        packInfo = ""
        for x in pack:
            packInfo += str(x) + ","

        packInfo += str(round(self.milesTraveled, 2)) + "," + str(datetime.timedelta(minutes=(routeDistance / 18) * 60)) + "," + self.truckID
        return packInfo

    #O(n^3), looks up 2 provided addresses on Distance Table.csv, returns distance
    def findDistance(self, x_address, y_address):
        addressList = []
        with open("WGUPS Distance Table - Sheet1.csv", newline='') as distanceTableData:
            i = 0
            distanceFile = csv.reader(distanceTableData)

            #generates list of addresses with index (i) within a tuple, providing column/row index
            for x in distanceFile:
                #ex:1488 4800 S (84123), 1488 4800 S is extracted, allowing simplified address usage from each row in Distance Table.csv
                addressList.append(((x[1][1:x[1].find("(")]).strip("\n"), i))
                i += 1

        with open("WGUPS Distance Table - Sheet1.csv", newline='') as distanceTableData:
            distanceFile = csv.reader(distanceTableData)

            for x in distanceFile:
                #check if provided x_address is within csv file rows
                if ((x[1][1:x[1].find("(")]).strip("\n") == x_address):
                    for y in addressList:
                        #checks if y_address is within addressList, column index provided (address, column index)
                        if (y[0] == y_address):
                            #if x at column index y[1] + 1 != "" return distance found, else swap addresses to account for possible csv file formatting issue
                            if((x[y[1] + 1]) != ""):
                                return (x[y[1] + 1])
                            else:
                                return (self.findDistance(y_address,x_address))
