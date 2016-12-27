import sys
import tkinter as tk
import tkinter.ttk as ttk

class State:
    def __init__(self, sname, stype, sparamlist):
        self.stname = sname
        self.sttype = stype
        self.stparamlist = sparamlist
    def __str__(self):
        return "<State> "+self.stname

class Screen:
    def __init__(self, name, data=""):
        self.scname = name
        self.scdata = data
    def appendData(self, data):
        self.scdata += data
    def __str__(self):
        return "<Screen> "+self.scname

class SType:
    def __init__(self, name, paramcount, paramlist):
        self.name = name
        self.paramcount = paramcount
        self.paramlist = paramlist
    def __str__(self):
        return "<SType> " + self.name

class StateTable:
    def __init__(self):
        self.ptype = ('number', 'screen', 'state')
        self.stype = dict()
        #Add only <State> to the list
        self.stateList = dict()
        #Add only <Screen> to the list
        self.screenList = list()
    def addScreenToList(self, scr):
        self.screenList.append(scr)
    def addTypeToList(self, styp):
        self.stype[styp.name] = styp
    def addStateToList(self, state):
        self.stateList[state.stname] = state

class ScreenGUI:
    FWIDTH = 20
    FHEIGHT = 20
    LabelArray = [[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None], \
        ]
    def __init__(self, screen):
        self.name = screen.scname
        self.data = screen.scdata
        self.clearScreen()
        self.cursor = [ 0, 0]
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.clearScreen()
        self.cursor = [0,0]
    def clearScreen(self):
        self.screenbuf = [['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
                ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''], \
            ]
    def addText(self, text, row, col):
        for s in text:
            if row < 16 and col < 32 :
                self.screenbuf[row][col] = s
            col+=1
    """def addText(self, text):
        self.addText(self.cursor[0], self.cursor[1], text)"""
    def setCursor(self, row, col):
        self.cursor = [row, col]
    def DisplayText(self,parent, buf):
        for i in range(16):
            for j in range(32):
                temp = tk.Label(parent, fg='white', width=1, text=buf[i][j],bg='black')
                temp.place(x = (j * self.FWIDTH), y = (i * self.FHEIGHT), width = self.FWIDTH, height = self.FHEIGHT)
                #temp.pack()
                self.LabelArray[i][j] = temp
    def showScreen(self):
        view = tk.Tk()
        view.title(self.name)
        self.DisplayText(view, self.screenbuf)
        view.geometry(str(self.FWIDTH*32)+"x"+str(self.FHEIGHT*16))
        view.mainloop()
    def processData(self):
        print('Generating Screen:', self.name)
        #print('Screen Data:', self.data)
        d = self.data
        head = 0
        length = len(d)
        command = ""
        while head < length:
            if d[head] == "@":
                head += 1
                command = d[head:head+2]
                head += 2
            else:
                #head += 1
                if head < length:
                    s = d[head]
                    text = ''
                    while s != '@':
                        text += s
                        head += 1
                        if head >= length:
                            break
                        else:
                            s = d[head]
                    self.addText(text, self.cursor[0], self.cursor[1])
                    continue
            #print("Command :", command)
            if command == "FF":
                self.clearScreen()
            elif command == "SI":
                #print("unparsed:", d[head:])
                #print("Row:", d[head:head+2])
                row = int(d[head:head+2])
                head += 2
                col = int(d[head:head+2])
                head += 2
                self.setCursor(row, col)
            elif command == "CS":
                head += 1
                if head < length:
                    s = d[head]
                    text = ''
                    while s != '@':
                        text += s
                        head += 1
                        if head >= length:
                            break
                        else:
                            s = d[head]
                    self.addText(text, self.cursor[0], self.cursor[1])
            else:
                s = d[head]
                while s != '@':
                    head += 1
                    if head >= length:
                        break
                    else:
                        s = d[head]
                #head += 1
                """if head < length:
                    s = d[head]
                    text = ''
                    while s != '@':
                        text += s
                        head += 1
                        if head >= length:
                            break
                        else:
                            s = d[head]
                    self.addText(text, self.cursor[0], self.cursor[1])"""
        self.showScreen()

