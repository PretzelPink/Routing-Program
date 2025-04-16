class package:

    #package constructor, initiates all package csv data to variables, used line 22 (main.py)
    def __init__(self, iD, dlvryTime, addrs, cty, zipCd, wgt, note=""):
        self.ID = iD
        self.address = addrs
        self.city = cty
        self.zipCode = zipCd
        self.weight = wgt
        self.deadline = dlvryTime
        self.specialNote = note
        self.timeDelivered = 0

    #handles package string conversion to display all package information instead of a memory address
    def __str__(self):
        packageString = ""
        packageString += str(self.ID) + "," + self.address + "," + self.city + "," + self.zipCode + "," + self.weight + "," + self.deadline + "," + self.specialNote + "," + "at hub"
        return (packageString)
