import csv

import Package
import Truck
import HashMapper
import datetime

#preparation of program data for UI
packageHashTable = HashMapper.ChainingHashTable()

IDList = []
time = datetime.timedelta(hours=int(8), minutes=int(0))
deliveryInfo = [None] * 41

with open('WGUPS Package File - Sheet1.csv', newline='') as packageInfo:
    packageFile = csv.reader(packageInfo)

    for x in packageFile:
        pack = Package.package(x[0],x[5],x[1],x[2],x[3], x[6], x[7])
        IDList.append(x[0])
        packageHashTable.insert(x[0], pack)

def packageInfo(id):
    if(deliveryInfo[id] != None):
        print(deliveryInfo[id])

def startTruckDeliveries(truck):
    while (len(truck.packages) > 0):
        packInfo = (truck.deliverPackage(time))
        deliveryInfo[int(str(packInfo).split(",")[0])] = packInfo.split(",")


truck1 = Truck.truck("truck1")
truck2 = Truck.truck("truck2")
truck3 = Truck.truck("truck3")

i =0
for id in IDList:
    #print(str(len(truck1.packages)) + "   " + str(len(truck2.packages)))
    if(len(truck1.packages)<16):
        truck1.loadPackage(packageHashTable.search(id))
    elif(len(truck2.packages)<16):
        truck2.loadPackage(packageHashTable.search(id))

startTruckDeliveries(truck1)
startTruckDeliveries(truck2)
#startTruckDeliveries(truck3)

#UI section of code, program data generation complete
print("Welcome To WGUPS\nPlese enter package ID to view package info or a to view all, t total mileage, or q to quit, or a time from 8:00 to 12:00 ex input(start)'8:00 am' input(end)'9:00 am'\n")
while(True):
    userResponse = input()
    if(userResponse == "q"):
        print("goodbye")
        break
    elif(userResponse.isdigit()):
        if(int(userResponse) > 0 and int(userResponse) <= len(deliveryInfo) and deliveryInfo[int(userResponse)] != None):
            print("ID, Address, City, State, Weight(KILO), Delivery Deadline, Special Note, Status, Miles, Delivered")
            for x in deliveryInfo[int(userResponse)]:
                print(x, end=", ")
            #deliveryTime = ((((float(deliveryInfo[int(userResponse)][7]))/18) * 60))
            #arrivalTime = time + datetime.timedelta(minutes=deliveryTime)
            #print(arrivalTime)
        else:
            print("error, package not found")
    elif(userResponse == "a"):
        for x in deliveryInfo:
            if(x != None):
                for z in x:
                    print(z, end=", ")
                print("\n")
    elif(userResponse == "t"):
        print(str(round((truck1.milesTraveled + truck2.milesTraveled + truck3.milesTraveled), 2)) + " miles traveled")
        print("truck 1: miles traveled " + str(round(truck1.milesTraveled, 2)))
        print("truck 2: miles traveled " + str(round(truck2.milesTraveled, 2)))
        print("truck 3: miles traveled " + str(round(truck3.milesTraveled, 2)))
                # deliveryTime = ((((float(x[7])) / 18) * 60))
                # arrivalTime = time + datetime.timedelta(minutes=deliveryTime)
                # print(arrivalTime)
    elif(":" in userResponse):
        startTime = datetime.timedelta(hours=int(int(userResponse.split(":")[0])), minutes=int(int(userResponse.split(":")[1][0:2])))

        print("please enter end time")
        userResponse = input()
        endTime = datetime.timedelta(hours=int(int(userResponse.split(":")[0])),minutes=int(int(userResponse.split(":")[1][0:2])))

        if(startTime < endTime):
            for x in deliveryInfo:

                if(x != None):

                    timeDelivered = datetime.timedelta(hours=int(int(x[9].split(":")[0])),minutes=int(int(x[9].split(":")[1][0:2])))

                    if(timeDelivered > startTime and timeDelivered < endTime):
                        x[7] = "delivered"
                        print(x)
                    elif(timeDelivered > endTime):
                        x[7] = "en route"
                        print(x)
                    else:
                        x[7] = "at hub"
                        print(x)

    else:
        print("error, please enter another input")