filestack = []
curfd = None
curSegment = None
statetable = None
terminatorList = {'config' : 'end', 'timer_def' : 'end', \
            'misc_config_data' : 'end', 'enhanced_params_def' : 'end', \
            'screen_def' : 'end_screen_def', 'state_def' : 'end', \
            'state_table' : 'end', 'host_state_def' : 'end', \
            'oar_def' : 'end'
            }
segmentList = ('config', 'timer_def', 'misc_config_data', 'enhanced_params_def', 'screen_def', 'state_def', 'state_table', 'host_state_def', 'oar_def')
curScreen = None
stateCount = 0
stypeCount = 0
screenCount = 0
printed = None

RED   = "\033[0;31m"
BLUE  = "\033[0;34m"
CYAN  = "\033[0;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"

def filestackTest():
    global filestack
    for a in filestack:
        print(str(a))

def openFile(filename):
    fd = open(filename, 'r')
    #filestack.append(fd)
    return fd

def popFile():
    global filestack
    fd = filestack[-1]
    if fd != None:
        close(fd)
"""
def getLine():
    global filestack, curfd
    line = curfd.readline()
    if filestack[-1] != None:
        fd = filestack[-1]
    else:
        return -1
    line = getLine
"""
def setSegment(line):
    global curSegment, segmentList
    for seg in segmentList:
        if seg == line.lower():
            curSegment = seg

def isTerminator(line):
    global terminatorList, curSegment
    if terminatorList[curSegment] == line.lower():
        return True
    return False

def newScreen(name):
    global curScreen
    scr = Screen(name)
    curScreen = scr
    #print('Added Screen [' + name + ']')

def addScreen():
    global curScreen, statetable, screenCount
    if curScreen is not None:
        statetable.addScreenToList(curScreen)
        screenCount += 1
        curScreen = None
    else:
        print("Error: Current screen is none. Cannot Add.")

def addScreenData(data):
    global curScreen
    if curScreen is not None:
        curScreen.appendData(data)
    else:
        print("Error: Current screen is none. Cannot Add data.")

def processScreen(line):
    global curScreen
    temp = line.lower()
    if temp.find('screen:') == 0:
        temp = temp.replace('screen:','').strip()
        newScreen(temp)
    elif temp == 'end':
        addScreen()
    else:
        addScreenData(line)

def processType(line):
    #line = processLine(line)
    global statetable, stypeCount
    #print('processing: [' + line + ']')
    line = line.split()
    styp = SType(line[0], line[1], line[2:])
    statetable.addTypeToList(styp)
    stypeCount += 1
    #print("Added StateType[", styp.name, "].")

def processState(line):
    global statetable, stateCount
    line = line.split()
    state = State(line[0], line[1], line[2:])
    statetable.addStateToList(state)
    #print("Added State[", state.stname, "].")
    stateCount += 1

def process(line):
    global curSegment
    if curSegment == None:
        setSegment(line)
    elif isTerminator(line):
        curSegment = None
        return
    else:
        if curSegment == 'screen_def':
            processScreen(line)
        elif curSegment == 'state_def':
            processType(line)
        elif curSegment == 'state_table':
            processState(line)
        """
        elif curSegment == 'host_state_def':
            processScreen(line)
        elif curSegment == 'config':
            processScreen(line)
        elif curSegment == 'oar_def':
            processScreen(line)
        elif curSegment == 'timer_def':
            processScreen(line)
        elif curSegment == 'enhanced_params_def':
            processScreen(line)"""

