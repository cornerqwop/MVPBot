import datetime
import re

class MVP():
    tombCoords = [0, 0]
    timeKilled = -1
    respawnTime = -1

    def __init__(self, name, spawnMap, respawnRate, weakTo=""):
        self.name = name
        self.spawnMap = spawnMap
        self.respawnRate = respawnRate
        self.weakTo = weakTo

    def setState(self, tombCoords, timeKilled):
        self.tombCoords = tombCoords
        self.timeKilled = timeKilled
        self.respawnTime = self.timeKilled + self.respawnRate * minute
        print("UPDATED: " + self.name + "\nTO: " + timeKilled)

class MVPList():

    mvps = {}
    timesCache = {}

    def __init__(self):
        pass

    def push(self, mvp): # adds mvp to list
        if mvp.name in self.mvps:
            last = self.mvps[mvp.name]
            lastTomb = last.tombCoords
            lastKilled = last.timeKilled
        self.mvps[mvp.name] = mvp

    def pop(self, mvp): # removes mvp from list
        if mvp.name in self.mvps:
            del self.mvps[mvp.name]

    def get(self, mvpName): # gets state for mvp
        if mvpName not in self.mvps:
            return -1

        return self.mvps[mvpName]

    def nextUp(self): # gets the next up mvp
        sortedTimes = sorted(self.timesCache)
        now = currentTime()
        for i in sortedTimes:
            if now < i:
                return self.mvps[self.timesCache[i]]
            elif now - hour > i:
                del self.timesCache[i]
        return -1
    
    def setMVP(self, mvpName, tombCoords, timeKilled): # set state for an MVP. timeKilled is in 'hh:mm' string format, utc
        if mvpName not in self.mvps:
            return -1
        if not re.match('([1-9]+:[1-9]+})', timeKilled):
            return -1
        
        t = timeKilled.split(':')
        toSet = currentTime().replace(hour = t[0], minute = t[1])
        if currentTime() < toSet + 3 * minute: # 3 minutes of leniency
            toSet = toSet - day
        self.mvps[mvpName].setState(tombCoords, toSet)
    
    def clean(self): # deletes out of date items
        sortedTimes = sorted(timesCache)
        now = currentTime()
        for i in sortedTimes:
            if now - hour > i:
                del self.timesCache[i]

    def printAll(self):
        tempstring  = ""
        for x in self.mvps:
            tempstring += "NAME: " + self.mvps[x].name + "\nSPAWNMAP: " + self.mvps[x].spawnMap + "\nRespawn Rate: " + str(self.mvps[x].respawnRate) + "\nWeak To: " + self.mvps[x].weakTo
            tempstring += "\nTomb Coords: " + str(self.mvps[x].tombCoords) + "\nTime Killed: " + str(self.mvps[x].timeKilled) + "\nRespawn Time: " + str(self.mvps[x].respawnTime)
            tempstring += "\n\n"
        return tempstring

    def printMVP(self, MVP):
        if MVP != -1:
            tempstring = ""
            tempstring += "NAME: " + MVP.name + "\nSpawn Map: " + MVP.spawnMap + "\nRespawn Time: " + str(MVP.respawnTime) + "\nWeak To: " + MVP.weakTo
            tempstring += "\n\n"
            return tempstring
        else:
            return "MVP Not Found"
        
minute = datetime.timedelta(seconds = 60)
hour = 60 * minute
day = 24 * hour

def currentTime():
    return datetime.datetime.utcnow()