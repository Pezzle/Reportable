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
    rRef["Overall"] = []
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
                rRef[currentKey]["Overall"] = []
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

def LoadReference(rRef):
    #open the file
    file = open("test.txt",'r')
    #format looks like:
    '''
    '1. Chapter One', (optional Description)
        1.1 SubChapter
            (Optional Description)
        1.2 SubChapter, (...)
        

    '''
    currentTitle = ""
    currentDescription = ""
    currentIndex = ""
    line = file.readline();
    line = line.strip();
    depth = 0
    prevID = [""]
    currentSubChapter = ""
    while(line != ""):
        #first determine if the line is a Chapter/SubChapter or a description
        #until we have seen a Chapter/SubChapter disregard any text
        lineList = line.split()
        #now reconstitute it
        secondaryLine = ""
        for item in lineList[1:]:
            secondaryLine += item + " "
        title = secondaryLine.split(",")[0]
        secondaryLine = secondaryLine.split(",")[1:]
        description = ""
        for item in secondaryLine:
            description += item.strip() + ", "
        description = description[:-2]
        indexID = lineList[0]
        ID = re.findall(r'([0-9]+(.)*)+', indexID)
        #if ID == "" then it is a description
        isDescription = True
        if(len(ID) != 0):
            isDescription = False
        #then if it isnt we need to figure out if it is a continuation of the current chapter's subchapters or
        #whether it is a new chapter
        isSub = False
        if(not isDescription):
            if(prevID[0] == ""):
                print "First Chapter"
                currentTitle = title
                currentDescription = description
                rRef[currentTitle]["Description"] = description
                rRef[currentTitle] = {}
                #we know its the FIRST chapter
                depth = 1
            else:
                if(len(prevID[0][0]) < len(ID[0][0])):
                    print "A New SubChapter"
                    depth = 2
                    currentDescription = ""
                    currentSubChapter = title
                    rRef[currentTitle][title] = currentDescription
                if(len(prevID[0][0]) == len(ID[0][0])):
                    print "A Continuation of the current chapter"
                    currentDescription = ""
                    rRef[currentTitle][title] = currentDescription
                    currentSubChapter = title
                if(len(prevID[0][0]) > len(ID[0][0])):
                    depth = 1
                    print "A new Chapter"
                    currentDescription = ""
                    currentTitle = title
                    currentDescription = description
                    rRef[currentTitle]["Description"] = description
                    rRef[currentTitle] = {}
            prevID = ID
        else:
            print "More description"
            if(depth == 1):
                rRef[currentTitle]["Description"] = rRef[currentTitle]["Description"] + "\n" + line
            if(depth == 2):
                rRef[currentTitle][currentSubChapter] = rRef[currentTitle][currentSubChapter] + "\n" + line
            #append it to the Chapters description
        line = (file.readline()).strip()

        #eg: simply if IDprev vs IDnew, if IDnew is longer then it is a subchapter of the current chapter
        #if it is the same then it is a continuation
        #if it is shorter then its a new chapter
        #if(


#def BuildMenu(hash, parentMenu,

mySyllabus = {}

BeginRecursiveFill(mySyllabus)


top = Tkinter.Tk()


def Hello():
    print "Hello"

# Code to add widgets will go here...


#first lets test out how to fill this form out
mb=  Menubutton ( top, text="Chapter:", relief=RAISED )
mb.grid()
mb.menu  =  Menu ( mb, tearoff = 0 )
mb["menu"]  =  mb.menu
    
mb1 = Menu ( mb.menu, tearoff = 0 )
mb1.add_command(label = "first's Command", command = Hello())
mb.menu.add_cascade(label = "first", menu = mb1)
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