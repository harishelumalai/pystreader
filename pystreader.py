import sys
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

def printLevel(level):
    temp = ''
    for i in range(level):
        temp += '\t'
    return temp

def printBlue(text, level):
    print(printLevel(level) + 'b[27m'+text)

def printRed(text, level):
    print(printLevel(level) + 'r[27m'+text)

def printYellow(text,level):
    print(printLevel(level) + 'y[27m'+text)

def printGreen(text, level):
    print(printLevel(level) + 'g[27m'+text)

def markPrinted(name):
    global printed
    printed[name] = 1

def printState(state, level):
    global statetable, printed
    temp = None
    types = None
    params = None
    try:
        types = statetable.stype[state.sttype].paramlist
        i = 0
        for p in state.stparamlist:
            if types[i] == 'state':
                try:
                    temp = printed[p]
                    #printLevel(level + 1)
                    printBlue(p, level + 1)
                    if not printed[p]:
                        printState(statetable.stateList[p], level + 1)
                except 'KeyError':
                    #printLevel(level + 1)
                    printRed(p, level + 1)
                #printBlue(p)
            elif types[i] == 'number':
                #printLevel(level + 1)
                printYellow(p, level + 1)
            elif types[i] == 'screen':
                #printLevel(level + 1)
                printGreen(p, level + 1)
            i += 1
        printed[state.stname] = True
    except:
        printRed('Exception', 0)
        #raise
        return

def printStateTable():
    global statetable, printed
    level=0
    printed = dict()
    for s in statetable.stateList:
        printed[s] = False
    root = getRootState()
    printBlue(root.stname, level)
    if root is not None:
        printState(root, level)
        printLevel(level)

printStateTable()
