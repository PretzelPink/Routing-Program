import csv

import Package
import Truck
import HashMapper


packageHashTable = HashMapper.ChainingHashTable()

IDList = []
addressList = []
time = 8.00 # 8:00 AM

with open("WGUPS Distance Table - Sheet1.csv", newline='') as packageInfo:
    i = 0
    packageFile = csv.reader(packageInfo)

    for x in packageFile:
        addressList.append(((x[1][1:x[1].find("(")]).strip("\n"), i))
        i += 1

with open('WGUPS Package File - Sheet1.csv', newline='') as packageInfo:
    packageFile = csv.reader(packageInfo)

    for x in packageFile:
        pack = Package.package(x[0],x[5],x[1],x[2],x[3], x[6], x[7])
        IDList.append(x[0])
        packageHashTable.insert(x[0], pack)


#print(findDistance(addressList[5][0], tempPackageList[6].address))

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

while(len(truck1.packages)):
    truck1.deliverPackage()