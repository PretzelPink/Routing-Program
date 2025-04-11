class package:

    ID=0
    address=""
    city=""
    zipCode=0
    weight=0
    status=""
    deliveryTime=0
    deadLine=0
    specialNote=""

    def __init__(self, iD, dlvryTime, addrs, cty, zipCd, wgt, note=""):
        self.ID = iD
        self.address = addrs
        self.city = cty
        self.zipCode = zipCd
        self.weight = wgt
        self.deadline = dlvryTime
        self.specialNote = note

    def stringify(self):
        packageString = ""

        packageString += str(self.ID) + "\n" + self.address