def __main__():
    global filestack, curfd, curSegment, statetable
    f = "state.tbl"
    curfd = openFile(f)
    statetable = StateTable()
    #statetable.
    #while line = getLine() != -1:
    for line in curfd:
        line = line.strip()
        if line != '':
            if line[0] != '#':
                if line[-1] == '\\':
                    while line[-1] == '\\':
                        line = line.replace('\\', '')
                        line += curfd.readline().strip()
                #process line here
                #print(line)
                process(line)
    curfd.close()
    print("Parsing sucessful!")

#print(statetable.stateList.values())

def writeToCSV(name):
    global statetable
    fd = open(name, "w")
    fd.write("State Type List\n")
    for stype in statetable.stype.values():
        fd.write(stype.name + ',' + stype.paramcount )
        for p in stype.paramlist:
            fd.write(',' + p)
        fd.write('\n\n\n')
    fd.write("Screens list\n\n")
    for scr in statetable.screenList:
        fd.write(scr.scname + ',' + scr.scdata + '\n\n\n')
    fd.write("States List\n\n")
    for state in statetable.stateList.values():
        fd.write(state.stname + ',' + state.sttype)
        for p in state.stparamlist:
            fd.write(',' + p)
        fd.write('\n')
    fd.close()
__main__()
#filestackTest()
#writeToCSV("statetable.csv")
print("Screen Count :", screenCount)
print("SType Count :", stypeCount)
print("States Count :", stateCount)

def getRootState():
    global statetable
    for state in statetable.stateList:
        if statetable.stateList[state].sttype == "A":
            return statetable.stateList[state]
    return None

def createViewer(name, data):
    s = ScreenGUI(name, data)
    #s = ScreenGUI("scr","@SO670@ES[060z@SO671@ES[060z@SO672@ES[060z@SO679@ES[020z@SO674@ES[060z@SO675@ES[060z@SO679@ES[020z@SO676@ES[060z@SO677@ES[060z@SO678@ES[060z@SO679@ES[020z")

    s.processData()


class Begueradj(tk.Frame):
    '''
    classdocs
    '''
    global statetable
    def __init__(self, parent):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize_user_interface()

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("Canvas Test")
        self.parent.grid_rowconfigure(1,weight=1)
        self.parent.grid_columnconfigure(1,weight=1)
        self.parent.config(background="lavender")


        # Define the different GUI widgets
        #self.dose_label = tk.Label(self.parent, text = "Dose:")
        #self.dose_entry = tk.Entry(self.parent)
        #self.dose_label.grid(row = 0, column = 0, sticky = tk.W)
        #self.dose_entry.grid(row = 0, column = 1)

        #self.modified_label = tk.Label(self.parent, text = "Date Modified:")
        #self.modified_entry = tk.Entry(self.parent)
        #self.modified_label.grid(row = 1, column = 0, sticky = tk.W)
        #self.modified_entry.grid(row = 1, column = 1)

        #self.submit_button = tk.Button(self.parent, text = "Insert", command = self.insert_data)
        #self.submit_button.grid(row = 2, column = 1, sticky = tk.W)
        #self.exit_button = tk.Button(self.parent, text = "Exit", command = self.parent.quit)
        #self.exit_button.grid(row = 0, column = 3)

        # Set the treeview
        self.tree = ttk.Treeview( self.parent)
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)
        self.tree.heading('#0', text='State Table Tree View')
        #self.tree.heading('#1', text='Dose')
        #self.tree.heading('#2', text='Modification Date')
        #self.tree.column('#1', stretch=tk.YES)
        #self.tree.column('#2', stretch=tk.YES)
        self.tree.column('#0', stretch=tk.YES, minwidth=500, width=700)
        #self.tree.grid(row=1, sticky='nsew')
        self.treeview = self.tree

        self.tree.tag_configure('number', foreground='brown')
        self.tree.tag_configure('screen', foreground='green')
        self.tree.tag_configure('state', foreground='blue')
        self.tree.tag_configure('undefined', foreground='red')

        self.tree.bind("<Double-1>", self.OnDoubleClick)
        # Initialize the counter
        self.i = 0


    def insert_data(self, parent, name, level, tag):
        """
        Insertion method.
        """
        #print("inserting " + name + " to " + str(parent))
        if parent == 'root':
            id1 = self.treeview.insert(parent='', index=0, text=str(name), tags=('state'))
            #print(id1)
        else:
            id1 = self.treeview.insert(parent=parent, index='end',text=str(name), tags=(tag))


        # Increment counter
        self.i = self.i + 1
        return id1

    """def doubleClick_Screen(self, event):
        self.tree"""
    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        if self.tree.item(item, "tags")[0] == "screen":
            scr_name = self.tree.item(item,"text")
            for scr in statetable.screenList:
                if scr.scname == scr_name:
                    createViewer(scr_name, scr.scdata)
            #print("you clicked on", self.tree.item(item,"tags"))


