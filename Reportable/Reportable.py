from Tkinter import *
import tkMessageBox
import Tkinter
from datetime import date
import re;

class Person:
    def __init__(self):
        self.FirstName = ""
        self.LastName = ""
        self.Progress = {}
        self.DOBm = -1
        self.DOBd = -1
        self.DOBy = -1
        self.ContactInfo = 0
    def UpdateDOB(day, month, year):
        self.DOBm = month
        self.DOBd = day
        self.DOBy = year

#use date.today() to get date;



def RecursiveFill(rRef, file, line, depth):
    position = 0
    while (line != ""):
        #lets figure out if it is a description.
        #split based on spaces
        line = line.strip()
        linesp = line.strip();
        spaceSplit = linesp.split()
        ID = re.findall(r'([0-9]+(.)*)+', spaceSplit[0])
        isDescription = False
        if(len(ID) == 0):
            isDescription = True
        if(isDescription):
            if(depth == 0):
                rRef["Description"].append(line)# wont work here
            else:
                rRef[currentKey]["Description"].append(line)#wont work here
        else:
            key = line.split(",")[0]
            if(depth == 0 or len(ID[0][0]) == depth):
                currentKey = key
                rRef[currentKey] = {}
                rRef[currentKey]["Description"] = []
                rRef[currentKey]["Notes"] = []
                depth = len(ID[0][0])
                if(line.split(",") > 1):
                    linesp = line.split(",")[1:]
                    desc = ""
                    for item in linesp:
                        desc += item + ", "
                        if(len(linesp) != 0):
                            desc = desc[:-2].strip()
                            if(desc[-1] != "."):
                                desc += "."
                            rRef[currentKey]["Description"].append(desc.strip())
                        #continue looping here
            else:
                if(len(ID[0][0]) > depth):
                    RecursiveFill(rRef[currentKey], file, line, depth)
                else:
                    file.seek(position)
                    return
                #we need to go down a level and pass the currentKey
        position = file.tell()
        line = file.readline();

def BeginRecursiveFill(rRef):
    #we need to open the file.
    file = open("test.txt",'r')
    line = "BEGIN"
    depth = 0
    rRef["Description"] = []
    rRef["Notes"] = []
    currentKey = ""
    while (line != ""):
        #lets figure out if it is a description.
        #split based on spaces
        line = file.readline();
        linesp = line.strip();
        spaceSplit = linesp.split()
        if(line == ""):
            return
        ID = re.findall(r'([0-9]+(.)*)+', spaceSplit[0])
        isDescription = False
        if(len(ID) == 0):
            isDescription = True
        if(isDescription):
            if(depth == 0):
                rRef["Description"].append(line.strip())
            else:
                rRef[currentKey]["Description"].append(line.strip())
        else:
            key = line.split(",")[0]
            if(depth == 0 or len(ID[0][0]) == depth):
                currentKey = key
                rRef[currentKey] = {}
                rRef[currentKey]["Description"] = []
                rRef[currentKey]["Notes"] = []
                depth = len(ID[0][0])
                if(line.split(",") > 1):
                    linesp = line.split(",")[1:]
                    desc = ""
                    if(len(linesp) != 0):
                        for item in linesp:
                            desc += item + ", "
                        desc = desc[:-2].strip()
                        if(desc[-1] != "."):
                            desc += "."
                        rRef[currentKey]["Description"].append(desc.strip())
                #continue looping here
            else:
                RecursiveFill(rRef[currentKey], file, line, depth + 1)
                #we need to go down a level and pass the currentKey

def BuildMenu(parentMenu, hash = {}, name = ""):
    #first we need to order it
    l = hash.keys()
    l.sort()
    for key in l:
        #create a button for keys: "Notes"
        if(key == "Notes"):
            parentMenu.add_command(label = key, command= lambda: myPrint(hash["Description"]))
            continue
        if(key == "Description"):
            continue
        #currentMenu = Menu ( parentMenu, tearoff = 0 )
        
        if(len(hash[key]) > 0):
            nextMenu = Menu ( parentMenu, tearoff = 0 )
            BuildMenu(nextMenu, hash[key], key)
            parentMenu.add_cascade(label = key, menu = nextMenu)

        #parentMenu.add_cascade(label = key, menu = currentMenu)
    
        


mySyllabus = {}

BeginRecursiveFill(mySyllabus)


top = Tkinter.Tk()


def myPrint(str):
    print str

# Code to add widgets will go here...


#first lets test out how to fill this form out
mb=  Menubutton ( top, text="Chapter:", relief=RAISED )
mb.grid()
mb.menu  =  Menu ( mb, tearoff = 0 )
mb["menu"]  =  mb.menu
    
BuildMenu(mb.menu, mySyllabus, "menu")


#mb1 = Menu ( mb.menu, tearoff = 0 )
#mb1.add_command(label = "first's Command", command = Hello())
#mb.menu.add_cascade(label = "first", menu = mb1)
#mayoVar  = IntVar()
#ketchVar = IntVar()

#mb.menu.add_checkbutton ( label="mayo",
#                          variable=mayoVar )
#mb.menu.add_checkbutton ( label="ketchup",
#                          variable=ketchVar )


mb.pack()
#chList = []
#for key in mySyllabus:
#    if(key != "Description"):
#        chList.append(key)
#chList.sort()
#for key in chList:
#    if(key != "Description"):
#        #lets add an item to the menu
#        currentMenu =  Menu ( mb.menu, tearoff = 0 )
#        mb.menu.add_command(label = key)

#we need to recursively build the menu from the ground up

top.mainloop()