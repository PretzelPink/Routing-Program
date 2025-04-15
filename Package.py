class package:

    def __init__(self, iD, dlvryTime, addrs, cty, zipCd, wgt, note=""):
        self.ID = iD
        self.address = addrs
        self.city = cty
        self.zipCode = zipCd
        self.weight = wgt
        self.deadline = dlvryTime
        self.specialNote = note
        self.timeDelivered = 0

    def __str__(self):
        packageString = ""
        packageString += str(self.ID) + "," + self.address + "," + self.city + "," + self.zipCode + "," + self.weight + "," + self.deadline + "," + self.specialNote + "," + "at hub"
        return (packageString)