def printLevel(level):
    temp = ''
    for i in range(level - 1):
        temp += '|   '
    if level != 0:
        temp += '|___'
    return temp

def printBlue(app, parent, text, level):
    global BLUE,RESET
    #print(printLevel(level) + BLUE + text + RESET)
    #print(printLevel(level) + text)
    return app.insert_data(parent, text,level, 'state')

def printRed(app, parent, text, level):
    global RED,RESET
    #print(printLevel(level) + RED + text + RESET)
    #print(printLevel(level) + text)
    return app.insert_data(parent, text,level, 'undefined')

def printYellow(app, parent, text,level):
    global CYAN,RESET
    #print(printLevel(level) + CYAN + text + RESET)
    #print(printLevel(level) + text)
    return app.insert_data(parent, text,level, 'number')

def printGreen(app, parent, text, level):
    global GREEN, RESET
    #print(printLevel(level) + GREEN + text + RESET)
    #print(printLevel(level) + text)
    return app.insert_data(parent, text, level, 'screen')

def printRoot(app, text, level):
    global GREEN, RESET
    #print(printLevel(level) + GREEN + text + RESET)
    #print(printLevel(level) + text)
    return app.insert_data('root', text, level, 'state')

def markPrinted(name):
    global printed
    printed[name] = 1

def printState(app, parent, state, level):
    global statetable, printed
    temp = None
    types = None
    params = None
    try:
        types = statetable.stype[state.sttype].paramlist
        i = 0
        for p in state.stparamlist:
            printed[state.stname] = True
            if types[i] == 'state':
                try:
                    temp = printed[p]
                    #for "state_name (state type)"
                    tp = p + " (" + statetable.stateList[p].sttype + ")"
                    pid = printBlue(app, parent, tp, level + 1)
                    if str(state).lower != "null":
                        if not printed[p]:
                            printState(app, pid, statetable.stateList[p], level + 1)
                except KeyError:
                    #printLevel(level + 1)
                    printRed(app, parent, p, level + 1)
                #printBlue(p)
            elif types[i] == 'number':
                #printLevel(level + 1)

                printYellow(app, parent, p, level + 1)
            elif types[i] == 'screen':
                #printLevel(level + 1)
                printGreen(app, parent, p, level + 1)
            i += 1

    except:
        printRed(app, parent, 'Exception', 0)
        raise
        return

def printStateTable(app):
    global statetable, printed
    level=0
    printed = dict()
    for s in statetable.stateList:
        printed[s] = False
    root = getRootState()
    parent = printRoot(app, root.stname + " (" + root.sttype + ")", level)
    #parent = printRoot(app, root.stname, level)
    if root is not None:
        printState(app, parent, root, level)
        #printLevel(level)
print("Generating CSV...")
writeToCSV("statetable.csv")
print("Invoking GUI...")
root = tk.Tk()
d = Begueradj(root)
#d=0
printStateTable(d)
root.mainloop()
