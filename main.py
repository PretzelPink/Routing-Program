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
    global time
    while (True):
        if(len(truck.packages) > 0):
            packInfo = (truck.deliverPackage(time))
            processedInfo = packInfo.split(",")
            time += (datetime.timedelta(hours=int(0),minutes=int(str(packInfo.split(",")[9]).split(":")[1])))
            #print(str(time) + "        " + str(packInfo))
            processedInfo[9] = str(time)
            deliveryInfo[int(str(packInfo).split(",")[0])] = processedInfo
        else:
            time += truck.backToHub()
            break


truck1 = Truck.truck("truck1")
truck2 = Truck.truck("truck2")
truck3 = Truck.truck("truck3")

i =0

truck1.loadPackage(packageHashTable.search("15"))  # 9:00 am deadline
truck1.loadPackage(packageHashTable.search("14"))  # must be delivered with 15,9   deadline 10:20 am
truck1.loadPackage(packageHashTable.search("13"))  # deadline 10:30 am
truck1.loadPackage(packageHashTable.search("20"))  # must be delivered with 13, 15 deadline 10:20 am
truck1.loadPackage(packageHashTable.search("19"))  # must be delivered with 13, 15 deadline 10:20 am
truck1.loadPackage(packageHashTable.search("16"))  # must be delivered with 13, 19 deadline 10:20 am
truck1.loadPackage(packageHashTable.search("1"))   # deadline 10:30 am
truck1.loadPackage(packageHashTable.search("29"))  # deadline 10:30 am
truck1.loadPackage(packageHashTable.search("30"))  # deadline 10:30 am
truck1.loadPackage(packageHashTable.search("31"))  # deadline 10:30 am
truck1.loadPackage(packageHashTable.search("34"))  # deadline 10:30 am
truck1.loadPackage(packageHashTable.search("37"))  # deadline 10:30 am
truck1.loadPackage(packageHashTable.search("40"))  # deadline 10:30 am


truck2.loadPackage(packageHashTable.search("6"))  # delayed until 9:05 am deadline 10:30
truck2.loadPackage(packageHashTable.search("25"))  # delayed until 9:05 am deadline 10:30
truck2.loadPackage(packageHashTable.search("28"))  # delayed until 9:05 am
truck2.loadPackage(packageHashTable.search("32"))  # delayed until 9:05 am
truck2.loadPackage(packageHashTable.search("3"))  # can only be on truck2
truck2.loadPackage(packageHashTable.search("18"))  # can only be on truck2
truck2.loadPackage(packageHashTable.search("36"))  # can only be on truck2
truck2.loadPackage(packageHashTable.search("38"))  # can only be on truck2

truck3.loadPackage(packageHashTable.search("9"))   # address corrected at 10:20 am  EOD

for id in IDList:

    if((str(packageHashTable.search(id)).split(",")[6]) == "" and (str(packageHashTable.search(id)).split(",")[5]) == "EOD" and id != "19"):
        if(len(truck1.packages)<8):
            truck1.loadPackage(packageHashTable.search(id))
        elif(len(truck2.packages)<16):
            truck2.loadPackage(packageHashTable.search(id))
        else:
            truck3.loadPackage(packageHashTable.search(id))


truck1.timeDeployed = time
startTruckDeliveries(truck1)

if(time >= (datetime.timedelta(hours=int(9),minutes=int(5)))):
    truck2.timeDeployed = time
    startTruckDeliveries(truck2)

if(truck1.atHub()):
    truck3.timeDeployed = time
    startTruckDeliveries(truck3)


#UI section of code, program data generation complete
print("Welcome To WGUPS\nPlese enter package ID to view package info or a to view all, t total mileage, or q to quit, or a time from 8:00 to 12:00 ex input(start)'8:00 am' input(end)'9:00 am'\n")

for x in deliveryInfo:
    if (x != None):
        if (int(str(x[9].split(":")[0])) > 12):
            x[9] = str(datetime.timedelta(hours=int(int(str(x[9].split(":")[0])) - 12),minutes=int(str(x[9].split(":")[1])))) + " pm"
        else:
            x[9] =  x[9] + " am"

while(True):
    userResponse = input()
    if(userResponse == "q"):
        print("goodbye")
        break
    elif(userResponse.isdigit()):
        if(int(userResponse) > 0 and int(userResponse) <= len(deliveryInfo) and deliveryInfo[int(userResponse)] != None):
            print("ID, Address, City, State, Weight(KILO), Delivery Deadline, Special Note, Status, Miles, Delivered")

            deliveryInfo[int(userResponse)][7] = "delivered"
            for x in deliveryInfo[int(userResponse)]:
                print(x, end=", ")
        else:
            print("error, package not found")
    elif(userResponse == "a"):
        for x in deliveryInfo:
            if(x != None):
                x[7] = "delivered"
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
                    elif(x[10] == truck1.truckID and startTime <= truck1.timeDeployed):
                        x[7] = "at hub"
                        print(x)
                    elif(x[10] == truck2.truckID and startTime <= truck2.timeDeployed):
                        x[7] = "at hub"
                        print(x)
                    elif(x[10] == truck3.truckID and startTime <= truck3.timeDeployed):
                        x[7] = "at hub"
                        print(x)
                    else:
                        print(x)

    else:
        print("error, please enter another input")