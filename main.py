#main.py, Student Id: xxxxxx

import csv
from operator import contains

import Package
import Truck
import HashMapper
import datetime

#instantiation of non library hashmap class
packageHashTable = HashMapper.ChainingHashTable()

#instantiation of base time, delivery info list and idlist for later use
IDList = []
time = datetime.timedelta(hours=int(8), minutes=int(0))
deliveryInfo = [None] * 41

with open('WGUPS Package File - Sheet1.csv', newline='') as packageInfo:
    packageFile = csv.reader(packageInfo)

    #O(n), iterates packageFile to extract package data in preparation for truck loading
    for x in packageFile:
        pack = Package.package(x[0],x[5],x[1],x[2],x[3], x[6], x[7]) #instantiates new Package class with provided csv package data
        IDList.append(x[0]) #adds each package id (x[0] == package id), to IDList for iterating each package by ID
        packageHashTable.insert(x[0], pack) #populates hashtable with package objects via ID

#O(n), helper function, takes truck object, fulfills entire route
def startTruckDeliveries(truck):
    global time
    while (True):
        #while packages exist, continue route
        if(len(truck.packages) > 0):
            packInfo = (truck.deliverPackage())
            processedInfo = packInfo.split(",")
            #add time to deliver package to base (time) variable
            time += (datetime.timedelta(hours=int(0),minutes=int(str(packInfo.split(",")[9]).split(":")[1])))
            #sets (processedInfo[9] == route time) to time (current time + route time == time delivered)
            #workaround due to timedelta generating additional time context ex: (1 day, 01:20:00)
            processedInfo[9] = str(time)
            deliveryInfo[int(str(packInfo).split(",")[0])] = processedInfo
        else:
            time += truck.backToHub()
            break

#instantiation of truck objects to be packed
truck1 = Truck.truck("truck1")
truck2 = Truck.truck("truck2")
truck3 = Truck.truck("truck3")


#manual loading of special note packages and packages with deadlines
#packages loaded in order to meet each requirement
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

#O(n), loads packages without notes or deadlines into open truck slots
for id in IDList:
    if((str(packageHashTable.search(id)).split(",")[6]) == "" and (str(packageHashTable.search(id)).split(",")[5]) == "EOD" and id != "19"):
        #truck1 loaded with 13 packages to allow more time for truck2 deadlines
        if(len(truck1.packages)<13):
            truck1.loadPackage(packageHashTable.search(id))
        elif(len(truck2.packages)<16):
            truck2.loadPackage(packageHashTable.search(id))
        else:
            truck3.loadPackage(packageHashTable.search(id))

#O(n), logging time deployed and starting truck route
#route does not end until all packages delivered
truck1.timeDeployed = time
startTruckDeliveries(truck1)

if(time >= (datetime.timedelta(hours=int(9),minutes=int(5)))):
    truck2.timeDeployed = time
    startTruckDeliveries(truck2)

if(truck1.atHub()):
    truck3.timeDeployed = time
    startTruckDeliveries(truck3)


#UI section of code, program data generation complete
print("Welcome To WGUPS\nPlese enter package ID to view package info or a to view all, t total mileage, or q to quit, or a time ex:'8:00 am' (enter) '9:00 am'\n")

#O(n), "fixes" x[9] time value to display pm values if time > 12:59
for x in deliveryInfo:
    if (x != None):
        if (int(str(x[9].split(":")[0])) > 12):
            x[9] = str(datetime.timedelta(hours=int(int(str(x[9].split(":")[0])) - 12),minutes=int(str(x[9].split(":")[1])))) + " pm"
        else:
            x[9] =  x[9] + " am"

#O(n^2), handles user input, q, t, a, #(number 1-40), 8:00 am-8:00 pm
while(True):
    userResponse = input()
    if(userResponse == "q"):
        print("goodbye")
        break
    #prints info of a single package
    elif(userResponse.isdigit()):
        #checks if digit within deliveryInfo, allows scaling for more packages
        if(int(userResponse) > 0 and int(userResponse) <= len(deliveryInfo) and deliveryInfo[int(userResponse)] != None):
            print("ID, Address, City, State, Weight(KILO), Delivery Deadline, Special Note, Status, Miles, Delivered")

            #O(n), sets package status to delivered, prints each component in x for readability
            deliveryInfo[int(userResponse)][7] = "delivered"
            for x in deliveryInfo[int(userResponse)]:
                print(x, end=", ")
        else:
            print("error, package not found")
    #O(n^2), prints all package information in deliveryInfo
    elif(userResponse == "a"):
        for x in deliveryInfo:
            if(x != None):
                x[7] = "delivered"
                for z in x:
                    print(z, end=", ")
                print("\n")
    #extracts miles traveled from each truck and prints to console
    elif(userResponse == "t"):
        print(str(round((truck1.milesTraveled + truck2.milesTraveled + truck3.milesTraveled), 2)) + " miles traveled")
        print("truck 1: miles traveled " + str(round(truck1.milesTraveled, 2)))
        print("truck 2: miles traveled " + str(round(truck2.milesTraveled, 2)))
        print("truck 3: miles traveled " + str(round(truck3.milesTraveled, 2)))

    #if user input time ex: 8:00, they can input a second endTime ex:9:00 to view packages during these times
    elif(":" in userResponse):
        startTime = datetime.timedelta(hours=int(int(userResponse.split(":")[0])), minutes=int(int(userResponse.split(":")[1][0:2])))
        if("pm" in userResponse):
            startTime += datetime.timedelta(hours=int(12), minutes=int(0))

        print("please enter end time")
        userResponse = input()
        endTime = datetime.timedelta(hours=int(int(userResponse.split(":")[0])),minutes=int(int(userResponse.split(":")[1][0:2])))
        if("pm" in userResponse):
            endTime += datetime.timedelta(hours=int(12), minutes=int(0))
        #O(n), input validation for times

        print("ID, Address, City, State, Weight(KILO), Delivery Deadline, Special Note, Status, Miles, Time Delivered")
        for x in deliveryInfo:
            if(x != None):
                timeDelivered = datetime.timedelta(hours=int(int(x[9].split(":")[0])),minutes=int(int(x[9].split(":")[1][0:2])))

                #checks each package against delivered time to determine status
                if(x[6] == "Wrong address listed" and startTime >= datetime.timedelta(hours=int(10),minutes=int(20))):
                    x[1] = "410 S State St"
                else:
                    x[1] = "300 State St"
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