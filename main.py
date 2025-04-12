import csv

import Package
import Truck
import HashMapper
import datetime

#preparation of program data for UI
packageHashTable = HashMapper.ChainingHashTable()

IDList = []
time = 8.00 # 8:00 AM
deliveryInfo = [None] * 41
timeObject = datetime.timedelta(hours=int(8), minutes=int(0))

with open('WGUPS Package File - Sheet1.csv', newline='') as packageInfo:
    packageFile = csv.reader(packageInfo)

    for x in packageFile:
        pack = Package.package(x[0],x[5],x[1],x[2],x[3], x[6], x[7])
        IDList.append(x[0])
        packageHashTable.insert(x[0], pack)

def packageInfo(id):
    if(deliveryInfo[id] != None):
        print(deliveryInfo[id])


truck1 = Truck.truck()
truck2 = Truck.truck()
truck3 = Truck.truck()

i =0
for id in IDList:
    if(len(truck1.packages)<16):
        truck1.loadPackage(packageHashTable.search(id))
    elif(len(truck2.packages)<16):
        truck2.loadPackage(packageHashTable.search(id))
    else:
        truck3.loadPackage(packageHashTable.search(id))

while(len(truck1.packages) > 0):
    packInfo = (truck1.deliverPackage())
    deliveryInfo[int(str(packInfo).split(",")[0])] = packInfo.split(",")


#UI section of code, program data generation complete
print("Welcome To WGUPS\nPlese enter package ID to view package info or a to view all or q to quit\n")
while(True):
    userResponse = input()
    if(userResponse == "q"):
        print("goodbye")
        break
    elif(userResponse.isdigit()):
        if(deliveryInfo[int(userResponse)] != None):
            print("ID, Address, City, State, Weight(KILO), Delivery Deadline, Special Note, Status, Delivery Time")
            for x in deliveryInfo[int(userResponse)][0:7]:
                print(x, end=", ")
            deliveryTime = ((((float(deliveryInfo[int(userResponse)][7]))/18) * 60))
            arrivalTime = timeObject + datetime.timedelta(minutes=deliveryTime)
            print(arrivalTime)
        else:
            print("error, package not found")
    elif(userResponse == "a"):
        for x in deliveryInfo:
            if(x != None):
                for z in x[0:7]:
                    print(z, end=", ")

                deliveryTime = ((((float(x[7])) / 18) * 60))
                arrivalTime = timeObject + datetime.timedelta(minutes=deliveryTime)
                print(arrivalTime)
    else:
        print("error, please enter another input")