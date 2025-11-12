# -*- coding: utf-8 -*-
"""
Created on Mon May 23 20:16:57 2022

@author: bendg
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import numpy as np
import math as math
import copy as copy
import random as random
letters = np.array(['A','B','C','D','E','F','G','H','I'])
#numbersnake
class numbersnakegrid(object):
    def __init__(self, nums):
        self.nums = nums
        #helper functions
    def finddistance(self, num1, num2):
        rowlength = np.sqrt(len(self.nums))
        row1 = num1//rowlength
        col1 = num1%rowlength
        row2 = num2//rowlength
        col2 = num2%rowlength
        distance = abs(row2-row1) + abs(col2-col1)
        return distance
    def findcoldistance(self, num1, num2):
        rowlength = np.sqrt(len(self.nums))
        col1 = num1%rowlength
        col2 = num2%rowlength
        coldistance = abs(col2-col1)
        return coldistance
    def findrowdistance(self, num1, num2):
        rowlength = np.sqrt(len(self.nums))
        row1 = num1//rowlength
        row2 = num2//rowlength
        rowdistance = abs(row2-row1)
        return rowdistance
    def samerow(self, num1, num2):
        rowlength = np.sqrt(len(self.nums))
        row1 = num1//rowlength
        row2 = num2//rowlength
        if(row1 == row2):
            return True
        else:
            return False
    def samecolumn(self, num1, num2):
        rowlength = np.sqrt(len(self.nums))
        col1 = num1%rowlength
        col2 = num2%rowlength
        if(col1 == col2):
            return True
        else:
            return False
    def findstepsaway(self,num1,num2):
        distance = int(self.finddistance(num1, num2))
        numdifference = self.nums[num2]-self.nums[num1]
        stepsaway = (numdifference - distance)/2
        return stepsaway
        #solving methods
    def oneawaypathexclusion(self):
        rowlength = int(np.sqrt(len(self.nums)))
        for i in range(len(self.nums)):
            if i in self.nums:
                location = self.nums.index(i)
                nextnumber = 0
                index = i+1
                while(nextnumber == 0):
                    if index in self.nums:
                        nextnumber = index
                        nextlocation = self.nums.index(nextnumber)
                        difference = nextnumber - i
                    else:
                        index += 1
                        if(index > len(self.nums)):
                            nextnumber = -1
                if(nextnumber != -1 and difference > 1):
                    distancebetween = int(self.finddistance(location, nextlocation))
                    stepsaway = int((difference - distancebetween)/2)
                    if(stepsaway == 1):
                        print(i)
                        print(nextnumber)
                        coldistance = int(self.findcoldistance(location, nextlocation))
                        rowdistance = int(self.findrowdistance(location, nextlocation))
                        paths1 = []
                        paths2 = []
                        pathdirections1 = []
                        pathdirections2 = []
                        path = []
                        path1 = []
                        path2 = []
                        numberofpaths1 = int(math.factorial(distancebetween+2) / (math.factorial(coldistance+1)*math.factorial(rowdistance)))
                        numberofpaths2 = int(math.factorial(distancebetween+2) / (math.factorial(coldistance)*math.factorial(rowdistance+1)))
                        for l in range(coldistance):
                            if(location%9 > nextlocation%9):
                                path.append("l")
                            else:
                                path.append("r")
                        for l in range(rowdistance):
                            if(location//9 > nextlocation//9):
                                path.append("u")
                            else:
                                path.append("d")
                        path1 = copy.deepcopy(path)
                        path2 = copy.deepcopy(path)
                        path1.append("l")
                        path1.append("r")
                        path2.append("u")
                        path2.append("d")
                        pathstring1 = ""
                        pathstring2 = ""
                        for n in range(distancebetween+2):
                            pathstring1 += path1[n]
                            pathstring2 += path2[n]
                        pathdirections1.append(pathstring1)
                        pathdirections2.append(pathstring2)
                        while(len(pathdirections1) < numberofpaths1):
                            newpath = []
                            orderlist = []
                            numberlist = []
                            for n in range(distancebetween+2):
                                numberlist.append(n)
                            while(len(numberlist) > 0):
                                randnum = random.randint(0, distancebetween+1)
                                if(randnum in numberlist):
                                    orderlist.append(randnum)
                                    numberlist.remove(randnum)
                            for n in range(distancebetween+2):
                                newpath.append(path1[orderlist[n]])
                            newpathstring = ""
                            for n in range(distancebetween+2):
                                newpathstring += newpath[n]
                            if(newpathstring not in pathdirections1):
                                pathdirections1.append(newpathstring)
                        for p in range(numberofpaths1):
                            currentnumber = location
                            pathnumbers1 = []
                            invalid = False
                            for d in range(distancebetween+2):
                                if(pathdirections1[p][d] == "l"):
                                    if(currentnumber%9 == 0):
                                        invalid = True
                                    currentnumber -= 1
                                    pathnumbers1.append(currentnumber)
                                if(pathdirections1[p][d] == "r"):
                                    if(currentnumber%9 == 8):
                                        invalid = True
                                    currentnumber += 1
                                    pathnumbers1.append(currentnumber)
                                if(pathdirections1[p][d] == "u"):
                                    if(currentnumber//9 == 0):
                                        invalid = True
                                    currentnumber -= 9
                                    pathnumbers1.append(currentnumber)
                                if(pathdirections1[p][d] == "d"):
                                    if(currentnumber//9 == 8):
                                        invalid = True
                                    currentnumber += 9
                                    pathnumbers1.append(currentnumber)
                            if not invalid:
                                paths1.append(pathnumbers1)
                        givens = []
                        for g in range(len(self.nums)):
                            if(self.nums[g] != 0 and g != nextlocation):
                                givens.append(g)
                        pathcopy1 = copy.deepcopy(paths1)
                        for pathlist in paths1:
                            invalid = False
                            for z in range(distancebetween+2):
                                if(pathlist[z] in givens):
                                    invalid = True
                            if(len(pathlist) != len(set(pathlist))):
                                invalid = True
                            if(invalid == True):
                                pathcopy1.remove(pathlist)
                        paths1 = pathcopy1
                        while(len(pathdirections2) < numberofpaths2):
                            newpath = []
                            orderlist = []
                            numberlist = []
                            for n in range(distancebetween+2):
                                numberlist.append(n)
                            while(len(numberlist) > 0):
                                randnum = random.randint(0, distancebetween+1)
                                if(randnum in numberlist):
                                    orderlist.append(randnum)
                                    numberlist.remove(randnum)
                            for n in range(distancebetween+2):
                                newpath.append(path2[orderlist[n]])
                            newpathstring = ""
                            for n in range(distancebetween+2):
                                newpathstring += newpath[n]
                            if(newpathstring not in pathdirections2):
                                pathdirections2.append(newpathstring)
                        for p in range(numberofpaths2):
                            currentnumber = location
                            pathnumbers2 = []
                            invalid = False
                            for d in range(distancebetween+2):
                                if(pathdirections2[p][d] == "l"):
                                    if(currentnumber%9 == 0):
                                        invalid = True
                                    currentnumber -= 1
                                    pathnumbers2.append(currentnumber)
                                if(pathdirections2[p][d] == "r"):
                                    if(currentnumber%9 == 8):
                                        invalid = True
                                    currentnumber += 1
                                    pathnumbers2.append(currentnumber)
                                if(pathdirections2[p][d] == "u"):
                                    if(currentnumber//9 == 0):
                                        invalid = True
                                    currentnumber -= 9
                                    pathnumbers2.append(currentnumber)
                                if(pathdirections2[p][d] == "d"):
                                    if(currentnumber//9 == 8):
                                        invalid = True
                                    currentnumber += 9
                                    pathnumbers2.append(currentnumber)
                            if not invalid:
                                paths2.append(pathnumbers2)
                        pathcopy2 = copy.deepcopy(paths2)
                        for pathlist in paths2:
                            invalid = False
                            for z in range(distancebetween):
                                if(pathlist[z] in givens):
                                    invalid = True
                            if(len(pathlist) != len(set(pathlist))):
                                invalid = True
                            if(invalid == True):
                                pathcopy2.remove(pathlist)
                        paths2 = pathcopy2
                        allpaths = paths1 + paths2
                        for loc in range(len(self.nums)):
                            if(self.nums[loc] == 0):
                                listofpossibleroutes = []
                                for b in range(len(self.nums)):
                                    if(b in self.nums):
                                        newlocation = self.nums.index(b)
                                        newnextnumber = 0
                                        newindex = b+1
                                        while(newnextnumber == 0):
                                            if newindex in self.nums:
                                                newnextnumber = newindex
                                                newnextlocation = self.nums.index(newnextnumber)
                                                difference = newnextnumber - b
                                            else:
                                                newindex += 1
                                                if(newindex > len(self.nums)):
                                                    newnextnumber = -1
                                        if(nextnumber != -1 and difference > 1):
                                            newstepsaway = (difference - self.finddistance(newlocation, newnextlocation))/2
                                            minimumaway = 0
                                            loccolumn = loc%9
                                            newloccolumn = newlocation%9
                                            nextloccolumn = newnextlocation%9
                                            locrow = loc//9
                                            newlocrow = newlocation//9
                                            nextlocrow = newnextlocation//9
                                            if(loccolumn > newloccolumn and loccolumn > nextloccolumn):
                                                minimumaway += min(loccolumn-newloccolumn, loccolumn-nextloccolumn)
                                            if(loccolumn < newloccolumn and loccolumn < nextloccolumn):
                                                minimumaway += min(newloccolumn-loccolumn, nextloccolumn-loccolumn)
                                            if(locrow > newlocrow and locrow > nextlocrow):
                                                minimumaway += min(locrow-newlocrow, locrow-nextlocrow)
                                            if(locrow < newlocrow and locrow < nextlocrow):
                                                minimumaway += min(newlocrow-locrow, nextlocrow-locrow) 
                                            if(minimumaway <= newstepsaway):
                                                listofpossibleroutes.append(newlocation)
                                if(len(listofpossibleroutes) == 1 and listofpossibleroutes[0] == location):
                                    print('cell ' + str(loc) + " can only be in the route starting at " + str(self.nums[location]))
                                    tempallpaths = copy.deepcopy(allpaths)
                                    for j in range(len(allpaths)):
                                        if loc not in allpaths[j]:
                                            tempallpaths.remove(allpaths[j])
                                    allpaths = tempallpaths
                        for spot in range(distancebetween+1):
                            same = True
                            samevalue = 0
                            for j in range(len(allpaths)):
                                if(samevalue == 0 or samevalue == allpaths[j][spot]):
                                    samevalue = allpaths[j][spot]
                                else:
                                    same = False
                            if(same):
                                print("found value by oneawaypathexclusion: " + str(i + 1 + spot))
                                self.nums[samevalue] = i + 1 + spot
                                
                            
                                              
        return
    def onepathleft(self):
        viablestarts = []
        viableends = []
        rowlength = int(np.sqrt(len(self.nums)))
        for i in range(len(self.nums)):
            if i in self.nums:
                location = self.nums.index(i)
                nextnumber = 0
                index = i+1
                while(nextnumber == 0):
                    if index in self.nums:
                        nextnumber = index
                        nextlocation = self.nums.index(nextnumber)
                        difference = nextnumber - i
                    else:
                        index += 1
                        if(index > len(self.nums)):
                            nextnumber = -1
                if(nextnumber != -1 and difference > 1):
                    viablestarts.append(location)
                    viableends.append(nextlocation)
        if(len(viablestarts) == 1):
            start = viablestarts[0]
            path = []
            paths = []
            for i in range(len(self.nums)):
                if(self.nums[i] == 0):
                    path.append(i)
            numberofpaths = math.factorial(len(path))
            iter = 0
            while(iter < 500):
                correctone = True
                iter += 1
                for j in range(len(path)):
                    if(j != 0):
                        if(abs(path[j] - path[j-1]) != 9 and abs(path[j] - path[j-1]) != 1):
                            correctone = False
                            if(j == 1):
                                temppath = []
                                numbers = []
                                numbersadded = []
                                for num in range(len(path)):
                                    numbers.append(num)
                                while(len(numbers) > 0):
                                    cunt = random.randint(0, len(path)-1)
                                    if(cunt not in numbersadded):
                                        numbersadded.append(cunt)
                                        numbers.remove(cunt)
                                for inum in range(len(path)):
                                    temppath.append(path[numbersadded[inum]])
                                path = temppath
                            elif(iter % 50 != 0):
                                temppath = copy.deepcopy(path)
                                temppath = path[0:j] + path[j+1:len(path)] + path[j:j+1]
                                path = temppath
                            else:
                                temppath = copy.deepcopy(path)
                                randomizer = random.randint(0,len(path)-1)
                                temppath = path[randomizer:len(path)] + path[0:randomizer]
                                path = temppath
                if(correctone):
                    for j in range(len(path)):
                        self.nums[path[j]] = self.nums[viablestarts[0]] + 1 + j
                        print("Cell " + str(path[j]) + " was in the last path, and its value is " + str(self.nums[viablestarts[0]] + 1 + j))
                    return
            if(numberofpaths < 1000):
                while(len(paths) < numberofpaths):
                    newpath = []
                    orderlist = []
                    numberlist = []
                    for n in range(len(path)):
                        numberlist.append(n)
                    while(len(numberlist) > 0):
                        randnum = random.randint(0, len(path)-1)
                        if(randnum in numberlist):
                            orderlist.append(randnum)
                            numberlist.remove(randnum)
                    for n in range(len(path)):
                        newpath.append(path[orderlist[n]])
                    if(newpath not in paths):
                        paths.append(newpath)
                path.append(nextlocation)
                for i in range(numberofpaths):
                    paths[i].append(nextlocation)
                for i in range(numberofpaths):
                    correctone = True
                    for j in range(len(path)):
                        if(j != 0):
                            if(abs(paths[i][j] - paths[i][j-1]) != 9 and abs(paths[i][j] - paths[i][j-1]) != 1):
                                correctone = False
                    if(correctone):
                        for j in range(len(path)-1):
                            self.nums[numberofpaths[i]] = self.nums[viablestarts[0]] + 1 + j
                            print("Cell " + str(numberofpaths[i]) + " was in the last path, and its value is " + str(self.nums[viablestarts[0]] + 1 + j))
                    return
    def straightlinesolve(self):
        rowlength = int(np.sqrt(len(self.nums)))
        for i in range(len(self.nums)):
            if i in self.nums:
                location = self.nums.index(i)
                nextnumber = 0
                index = i+1
                while(nextnumber == 0):
                    if index in self.nums:
                        nextnumber = index
                        nextlocation = self.nums.index(nextnumber)
                        difference = nextnumber - i
                    else:
                        index += 1
                        if(index > len(self.nums)):
                            nextnumber = -1
                if(nextnumber != -1 and difference > 1):
                    if(self.finddistance(location,nextlocation) == difference and (self.samerow(location, nextlocation))):
                        print('found a row example')
                        print(i)
                        print(nextnumber)
                        row = location//rowlength
                        col1 = location%rowlength
                        col2 = nextlocation%rowlength
                        if(col2 > col1):
                            for j in range(int(9*row + col1+1), int(9*row + col2)):
                                self.nums[j] = i + int(self.finddistance(location, j))
                        else:
                            for j in range(int(9*row + col2+1), int(9*row + col1)):
                                self.nums[j] = i + int(self.finddistance(location, j))
                    if(int(self.finddistance(location,nextlocation)) == difference and (self.samecolumn(location, nextlocation))):
                        col = location%rowlength
                        row1 = location//rowlength
                        row2 = nextlocation//rowlength
                        print('found a col example')
                        print(i)
                        print(nextnumber)
                        if(row2 > row1):
                            for j in range(row1+1, row2):
                                jindex = 9*j+col
                                self.nums[jindex] = i + int(self.finddistance(location, jindex))
                        else:
                            for j in range(row2+1, row1):
                                jindex = 9*j+col
                                self.nums[jindex] = i + int(self.finddistance(location, jindex))
        return
    def onedirection(self):
        rowlength = int(np.sqrt(len(self.nums)))
        for i in range(len(self.nums)):
            if(self.nums[i] != 0 and (self.nums[i]+1) not in self.nums):
                validoptions = []
                if(i >= rowlength and self.nums[i-9] == 0):
                    validoptions.append(i-9)
                if(i < len(self.nums)-rowlength and self.nums[i+9] == 0):
                    validoptions.append(i+9)
                if(i%rowlength != rowlength-1 and self.nums[i+1] == 0):
                    validoptions.append(i+1)
                if(i%rowlength != 0 and self.nums[i-1] == 0):
                    validoptions.append(i-1)
                if(len(validoptions) == 1 and self.nums[i] != 81):
                    print("found a number with only one direction available:")
                    self.nums[validoptions[0]] = self.nums[i] + 1
                    print(self.nums[validoptions[0]])
        return
    def onepathcell(self):
        rowlength = int(np.sqrt(len(self.nums)))
        for i in range(len(self.nums)):
            if(self.nums[i] != 0):
                validoptions = []
                if(i >= rowlength and self.nums[i-9] == 0):
                    validoptions.append(i-9)
                if(i < len(self.nums)-rowlength and self.nums[i+9] == 0):
                    validoptions.append(i+9)
                if(i%rowlength != rowlength-1 and self.nums[i+1] == 0):
                    validoptions.append(i+1)
                if(i%rowlength != 0 and self.nums[i-1] == 0):
                    validoptions.append(i-1)
                if(len(validoptions) == 1 and self.nums[i] != 81):
                    print("found a number with only one direction available:")
                    self.nums[validoptions[0]] = self.nums[i] + 1
                    print(self.nums[validoptions[0]])
        return
    def pathexclusion(self):
        rowlength = int(np.sqrt(len(self.nums)))
        for i in range(len(self.nums)):
            if i in self.nums:
                location = self.nums.index(i)
                nextnumber = 0
                index = i+1
                while(nextnumber == 0):
                    if index in self.nums:
                        nextnumber = index
                        nextlocation = self.nums.index(nextnumber)
                        difference = nextnumber - i
                    else:
                        index += 1
                        if(index > len(self.nums)):
                            nextnumber = -1
                if(nextnumber != -1 and difference > 1):
                    distancebetween = int(self.finddistance(location, nextlocation))
                    stepsaway = int((difference - distancebetween)/2)
                    if(stepsaway == 0):
                        coldistance = int(self.findcoldistance(location, nextlocation))
                        rowdistance = int(self.findrowdistance(location, nextlocation))
                        paths = []
                        pathdirections = []
                        path = []
                        numberofpaths = int(math.factorial(distancebetween) / (math.factorial(coldistance)*math.factorial(rowdistance)))
                        for l in range(coldistance):
                            if(location%9 > nextlocation%9):
                                path.append("l")
                            else:
                                path.append("r")
                        for l in range(rowdistance):
                            if(location//9 > nextlocation//9):
                                path.append("u")
                            else:
                                path.append("d")
                        pathstring = ""
                        for n in range(distancebetween):
                            pathstring += path[n]
                        pathdirections.append(pathstring)
                        while(len(pathdirections) < numberofpaths):
                            newpath = []
                            orderlist = []
                            numberlist = []
                            for n in range(distancebetween):
                                numberlist.append(n)
                            while(len(numberlist) > 0):
                                randnum = random.randint(0, distancebetween-1)
                                if(randnum in numberlist):
                                    orderlist.append(randnum)
                                    numberlist.remove(randnum)
                            for n in range(distancebetween):
                                newpath.append(path[orderlist[n]])
                            newpathstring = ""
                            for n in range(distancebetween):
                                newpathstring += newpath[n]
                            if(newpathstring not in pathdirections):
                                pathdirections.append(newpathstring)
                        for p in range(numberofpaths):
                            currentnumber = location
                            pathnumbers = []
                            for d in range(distancebetween):
                                if(pathdirections[p][d] == "l"):
                                    currentnumber -= 1
                                    pathnumbers.append(currentnumber)
                                if(pathdirections[p][d] == "r"):
                                    currentnumber += 1
                                    pathnumbers.append(currentnumber)
                                if(pathdirections[p][d] == "u"):
                                    currentnumber -= 9
                                    pathnumbers.append(currentnumber)
                                if(pathdirections[p][d] == "d"):
                                    currentnumber += 9
                                    pathnumbers.append(currentnumber)
                            paths.append(pathnumbers)
                        givens = []
                        for g in range(len(self.nums)):
                            if(self.nums[g] != 0 and g != nextlocation):
                                givens.append(g)
                        pathcopy = copy.deepcopy(paths)
                        for pathlist in paths:
                            invalid = False
                            for z in range(distancebetween):
                                if(pathlist[z] in givens):
                                    invalid = True
                            if(invalid == True):
                                pathcopy.remove(pathlist)
                        paths = pathcopy
                        print(paths)
                        for loc in range(len(self.nums)):
                            if(self.nums[loc] == 0):
                                listofpossibleroutes = []
                                for b in range(len(self.nums)):
                                    if(b in self.nums):
                                        newlocation = self.nums.index(b)
                                        newnextnumber = 0
                                        newindex = b+1
                                        while(newnextnumber == 0):
                                            if newindex in self.nums:
                                                newnextnumber = newindex
                                                newnextlocation = self.nums.index(newnextnumber)
                                                difference = newnextnumber - b
                                            else:
                                                newindex += 1
                                                if(newindex > len(self.nums)):
                                                    newnextnumber = -1
                                        if(nextnumber != -1 and difference > 1):
                                            newstepsaway = (difference - self.finddistance(newlocation, newnextlocation))/2
                                            minimumaway = 0
                                            loccolumn = loc%9
                                            newloccolumn = newlocation%9
                                            nextloccolumn = newnextlocation%9
                                            locrow = loc//9
                                            newlocrow = newlocation//9
                                            nextlocrow = newnextlocation//9
                                            if(loccolumn > newloccolumn and loccolumn > nextloccolumn):
                                                minimumaway += min(loccolumn-newloccolumn, loccolumn-nextloccolumn)
                                            if(loccolumn < newloccolumn and loccolumn < nextloccolumn):
                                                minimumaway += min(newloccolumn-loccolumn, nextloccolumn-loccolumn)
                                            if(locrow > newlocrow and locrow > nextlocrow):
                                                minimumaway += min(locrow-newlocrow, locrow-nextlocrow)
                                            if(locrow < newlocrow and locrow < nextlocrow):
                                                minimumaway += min(newlocrow-locrow, nextlocrow-locrow) 
                                            if(minimumaway <= newstepsaway):
                                                listofpossibleroutes.append(newlocation)
                                if(len(listofpossibleroutes) == 1 and listofpossibleroutes[0] == location):
                                    print('path exclusion: cell ' + str(loc) + " can only be in the route starting at " + str(self.nums[location]))
                                    temppaths = copy.deepcopy(paths)
                                    for j in range(len(paths)):
                                        if loc not in paths[j]:
                                            temppaths.remove(paths[j])
                                    paths = temppaths
                        numsinall = []
                        numsinallcopy = []
                        for p in range(len(paths)):
                            if(p == 0):
                                for x in range(distancebetween-1):
                                    numsinall.append(paths[0][x])
                                numsinallcopy = copy.deepcopy(numsinall)
                            else:
                                for x in numsinall:
                                    if(x not in paths[p]):
                                        if(x in numsinallcopy):
                                            numsinallcopy.remove(x)
                        numsinall = numsinallcopy
                        if(len(numsinall) != 0):
                            for shit in numsinall:
                                self.nums[shit] = i + int(self.finddistance(location, shit))
                                print('found a number with pathexclusion:')
                                print(self.nums[shit])                           
        return
#name class
class Name(object):
    def __init__(self, name):
        self.name = name
        self.number = 0
#initialize cell object
class Cell(object):
    def __init__(self,value):
        self.value = value
        self.order = 0
        if(self.value == 0):
            self.options = np.array([1,2,3,4,5,6,7,8,9])
            self.method = ''
            self.explain = 'none'
        else:
            self.options = np.array([value])
            self.method = 'given'
            self.explain = 'given'
    def removeOption(self,number,method,grid,explain):
        templist = np.ndarray.tolist(self.options)
        if(number in templist): 
            templist.remove(number)
            if(method == 'Check Cells'):
                self.explain = explain
                if(len(templist) == 1):
                    grid.methods.append(method)
                    self.method = method
                    self.value = templist[0]
                    grid.cellsSolved += 1
                    self.order = grid.cellsSolved
                    self.explain += 'so by process of elimination, this cell must contain ' + str(templist[0]) + '..'
            elif(len(templist) == 1):
                grid.methods.append(method)
                self.method = method
                self.value = templist[0]
                grid.cellsSolved += 1
                self.order = grid.cellsSolved
                self.explain = explain
        newOptions = np.asarray(templist)
        self.options = newOptions
# initialize sudoku grid object, this class contains all of the solving methods
class sudokuGrid(object):
    def __init__(self,cells):
        self.cells = cells
        self.guessNaked = 0
        self.cellsSolved = 0
        self.methods = []
    def adjacentNumbers(self, row1, col1, row2, col2):
        if(row1 == row2):
            if(col1 == col2):
                return False
            return True
        if(col1 == col2):
            if(row1 == row2):
                return False
            return True
        if((row1 // 3 == row2 // 3) and (col1 // 3 == col2 //3)):
            return True
        return False
    def isAdjacent(self,cell1,cell2):
        col1 = 0
        row1 = 0
        col2 = 0
        row2 = 0
        for x in range(9):
            for y in range(9):
                if(cell1 is self.cells[x][y]):
                    row1 = x
                    col1 = y
        for x in range(9):
            for y in range(9):
                if(cell2 is self.cells[x][y]):
                    row2 = x
                    col2 = y
        if(col1 == col2 and row1 == row2):
            return False
        if(col1 == col2 or row1 == row2 or ((3*(col1//3)) == (3*(col2//3)) and ((3*(row1//3)) == (3*(row2//3))))):
            return True
        return False
    def errorTest(self):
        for row in range(9):
            knowns = []
            for j in range(9):
                if(self.cells[row][j].value != 0):
                    if(self.cells[row][j].value in knowns):
                        return('error')
                    knowns.append(self.cells[row][j].value)
        for col in range(9):
            knowns = []
            for i in range(9):
                if(self.cells[i][col].value != 0):
                    if(self.cells[i][col].value in knowns):
                        return('error')
                    knowns.append(self.cells[i][col].value)  
        for x in range(9):
            knowns = []
            for r in range(3*(x//3), (3*(x//3) + 3)):
                for c in range(3*(x%3), 3*(x%3) + 3):
                    if(self.cells[r][c].value != 0):
                        if(self.cells[r][c].value in knowns):
                            return('error')
                        knowns.append(self.cells[r][c].value)  
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'    
    def checkCells(self):
        letters = np.array(['A','B','C','D','E','F','G','H','I'])
        for i in range(9):
            for j in range(9):
                adjacentNumber = 0
                adjacentCell = ""
                if(self.cells[i][j].value == 0):
                    for x in range(9):
                        for y in range(9):
                            if(self.cells[x][y] != self.cells[i][j]):
                                if(x == i or y == j or (i//3 == x//3 and j//3 == y//3)):
                                    if(self.cells[x][y].value != 0):
                                        adjacentCell = letters[x] + str(y+1)
                                        adjacentNumber = self.cells[x][y].value
                                        explain = self.cells[i][j].explain
                                        if(explain == 'none' or explain == 'given'):
                                            explain = ''
                                        explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                                        self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                                    
                    # for x in range(9):
                    #     if(self.cells[x][j].value in self.cells[i][j].options and x != i):
                    #         adjacentCell = letters[x] + str(j+1)
                    #         adjacentNumber = self.cells[x][j].value
                    #         explain = self.cells[i][j].explain
                    #         if(explain == 'none' or explain == 'given'):
                    #             explain = ''
                    #         explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #         self.cells[i][j].removeOption(self.cells[x][j].value,'Check Cells',self, explain)
                    # if(i < 3 and j < 3):
                    #     for x in range(3):
                    #         for y in range(3):
                    #             if(self.cells[x][y].value in self.cells[i][j].options and not(x == i and y == j)):
                    #                 adjacentCell = letters[x] + str(y+1)
                    #                 adjacentNumber = self.cells[x][y].value
                    #                 explain = self.cells[i][j].explain
                    #                 if(explain == 'none' or explain == 'given'):
                    #                     explain = ''
                    #                 explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #                 self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                    # if(i > 2 and i < 6 and j < 3):
                    #     for x in range(3,6):
                    #         for y in range(3):
                    #             if(self.cells[x][y].value in self.cells[i][j].options and not(x == i and y == j)):
                    #                 adjacentCell = letters[x] + str(y+1)
                    #                 adjacentNumber = self.cells[x][y].value
                    #                 explain = self.cells[i][j].explain
                    #                 if(explain == 'none' or explain == 'given'):
                    #                     explain = ''
                    #                 explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #                 self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                    # if(i > 5 and j < 3):
                    #     for x in range(6,9):
                    #         for y in range(3):
                    #             if(self.cells[x][y].value in self.cells[i][j].options and not(x == i and y == j)):
                    #                 adjacentCell = letters[x] + str(y+1)
                    #                 adjacentNumber = self.cells[x][y].value
                    #                 explain = self.cells[i][j].explain
                    #                 if(explain == 'none' or explain == 'given'):
                    #                     explain = ''
                    #                 explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #                 self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                    # if(i < 3 and j > 2 and j < 6):
                    #     for x in range(3):
                    #         for y in range(3,6):
                    #             if(self.cells[x][y].value in self.cells[i][j].options and not(x == i and y == j)):
                    #                 adjacentCell = letters[x] + str(y+1)
                    #                 adjacentNumber = self.cells[x][y].value
                    #                 explain = self.cells[i][j].explain
                    #                 if(explain == 'none' or explain == 'given'):
                    #                     explain = ''
                    #                 explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #                 self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                    # if(i > 2 and i < 6 and j > 2 and j < 6):
                    #     for x in range(3,6):
                    #         for y in range(3,6):
                    #             if(self.cells[x][y].value in self.cells[i][j].options and not(x == i and y == j)):
                    #                 adjacentCell = letters[x] + str(y+1)
                    #                 adjacentNumber = self.cells[x][y].value
                    #                 explain = self.cells[i][j].explain
                    #                 if(explain == 'none' or explain == 'given'):
                    #                     explain = ''
                    #                 explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #                 self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                    # if(i > 5 and j > 2 and j < 6):
                    #     for x in range(6,9):
                    #         for y in range(3,6):
                    #             if(self.cells[x][y].value in self.cells[i][j].options and not(x == i and y == j)):
                    #                 adjacentCell = letters[x] + str(y+1)
                    #                 adjacentNumber = self.cells[x][y].value
                    #                 explain = self.cells[i][j].explain
                    #                 if(explain == 'none' or explain == 'given'):
                    #                     explain = ''
                    #                 explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #                 self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                    # if(i < 3 and j > 5):
                    #     for x in range(3):
                    #         for y in range(6,9):
                    #             if(self.cells[x][y].value in self.cells[i][j].options and not(x == i and y == j)):
                    #                 adjacentCell = letters[x] + str(y+1)
                    #                 adjacentNumber = self.cells[x][y].value
                    #                 explain = self.cells[i][j].explain
                    #                 if(explain == 'none' or explain == 'given'):
                    #                     explain = ''
                    #                 explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #                 self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                    # if(i > 2 and i < 6 and j > 5):
                    #     for x in range(3,6):
                    #         for y in range(6,9):
                    #             if(self.cells[x][y].value in self.cells[i][j].options and not(x == i and y == j)):
                    #                 adjacentCell = letters[x] + str(y+1)
                    #                 adjacentNumber = self.cells[x][y].value
                    #                 explain = self.cells[i][j].explain
                    #                 if(explain == 'none' or explain == 'given'):
                    #                     explain = ''
                    #                 explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #                 self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                    # if(i > 5 and j > 5):
                    #     for x in range(6,9):
                    #         for y in range(6,9):
                    #             if(self.cells[x][y].value in self.cells[i][j].options and not(x == i and y == j)):
                    #                 adjacentCell = letters[x] + str(y+1)
                    #                 adjacentNumber = self.cells[x][y].value
                    #                 explain = self.cells[i][j].explain
                    #                 if(explain == 'none' or explain == 'given'):
                    #                     explain = ''
                    #                 explain += adjacentCell + ' contains ' + str(adjacentNumber) + ', '
                    #                 self.cells[i][j].removeOption(self.cells[x][y].value,'Check Cells',self, explain)
                    # if(self.cells[i][j].options.size == 1):
                    #     self.cells[i][j].value = self.cells[i][j].options[0]
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'    
    def checkBoxes(self):
        letters = np.array(['A','B','C','D','E','F','G','H','I'])
        for box in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            knowns = []
            emptycells = []
            for x in range(3*(box // 3), 3*(box // 3) + 3):
                for y in range(3*(box % 3), 3*(box % 3) + 3):
                    if(self.cells[x][y].value == 0):
                        emptycells.append(letters[x] + str(y + 1))
                    if(self.cells[x][y].value in unknowns):
                        unknowns.remove(self.cells[x][y].value)
                    if(self.cells[x][y].value in knowns and self.cells[x][y].value != 0):
                        return 'error'
                    knowns.append(self.cells[x][y].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                counter = 0
                i = 0
                j = 0
                value = unknownarr[u]
                for x in range(3*(box // 3), 3*(box // 3) + 3):
                    for y in range(3*(box % 3), 3*(box % 3) + 3):
                        if (value in self.cells[x][y].options):
                            counter += 1
                            i = x
                            j = y
                if(counter == 1):
                    cell = letters[i] + str(j + 1)
                    if(len(emptycells) == 1):
                        explain = cell + ' is the only unfilled cell in its box..'
                    else:
                        if(cell in emptycells):
                            emptycells.remove(cell)
                        emptystring = ""
                        for k in emptycells:
                            emptystring += k + ', '
                        emptystring = emptystring[0:len(emptystring) - 2]
                        explain = emptystring + ' cannot contain ' + str(value) + ', so ' + cell + ' is the only cell in its box that could contain ' + str(value) + '..'
                    for s in self.cells[i][j].options:
                        if(s != unknownarr[u]):
                            self.cells[i][j].removeOption(s,'Check Boxes',self, explain)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def checkRows(self):
        letters = np.array(['A','B','C','D','E','F','G','H','I'])
        for row in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            knowns = []
            emptycells = []
            for col in range(9):
                #eliminates all values already known
                if(self.cells[row][col].value == 0):
                    emptycells.append(letters[row] + str(col + 1))
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
                if(self.cells[row][col].value in knowns and self.cells[row][col].value != 0):
                    return 'error'
                knowns.append(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                counter = 0
                j = 0
                value = unknownarr[u]
                for col in range(9):
                    #tries to find an unused number with only one valid location
                    if (value in self.cells[row][col].options):
                        counter = counter + 1
                        j = col
                if(counter == 1):
                    cell = letters[row] + str(j + 1)
                    if(len(emptycells) == 1):
                        explain = cell + ' is the only unfilled cell in its row..'
                    else:
                        if(cell in emptycells):
                            emptycells.remove(cell)
                        emptystring = ""
                        for k in emptycells:
                            emptystring += k + ', '
                        emptystring = emptystring[0:len(emptystring) - 2]
                        explain = emptystring + ' cannot contain ' + str(value) + ', so ' + cell + ' is the only cell in its row that could contain ' + str(value) + '..'
                    for s in self.cells[row][j].options:
                        if(s != value):
                            self.cells[row][j].removeOption(s,'Check Rows',self, explain)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def checkColumns(self):
        letters = np.array(['A','B','C','D','E','F','G','H','I'])
        for col in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            knowns = []
            emptycells = []
            for row in range(9):
                if(self.cells[row][col].value == 0):
                    emptycells.append(letters[row] + str(col + 1))
                #eliminates all values already known
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
                if(self.cells[row][col].value in knowns and self.cells[row][col].value != 0):
                    return 'error'
                knowns.append(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                counter = 0
                i = 0
                value = unknownarr[u]
                for row in range(9):
                    #tries to find an unused number with only one valid location
                    if (value in self.cells[row][col].options):
                        counter = counter + 1
                        i = row
                if(counter == 1):
                    cell = letters[i] + str(col + 1)
                    if(len(emptycells) == 1):
                        explain = cell + ' is the only unfilled cell in its column..'
                    else:
                        if(cell in emptycells):
                            emptycells.remove(cell)
                        emptystring = ""
                        for k in emptycells:
                            emptystring += k + ', '
                        emptystring = emptystring[0:len(emptystring) - 2]
                        explain = emptystring + ' cannot contain ' + str(value) + ', so ' + cell + ' is the only cell in its column that could contain ' + str(value) + '..'
                    for s in self.cells[i][col].options:
                        if(s != value):
                            self.cells[i][col].removeOption(s,'Check Columns',self, explain)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def hiddenPairs(self):
        for row in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            for j in range(9):
                if(self.cells[row][j].value != 0):
                    print(self.cells[row][j].value)
                    unknowns.remove(self.cells[row][j].value)
            possibleCells = []
            for u in range(len(unknowns)):
                cols = ""
                for col in range(9):
                    if(unknowns[u] in self.cells[row][col].options):
                        cols += str(col)
                possibleCells.append(cols)
            for k in range(len(unknowns)):
                for l in range(k):
                    if(k != l and possibleCells[k] == possibleCells[l] and len(possibleCells[k]) == 2):
                        print('hidden pair!')
                        print(str(row) + ',' + str(possibleCells[k][0]))
                        print(self.cells[row][int(possibleCells[k][0])].options)
                        print(str(row) + ',' + str(possibleCells[k][1]))
                        print(self.cells[row][int(possibleCells[k][1])].options)
                        if(self.cells[row][int(possibleCells[k][0])].options.size != 2 or self.cells[row][int(possibleCells[k][1])].options.size != 2): 
                            self.cells[row][int(possibleCells[k])].options = np.array([unknowns[k],unknowns[l]])
                            self.cells[row][int(possibleCells[l])].options = np.array([unknowns[k],unknowns[l]])
                            for x in range(9):
                                for y in range(9):
                                    if (self.isAdjacent(self.cells[x][y],self.cells[row][int(possibleCells[k][0])]) and self.isAdjacent(self.cells[x][y],self.cells[row][int(possibleCells[k][1])])):
                                        self.cells[x][y].removeOption(unknowns[k],'Hidden Pairs',self,'hidden pairs')
                                        self.cells[x][y].removeOption(unknowns[l],'Hidden Pairs', self, 'hidden pairs')
        
        for col in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            for i in range(9):
                if(self.cells[i][col].value != 0):
                    unknowns.remove(self.cells[i][col].value)
            possibleCells = []
            for u in range(len(unknowns)):
                rows = ""
                for row in range(9):
                    if(unknowns[u] in self.cells[row][col].options):
                        rows += str(row)
                possibleCells.append(rows)
            for k in range(len(unknowns)):
                for l in range(k):
                    if(k != l and possibleCells[k] == possibleCells[l] and len(possibleCells[k]) == 2):
                        print('hidden pair!')
                        print(str(possibleCells[k][0]) + ',' + str(col))
                        print(self.cells[int(possibleCells[k][0])][col].options)
                        print(str(possibleCells[k][1]) + ',' + str(col))
                        print(self.cells[int(possibleCells[k][1])][col].options)
                        if(self.cells[int(possibleCells[k][0])][col].options.size != 2 or self.cells[int(possibleCells[k][1])][col].options.size != 2):   
                            for x in range(9):
                                for y in range(9):
                                    if (self.isAdjacent(self.cells[x][y],self.cells[int(possibleCells[k][0])][col]) and self.isAdjacent(self.cells[x][y],self.cells[int(possibleCells[k][1])][col])):
                                        self.cells[x][y].removeOption(unknowns[k],'Hidden Pairs',self, 'hidden pairs')
                                        self.cells[x][y].removeOption(unknowns[l],'Hidden Pairs',self, 'hidden pairs')
        
        for x in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            for row in range(3*(x//3),3*(x//3) + 3):
                for col in range(3*(x%3),3*(x%3)+3):
                    if(self.cells[row][col].value != 0):
                        unknowns.remove(self.cells[row][col].value)
            possibleCellRows = []
            possibleCellCols = []
            for u in range(len(unknowns)):
                rows = ""
                cols = ""
                for row in range(3*(x//3),3*(x//3) + 3):
                    for col in range(3*(x%3),3*(x%3)+3):
                        if(unknowns[u] in self.cells[row][col].options):
                            rows += str(row)
                            cols += str(col)
                possibleCellRows.append(rows)
                possibleCellCols.append(cols)
            for k in range(len(unknowns)):
                for l in range(k):
                    if(k != l and possibleCellRows[k] == possibleCellRows[l] and possibleCellCols[k] == possibleCellCols[l] and len(possibleCellRows[k]) == 2):
                        print('hidden pair!')
                        print(str(possibleCellRows[k][0]) + ',' + str(possibleCellCols[k][0]))
                        print(self.cells[int(possibleCellRows[k][0])][int(possibleCellCols[k][0])].options)
                        print(str(int(possibleCellRows[k][1])) + ',' + str(possibleCellCols[k][1]))
                        print(self.cells[int(possibleCellRows[k][1])][int(possibleCellCols[k][1])].options)
                        if(self.cells[int(possibleCellRows[k][0])][int(possibleCellCols[k][0])].options.size != 2 or self.cells[int(possibleCellRows[k][1])][int(possibleCellCols[k][1])].options.size != 2): 
                            possibleCells = [self.cells[int(possibleCellRows[k][0])][int(possibleCellCols[k][0])],self.cells[int(possibleCellRows[k][1])][int(possibleCellCols[k][1])]]
                            for x in range(9):
                                for y in range(9):
                                    if (self.isAdjacent(self.cells[x][y],self.cells[int(possibleCellRows[k][0])][int(possibleCellCols[k][0])]) and self.isAdjacent(self.cells[x][y],self.cells[int(possibleCellRows[k][1])][int(possibleCellCols[k][1])])):
                                        self.cells[x][y].removeOption(unknowns[k],'Hidden Pairs',self, 'hidden pairs')
                                        self.cells[x][y].removeOption(unknowns[l],'Hidden Pairs',self, 'hidden pairs')
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def nakedPairs(self):
        for i in range(9):
            for j in range(9):
                p = self.cells[i][j].options
                if(p.size == 2):
                    identicalBoxes = 1
                    vals = [j]
                    for col in range(9):
                        if(np.array_equal(self.cells[i][col].options,p) and col!=j):
                            identicalBoxes += 1
                            vals.append(col)
                    if(identicalBoxes == 2):
                        for col in range(9):
                            if not(col in vals):
                                candidateLeft = 0
                                candidates = 0
                                for number in self.cells[i][col].options:
                                    if number not in p:
                                        candidateLeft = number
                                        candidates+=1
                                explain = letters[i] + str(vals[0] + 1) + ' and ' + letters[i] + str(vals[1] + 1) + ' have only two candidates: ' + str(p[0]) + ' and ' + str(p[1]) + '. Therefore, ' + letters[i] + str(col + 1) + ' cannot contain ' + str(p[0]) + ' or ' + str(p[1]) + ', leaving only one candidate: ' + str(candidateLeft) + '..'
                                for x in range(p.size):
                                    self.cells[i][col].removeOption(p[x],'Naked Pairs',self, explain)
                                    if(self.cells[i][col].options.size == 0):
                                        return 'error'
                    identicalBoxes = 1
                    vals = [i]
                    for row in range(9):
                        if(np.array_equal(self.cells[row][j].options,p) and row!=i):
                            identicalBoxes += 1
                            vals.append(row)
                    if(identicalBoxes == 2):
                        for row in range(9):
                            if not(row in vals):
                                candidateLeft = 0
                                candidates = 0
                                for number in self.cells[row][j].options:
                                    if number not in p:
                                        candidateLeft = number
                                        candidates+=1
                                explain = letters[vals[0]] + str(j + 1) + ' and ' + letters[vals[1]] + str(j + 1) + ' have only two candidates: ' + str(p[0]) + ' and ' + str(p[1]) + '. Therefore, ' + letters[row] + str(j + 1) + ' cannot contain ' + str(p[0]) + ' or ' + str(p[1]) + ', leaving only one candidate: ' + str(candidateLeft) + '..'
                                for x in range(p.size):
                                    self.cells[row][j].removeOption(p[x],'Naked Pairs',self, explain)
                                    if(self.cells[row][j].options.size == 0):
                                        return 'error'
                    for box in range(9):
                        identicalBoxes = 1
                        rows = [i]
                        cols = [j]
                        if(3*(box//3) <= i < 3*(box//3) + 3 and 3*(box % 3) <= j < 3*(box % 3) + 3):
                            for l in range(3*(box//3), 3*(box//3) + 3):
                                for m in range(3*(box % 3), 3*(box % 3) + 3):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       rows.append(l)
                                       cols.append(m)
                            if(2 == identicalBoxes):
                                for x in range(3*(box//3), 3*(box//3) + 3):
                                     for y in range(3*(box % 3), 3*(box % 3) + 3):
                                         winner = False
                                         for index in range(len(rows)):
                                             if(x == rows[index]):
                                                 if(cols[index] == y):
                                                     winner = True
                                         if not (winner):
                                             candidateLeft = 0
                                             candidates = 0
                                             for number in self.cells[x][y].options:
                                                 if number not in p:
                                                     candidateLeft = number
                                                     candidates+=1
                                             explain = letters[rows[0]] + str(cols[0] + 1) + ' and ' + letters[int(rows[1])] + str(cols[1] + 1) + ' have only two candidates: ' + str(p[0]) + ' and ' + str(p[1]) + '. Therefore, ' + letters[x] + str(y + 1) + ' cannot contain ' + str(p[0]) + ' or ' + str(p[1]) + ', leaving only one candidate: ' + str(candidateLeft) + '..'
                                             for num in range(p.size):
                                                 self.cells[x][y].removeOption(p[num],'Naked Pairs',self, explain)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def boxReduction(self):
        boxes = ['top left', 'top center', 'top right', 'middle left', 'center', 'middle right', 'bottom left', 'bottom center', 'bottom right']
        for box in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            for x in range(3*(box//3), 3*(box//3)+3):
                for y in range(3*(box%3), 3*(box%3)+3):
                    if(self.cells[x][y].value in unknowns):
                        unknowns.remove(self.cells[x][y].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                rows = np.array([])
                cols = np.array([])
                for x in range(3*(box//3), 3*(box//3)+3):
                    for y in range(3*(box%3), 3*(box%3)+3):
                        if(unknownarr[u] in self.cells[x][y].options):
                            rows = np.append(rows,x)
                            cols = np.append(cols,y)
                if(rows.size != 0):
                    if(np.all(rows == rows[0]) and rows.size > 1):
                        for col in range(0,3*(box%3)):
                            candidateLeft = 0
                            for number in self.cells[int(rows[0])][col].options:
                                if (number != int(unknownarr[u])):
                                    candidateLeft = number
                            explain = 'In the ' + boxes[box] + ' box, the ' + str(unknownarr[u]) + ' must be in row ' + letters[int(rows[0])] + ', so it cannot be a candidate for ' + letters[int(rows[0])] + str(col + 1) + ', which only leaves one candidate for ' + letters[int(rows[0])] + str(col + 1) + ': ' + str(candidateLeft) + '..'
                            self.cells[int(rows[0])][col].removeOption(unknownarr[u],'Box Reduction',self, explain)
                        for col in range(3*(box%3) + 3, 9):
                            candidateLeft = 0
                            for number in self.cells[int(rows[0])][col].options:
                                if (number != int(unknownarr[u])):
                                    candidateLeft = number
                            explain = 'In the ' + boxes[box] + ' box, the ' + str(unknownarr[u]) + ' must be in row ' + letters[int(rows[0])] + ', so it cannot be a candidate for ' + letters[int(rows[0])] + str(col + 1) + ', which only leaves one candidate for ' + letters[int(rows[0])] + str(col + 1) + ': ' + str(candidateLeft) + '..'
                            self.cells[int(rows[0])][col].removeOption(unknownarr[u],'Box Reduction',self, explain)
                    if(np.all(cols == cols[0])and cols.size > 1):
                        for row in range(0,3*(box//3)):
                            candidateLeft = 0
                            for number in self.cells[row][int(cols[0])].options:
                                if (number != int(unknownarr[u])):
                                    candidateLeft = number
                            explain = 'In the ' + boxes[box] + ' box, the ' + str(unknownarr[u]) + ' must be in column ' + str(1 + int(cols[0])) + ', so it cannot be a candidate for ' + letters[row] + str(int(cols[0] + 1)) + ', which only leaves one candidate for ' + letters[row] + str(int(cols[0] + 1)) + ': ' + str(candidateLeft) + '..'
                            self.cells[row][int(cols[0])].removeOption(unknownarr[u],'Box Reduction',self, explain)
                        for row in range(3*(box//3) + 3, 9):
                            for number in self.cells[row][int(cols[0])].options:
                                if (number != int(unknownarr[u])):
                                    candidateLeft = number
                            explain = 'In the ' + boxes[box] + ' box, the ' + str(unknownarr[u]) + ' must be in column ' + str(1 + int(cols[0])) + ', so it cannot be a candidate for ' + letters[row] + str(int(cols[0] + 1)) + ', which only leaves one candidate for ' + letters[row] + str(int(cols[0] + 1)) + ': ' + str(candidateLeft) + '..'
                            self.cells[row][int(cols[0])].removeOption(unknownarr[u],'Box Reduction',self, explain)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def rowReduction(self):
        for row in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            for col in range(9):
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                cols = np.array([])
                for y in range(9):
                    if(unknownarr[u] in self.cells[row][y].options):
                        cols = np.append(cols,y)
                if(np.all(cols < 3) and cols.size > 1):
                    if(row < 3):
                        for x in range(row):
                            for y in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the top left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the top left box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                        for x in range(row + 1,3):
                            for y in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the top left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the top left box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                    if(2 < row < 6):
                        for x in range(3,row): 
                            for y in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the middle left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the middle left box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                        for x in range(row+1,6):
                            for y in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the middle left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the middle left box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                    if(5 < row):
                        for x in range(6,row): 
                            for y in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the bottom left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the bottom left box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                        for x in range(row + 1,9):
                            for y in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the bottom left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the bottom left box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                if(np.all(2 < cols) and np.all(cols < 6) and cols.size > 1):
                    if(row < 3):
                        for x in range(row):
                            for y in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the top center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the top center box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                        for x in range(row + 1,3):
                            for y in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the top center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the top center box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                    if(2 < row < 6):
                        for x in range(3,row): 
                            for y in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the center box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                        for x in range(row+1,6):
                            for y in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the center box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                    if(5 < row):
                        for x in range(6,row): 
                            for y in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the bottom center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the bottom center box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                        for x in range((row + 1),9):
                            for y in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the bottom center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the bottom center box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                if(np.all(cols > 5)and cols.size > 1):
                    if(row < 3):
                        for x in range(row):
                            for y in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the top right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the top right box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                        for x in range(row + 1,3):
                            for y in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the top right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the top right box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                    if(2 < row < 6):
                        for x in range(3,row): 
                            for y in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the middle right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the middle right box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                        for x in range(row+1,6):
                            for y in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the middle right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the middle right box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                    if(5 < row):
                        for x in range(6,row): 
                            for y in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the bottom right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the bottom right box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
                        for x in range((row + 1),9):
                            for y in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In row ' + letters[row] + ', the ' + str(unknownarr[u]) + ' must be in the bottom right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because  ' + letters[x] + str(y + 1) + '  is in the bottom right box but not in row ' + letters[row] + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Row Reduction',self, explain)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def colReduction(self):
        for col in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            for row in range(9):
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                rows = np.array([])
                for x in range(9):
                    if(unknownarr[u] in self.cells[x][col].options):
                        rows = np.append(rows,x)
                if(np.all(rows < 3) and rows.size > 1):
                    if(col < 3):
                        for y in range(0,col): 
                            for x in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the top left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the top left box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                        for y in range((col + 1),3):
                            for x in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the top left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the top left box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                    if(2 < col < 6):
                        for y in range(3,col): 
                            for x in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the top center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the top center box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                        for y in range((col + 1),6):
                            for x in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the top center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the top center box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                    if(5 < col):
                        for y in range(6,col):
                            for x in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the top right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the top right box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                        for y in range((col + 1),9):
                            for x in range(3):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the top right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the top right box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                if(np.all(2 < rows) and np.all(rows < 6) and rows.size > 1):
                    if(col < 3):
                        for y in range(0,col): 
                            for x in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the middle left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the middle left box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                        for y in range((col + 1),3):
                            for x in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the middle left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the middle left box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                    if(2 < col < 6):
                        for y in range(3,col): 
                            for x in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the center box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                        for y in range((col + 1),6):
                            for x in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the center box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                    if(5 < col):
                        for y in range(6,col):
                            for x in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the middle right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the middle right box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                        for y in range((col + 1),9):
                            for x in range(3,6):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the middle right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the middle right box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                if(np.all(rows > 5)and rows.size > 1):
                    if(col < 3):
                        for y in range(0,col): 
                            for x in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the bottom left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the bottom left box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                        for y in range((col + 1),3):
                            for x in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the bottom left box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the bottom left box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                    if(2 < col < 6):
                        for y in range(3,col): 
                            for x in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the bottom center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the bottom center box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                        for y in range((col + 1),6):
                            for x in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the bottom center box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the bottom center box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                    if(5 < col):
                        for y in range(6,col):
                            for x in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the bottom right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the bottom right box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
                        for y in range((col + 1),9):
                            for x in range(6,9):
                                candidateLeft = 0
                                for number in self.cells[x][y].options:
                                    if (number != int(unknownarr[u])):
                                        candidateLeft = number
                                explain = 'In column ' + str(col + 1) + ', the ' + str(unknownarr[u]) + ' must be in the bottom right box, so ' + letters[x] + str(y + 1) + ' cannot contain ' + str(unknownarr[u]) + ', because ' + letters[x] + str(y + 1) + ' is in the bottom right box but not in column ' + str(col + 1) + '. This only leaves one candidate for ' + letters[x] + str(y + 1) + ': ' + str(candidateLeft) + '..' 
                                self.cells[x][y].removeOption(unknownarr[u],'Column Reduction',self,explain)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def nakedTriple(self):
        boxes = ['top left', 'top center', 'top right', 'middle left', 'center', 'middle right', 'bottom left', 'bottom center', 'bottom right']
        for row in range(9):
            cols = []
            knowns = []
            counter = 0
            for col in range(9):
                if(self.cells[row][col].value == 0):
                    if(self.cells[row][col].options.size <= 3):
                        counter += 1
                        cols.append(col)
                else:
                    knowns.append(self.cells[row][col].value)
            colsarr = np.asarray(cols)
            if(counter >= 3):
                for a in range(3,10):
                    if(a not in knowns):
                        for b in range(2,a):
                            if(b not in knowns):
                                for c in range(1,b):
                                    if(c not in knowns):
                                        abc = np.array([a,b,c])
                                        winners = []
                                        for i in range(len(colsarr)):
                                            if(self.cells[row][colsarr[i]].options.size == 2):
                                                if(self.cells[row][colsarr[i]].options[0] in abc and self.cells[row][colsarr[i]].options[1] in abc):
                                                    winners.append(colsarr[i])
                                            if(self.cells[row][colsarr[i]].options.size == 3):
                                                if(self.cells[row][colsarr[i]].options[0] in abc and self.cells[row][colsarr[i]].options[1] in abc and self.cells[row][colsarr[i]].options[2] in abc):
                                                    winners.append(colsarr[i])
                                        winarr = np.asarray(winners)
                                        if(len(winarr) == 3):
                                            for col in range(9):
                                                if(col not in winarr):
                                                    for i in range(self.cells[row][col].options.size):
                                                        if(self.cells[row][col].options[i] != a and self.cells[row][col].options[i] != b and self.cells[row][col].options[i] != c):
                                                            v = self.cells[row][col].options[i]
                                                    explain = 'In row ' + letters[row] + ', cells ' + letters[row] + str(winarr[0] + 1) + ', ' +  letters[row] + str(winarr[1] + 1) + ', ' +  letters[row] + str(winarr[2] + 1) + ' form a naked triple, with the candidates ' + str(a) + ', ' + str(b) + ', and ' + str(c) + ', so these numbers are eliminated as candidates for ' + letters[row] + str(col + 1) + '. This leaves only one candidate for ' + letters[row] + str(col + 1) + ': ' + str(v) + '..'
                                                    self.cells[row][col].removeOption(a,'Naked Triple',self, explain)
                                                    self.cells[row][col].removeOption(b,'Naked Triple',self, explain)
                                                    self.cells[row][col].removeOption(c,'Naked Triple',self, explain)
        for col in range(9):
            rows = []
            counter = 0
            knowns = []
            for row in range(9):
                if(self.cells[row][col].value == 0):
                    if(self.cells[row][col].options.size <= 3):
                        counter += 1
                        rows.append(row)
            rowsarr = np.asarray(rows)
            if(counter >= 3):
                for a in range(3,10):
                    if(a not in knowns):
                        for b in range(2,a):
                            if(b not in knowns):
                                for c in range(1,b):
                                    if(c not in knowns):
                                        abc = np.array([a,b,c])
                                        winners = []
                                        for i in range(len(rowsarr)):
                                            if(self.cells[rowsarr[i]][col].options.size == 2):
                                                if(self.cells[rowsarr[i]][col].options[0] in abc and self.cells[rowsarr[i]][col].options[1] in abc):
                                                    winners.append(rowsarr[i])
                                            if(self.cells[rowsarr[i]][col].options.size == 3):
                                                if(self.cells[rowsarr[i]][col].options[0] in abc and self.cells[rowsarr[i]][col].options[1] in abc and self.cells[rowsarr[i]][col].options[2] in abc):
                                                    winners.append(rowsarr[i])
                                        winarr = np.asarray(winners)
                                        if(len(winarr) == 3):
                                            for row in range(9):
                                                if(row not in winarr):
                                                    for i in range(self.cells[row][col].options.size):
                                                        if(self.cells[row][col].options[i] != a and self.cells[row][col].options[i] != b and self.cells[row][col].options[i] != c):
                                                            v = self.cells[row][col].options[i]
                                                    explain = 'In column ' + str(col + 1) + ', cells ' + letters[winarr[0]] + str(col + 1) + ', ' + letters[winarr[1]] + str(col + 1) + ', ' + letters[winarr[2]] + str(col + 1) + ' form a naked triple, with the candidates ' + str(a) + ', ' + str(b) + ', and ' + str(c) + ', so these numbers are eliminated as candidates for ' + letters[row] + str(col + 1) + '. This leaves only one candidate for ' + letters[row] + str(col + 1) + ': ' + str(v) + '..'
                                                    self.cells[row][col].removeOption(a,'Naked Triple',self, explain)
                                                    self.cells[row][col].removeOption(b,'Naked Triple',self, explain)
                                                    self.cells[row][col].removeOption(c,'Naked Triple',self, explain)
        for x in range(9):                                
            rows = []
            cols = []
            knowns = []
            counter = 0
            for col in range(3*(x%3),3*(x%3) + 3):
                for row in range(3*math.floor(x/3),3*math.floor(x/3) + 3):
                    if(self.cells[row][col].value == 0):
                        if(self.cells[row][col].options.size <= 3):
                            counter += 1
                            rows.append(row)
                            cols.append(col)
                    else:
                        knowns.append(self.cells[row][col].value)
            rowsarr = np.asarray(rows)
            colsarr = np.asarray(cols)
            if(counter >= 3):
                for a in range(3,10):
                    if(a not in knowns):
                        for b in range(2,a):
                            if(b not in knowns):
                                for c in range(1,b):
                                    if(c not in knowns):
                                        abc = np.array([a,b,c])
                                        rows = []
                                        cols = []
                                        for i in range(len(rowsarr)):
                                            if(self.cells[rowsarr[i]][colsarr[i]].options.size == 2):
                                                if(self.cells[rowsarr[i]][colsarr[i]].options[0] in abc and self.cells[rowsarr[i]][colsarr[i]].options[1] in abc):
                                                    rows.append(rowsarr[i])
                                                    cols.append(colsarr[i])
                                            if(self.cells[rowsarr[i]][colsarr[i]].options.size == 3):
                                                if(self.cells[rowsarr[i]][colsarr[i]].options[0] in abc and self.cells[rowsarr[i]][colsarr[i]].options[1] in abc and self.cells[rowsarr[i]][colsarr[i]].options[2] in abc):
                                                    rows.append(rowsarr[i])
                                                    cols.append(colsarr[i])
                                        if(len(cols) == 3):
                                            for col in range(3*(x%3),3*(x%3) + 3):
                                                for row in range(3*math.floor(x/3),3*math.floor(x/3) + 3):
                                                    winner = False
                                                    for k in range(len(rows)):
                                                        if(rows[k] == row):
                                                             if(cols[k] == col):
                                                                 winner = True
                                                    if(winner == False):
                                                        for i in range(self.cells[row][col].options.size):
                                                            if(self.cells[row][col].options[i] != a and self.cells[row][col].options[i] != b and self.cells[row][col].options[i] != c):
                                                                v = self.cells[row][col].options[i]
                                                        explain = 'In the ' + boxes[x] + ' box, cells ' + letters[int(rows[0])] + str(cols[0] + 1) + ', ' + letters[int(rows[1])] + str(cols[1] + 1) + ', ' + letters[rows[2]] + str(cols[2] + 1) + ' form a naked triple, with the candidates ' + str(a) + ', ' + str(b) + ', and ' + str(c) + ', so these numbers are eliminated as candidates for ' + letters[row] + str(col + 1) + '. This leaves only one candidate for ' + letters[row] + str(col + 1) + ': ' + str(v) + '..'
                                                        self.cells[row][col].removeOption(a,'Naked Triple',self, explain)
                                                        self.cells[row][col].removeOption(b,'Naked Triple',self, explain)
                                                        self.cells[row][col].removeOption(c,'Naked Triple',self, explain)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
    def xwing(self):
        for col in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            knowns = []
            for row in range(9):
                #eliminates all values already known
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
                if(self.cells[row][col].value in knowns and self.cells[row][col].value != 0):
                    return 'error'
                knowns.append(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            #cycles through unknown values for each column
            for u in range(unknownarr.size):
                cells = ""
                counter = 0
                rows = []
                value = unknownarr[u]
                for row in range(9):
                    if (value in self.cells[row][col].options):
                        counter += 1
                        rows.append(row)
                        cells = cells + letters[row] + str(col + 1) + ', '
                rowsarr = np.asarray(rows)
                if(counter == 2):
                #if there are only 2 cells in a column that could contain unknown value, check if that is true for another column.
                    for column in range(col + 1, 9):
                        morecells = ""
                        rowstemp = []
                        for r in range(9):
                            if (value in self.cells[r][column].options):
                                rowstemp.append(r)
                                morecells = morecells + letters[r] + str(column + 1) + ', '
                        if(rowstemp == rows):
                            cells = cells + morecells
                            cells = cells[0:len(cells)-2]
                            for c in range(9):
                                if(c != col and c != column):
                                    explain = ""
                                    if(self.cells[rowsarr[0]][c].options.size == 2):
                                        if(int(self.cells[rowsarr[0]][c].options[0] != int(unknownarr[u]))):
                                            v = self.cells[rowsarr[0]][c].options[0]
                                        
                                        else:
                                            v = self.cells[rowsarr[0]][c].options[1]
                                        explain = cells + ' form an x-wing, because they are the only two cells in columns ' + str(col + 1) + ' and ' + str(column + 1) + ' that could contain ' + str(unknownarr[u]) + '. This eliminates ' + str(unknownarr[u]) + ' as an candidate for ' + letters[rowsarr[0]] + str(c + 1) + ', leaving only one candidate: ' + str(v) + '..'
                                    self.cells[rowsarr[0]][c].removeOption(unknownarr[u],'x-wing',self,explain)
                                    explain = ""
                                    if(self.cells[rowsarr[1]][c].options.size == 2):
                                        if(int(self.cells[rowsarr[1]][c].options[0]) != int(unknownarr[u])):
                                            v = self.cells[rowsarr[1]][c].options[0]
                                        else:
                                            v = self.cells[rowsarr[1]][c].options[1]
                                        explain = cells + ' form an x-wing, because they are the only two cells in columns ' + str(col + 1) + ' and ' + str(column + 1) + ' that could contain ' + str(unknownarr[u]) + '. This eliminates ' + str(unknownarr[u]) + ' as an candidate for ' + letters[rowsarr[1]] + str(c + 1) + ', leaving only one candidate: ' + str(v) + '..'
                                    self.cells[rowsarr[1]][c].removeOption(unknownarr[u],'x-wing',self,explain)
        for row in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            knowns = []
            for col in range(9):
                #eliminates all values already known
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
                if(self.cells[row][col].value in knowns and self.cells[row][col].value != 0):
                    return 'error'
                knowns.append(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                cells = ""
                counter = 0
                cols = []
                value = unknownarr[u]
                for col in range(9):
                    if (value in self.cells[row][col].options):
                        counter = counter + 1
                        cols.append(col)
                        cells = cells + letters[row] + str(col + 1) + ', '
                colsarr = np.asarray(cols)
                if(counter == 2):
                    for rowt in range(row + 1, 9):
                        morecells = ""
                        colstemp = []
                        for c in range(9):
                            if (value in self.cells[rowt][c].options):
                                colstemp.append(c)
                                morecells = morecells + letters[rowt] + str(c + 1) + ', '
                        if(colstemp == cols):
                            cells = cells + morecells
                            cells = cells[0:len(cells)-2]
                            for r in range(9):
                                if(r != row and r != rowt):
                                    explain = ""
                                    if(self.cells[r][colsarr[0]].options.size == 2):
                                        if(int(self.cells[r][colsarr[0]].options[0]) != int(unknownarr[u])):
                                            v = self.cells[r][colsarr[0]].options[0]
                                        else:
                                            v = self.cells[r][colsarr[0]].options[1]
                                           
                                        explain = cells + ' form an x-wing, because they are the only two cells in rows ' + letters[row] + ' and ' + letters[rowt] + ' that could contain ' + str(unknownarr[u]) + '. This eliminates ' + str(unknownarr[u]) + ' as an candidate for ' + letters[r] + str(colsarr[0] + 1) + ', leaving only one candidate: ' + str(v) + '..'
                                    self.cells[r][colsarr[0]].removeOption(unknownarr[u],'x-wing',self,explain)
                                    explain = ""
                                    if(self.cells[r][colsarr[1]].options.size == 2):
                                        if(int(self.cells[r][colsarr[1]].options[0]) != int(unknownarr[u])):
                                            v = self.cells[r][colsarr[1]].options[0]
                                        else:   
                                            v = self.cells[r][colsarr[1]].options[1]
                                        explain = cells + ' form an x-wing, because they are the only two cells in rows ' + letters[row] + ' and ' + letters[rowt] + ' that could contain ' + str(unknownarr[u]) + '. This eliminates ' + str(unknownarr[u]) + ' as an candidate for ' + letters[r] + str(colsarr[1] + 1) + ', leaving only one candidate: ' + str(v) + '..'
                                    self.cells[r][colsarr[1]].removeOption(unknownarr[u],'x-wing',self,explain)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
    def xywing(self):
        for row in range(9):
            for col in range(9):
                winners = []
                v = 0
                no = 0
                if(self.cells[row][col].options.size == 2):
                    b = self.cells[row][col].options
                    winners.append(b[0])
                    winners.append(b[1])
                    #check cells in same box as self.cells[row][col]
                    for x in range(3*(row//3), 3*(row//3) + 3):
                        for y in range(3*(col//3), (col//3)*3 + 3):
                            winners = [b[0],b[1]]
                            g = self.cells[x][y].options
                            if(self.cells[x][y].options.size == 2 and (x != row or y != col)):
                                if((g[0] in winners or g[1] in winners) and not(g[0] in winners and g[1] in winners)):             
                                    if(g[0] not in winners):
                                        winners.append(g[0])
                                        v = g[0]
                                        no = g[1]
                                    if(g[1] not in winners):
                                        winners.append(g[1])
                                        v = g[1]
                                        no = g[0]
                                #if cell in same box could lead to an xy-wing, check cells in the same column as original cell.
                                    for r in range(9):
                                        if(self.cells[r][col].options.size == 2):
                                            if(r != row and not (self.adjacentNumbers(r, col, x, y)) and (self.cells[r][col].options[0] in winners and self.cells[r][col].options[1] in winners and (self.cells[r][col].options[0] != no and self.cells[r][col].options[1] != no))):
                                                for k in range(9):
                                                    for l in range(9):
                                                        if(self.adjacentNumbers(r, col, k, l) and self.adjacentNumbers(x, y, k, l)):
                                                            explain = ""
                                                            if(self.cells[k][l].options.size == 2):
                                                                if(self.cells[k][l].options[0] != v):
                                                                    oneleft = self.cells[k][l].options[0]
                                                                else:
                                                                    oneleft = self.cells[k][l].options[1]
                                                                explain = 'Cells ' + letters[row] + str(col + 1) + ', ' + letters[x] + str(y + 1)+ ', ' + letters[r] + str(col + 1) + ' form an xy-wing. Either ' + letters[x] + str(y + 1)+ ' or ' + letters[r] + str(col + 1) + ' must contain ' + str(v) + ', so cell ' + letters[k] + str(l + 1) + ' cannot contain ' + str(v) + '. This leaves only one candidate for ' + letters[k] + str(l + 1) + ': ' + str(oneleft) + '..'
                                                                print('box-row xywing')
                                                            self.cells[k][l].removeOption(v,'xy-wing',self, explain)
                                    for c in range(9):
                                        if(self.cells[row][c].options.size == 2): 
                                            if(c != col and not (self.adjacentNumbers(row, c, x, y))and self.cells[row][c].options[0] in winners and self.cells[row][c].options[1] in winners and (self.cells[row][c].options[0] != no and self.cells[row][c].options[1] != no)):
                                                for k in range(9):
                                                    for l in range(9):
                                                        if(self.adjacentNumbers(row,c,k,l) and self.adjacentNumbers(x,y,k,l)):
                                                            explain = ""
                                                            if(self.cells[k][l].options.size == 2):
                                                                if(self.cells[k][l].options[0] != v):
                                                                    oneleft = self.cells[k][l].options[0]
                                                                else:
                                                                    oneleft = self.cells[k][l].options[1]
                                                                explain = 'Cells ' + letters[row] + str(col + 1) + ', ' + letters[x] + str(y + 1)+ ', ' + letters[row] + str(c + 1) + ' form an xy-wing. Either ' + letters[x] + str(y + 1)+ ' or ' + letters[row] + str(c + 1) + ' must contain ' + str(v) + ', so cell ' + letters[k] + str(l + 1) + ' cannot contain ' + str(v) + '. This leaves only one candidate for ' + letters[k] + str(l + 1) + ': ' + str(oneleft) + '..'
                                                                print('box-column xywing')
                                                            self.cells[k][l].removeOption(v,'xy-wing',self, explain)
                    for y in range(9):
                        winners = []
                        winners.append(b[0])
                        winners.append(b[1])
                        if(self.cells[row][y].options.size == 2 and y != col):
                            g = self.cells[row][y].options
                            if((g[0] in winners or g[1] in winners) and not(g[0] in winners and g[1] in winners)):
                                if(g[0] not in winners):
                                    winners.append(g[0])
                                    v = g[0]
                                    no = g[1]
                                if(g[1] not in winners):
                                    winners.append(g[1])
                                    v = g[1]
                                    no = g[0]
                                for x in range(9):
                                    if(self.cells[x][col].options.size == 2 and not (self.adjacentNumbers(x, col, row, y))and x != row and self.cells[x][col].options[0] in winners and self.cells[x][col].options[1] in winners and (self.cells[x][col].options[0] != no and self.cells[x][col].options[1] != no)):
                                        for k in range(9):
                                            for l in range(9):
                                                if(self.adjacentNumbers(row,y,k,l) and self.adjacentNumbers(x,col,k,l)):
                                                    explain = ""
                                                    if(self.cells[k][l].options.size == 2):
                                                        if(self.cells[k][l].options[0] != v):
                                                            oneleft = self.cells[k][l].options[0]
                                                        else:
                                                            oneleft = self.cells[k][l].options[1]
                                                        explain = 'Cells ' + letters[row] + str(col + 1) + ', ' + letters[row] + str(y + 1)+ ', ' + letters[x] + str(col + 1) + ' form an xy-wing. Either ' + letters[row] + str(y + 1)+ ' or ' + letters[x] + str(col + 1) + ' must contain ' + str(v) + ', so cell ' + letters[k] + str(l + 1) + ' cannot contain ' + str(v) + '. This leaves only one candidate for ' + letters[k] + str(l + 1) + ': ' + str(oneleft) + '..'
                                                        print('row-column xywing')
                                                    self.cells[k][l].removeOption(v,'xy-wing',self, explain)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
    def swordfish(self):
        for col in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            knowns = []
            for row in range(9):
                #eliminates all values already known
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
                if(self.cells[row][col].value in knowns and self.cells[row][col].value != 0):
                    return 'error'
                knowns.append(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                counter = 0
                rows = []
                value = unknownarr[u]
                for row in range(9):
                    if (value in self.cells[row][col].options):
                        counter = counter + 1
                        rows.append(row)
                rowsarr = np.asarray(rows)
                if(counter == 2):
                    winners = []
                    winners.append(rowsarr[0])
                    winners.append(rowsarr[1])
                    for column in range(col + 1, 9):
                        rowstemp = []
                        for row in range(9):
                            if (value in self.cells[row][column].options):
                                counter = counter + 1
                                rowstemp.append(row)
                        if(len(rowstemp) == 2 and (rowstemp[0] in rows or rowstemp[1] in rows) and rows != rowstemp):
                            if(rowstemp[0] in rows):
                                winners.append(rowstemp[1])
                            else:
                                winners.append(rowstemp[0])
                            for c in range(column + 1, 9):
                                rows3 = []
                                for row in range(9):
                                    if (value in self.cells[row][c].options):
                                        counter = counter + 1
                                        rows3.append(row)
                                if(len(rows3) == 2 and rows3 != rows and rows3 != rowstemp and rows3[0] in winners and rows3[1] in winners):
                                    for row in range(9):
                                        if(row not in winners):
                                            self.cells[row][col].removeOption(value,'swordfish',self)
                                            self.cells[row][column].removeOption(value,'swordfish',self)
                                            self.cells[row][c].removeOption(value,'swordfish',self)
        for row in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            knowns = []
            for col in range(9):
                #eliminates all values already known
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
                if(self.cells[row][col].value in knowns and self.cells[row][col].value != 0):
                    return 'error'
                knowns.append(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                counter = 0
                cols = []
                value = unknownarr[u]
                for col in range(9):
                    if (value in self.cells[row][col].options):
                        counter = counter + 1
                        cols.append(col)
                if(counter == 2):
                    winners = []
                    winners.append(cols[0])
                    winners.append(cols[1])
                    for ro in range(row + 1, 9):
                        colstemp = []
                        for col in range(9):
                            if (value in self.cells[ro][col].options):
                                counter = counter + 1
                                colstemp.append(col)
                        if(len(colstemp) == 2 and (colstemp[0] in cols or colstemp[1] in cols) and cols != colstemp):
                            if(colstemp[0] in cols):
                                winners.append(colstemp[1])
                            else:
                                winners.append(colstemp[0])
                            for r in range(ro + 1, 9):
                                cols3 = []
                                for col in range(9):
                                    if (value in self.cells[r][col].options):
                                        counter = counter + 1
                                        cols3.append(col)
                                if(len(cols3) == 2 and cols3 != cols and cols3 != colstemp and cols3[0] in winners and cols3[1] in winners):
                                    for col in range(9):
                                        if(col not in winners):
                                            self.cells[row][col].removeOption(value,'swordfish',self)
                                            self.cells[ro][col].removeOption(value,'swordfish',self)
                                            self.cells[r][col].removeOption(value,'swordfish',self)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
    def skyscraper(self):
        for col in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            knowns = []
            for row in range(9):
                #eliminates all values already known
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
                if(self.cells[row][col].value in knowns and self.cells[row][col].value != 0):
                    return 'error'
                knowns.append(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                counter = 0
                rows = []
                value = unknownarr[u]
                for row in range(9):
                    if (value in self.cells[row][col].options):
                        counter = counter + 1
                        rows.append(row)
                if(counter == 2):
                    for column in range(col + 1, 9):
                        rowstemp = []
                        for row in range(9):
                            if (value in self.cells[row][column].options):
                                counter = counter + 1
                                rowstemp.append(row)
                        if(len(rowstemp) == 2 and (rowstemp[0] in rows or rowstemp[1] in rows) and rows != rowstemp):
                            if(rowstemp[0] in rows):
                                cell1 = self.cells[rowstemp[1]][column]
                                
                                if(rows[0] in rowstemp):
                                    cell2 = self.cells[rows[1]][col]
                                    
                                else:
                                    cell2 = self.cells[rows[0]][col]
                                    
                            else:
                                cell1 = self.cells[rowstemp[0]][column]
                                
                                if(rows[0] in rowstemp):
                                    cell2 = self.cells[rows[1]][col]
                                   
                                else:
                                    cell2 = self.cells[rows[0]][col]
                                    
                            for r in range(9):
                                for c in range(9):
                                    if(self.cells[r][c].value == 0 and self.isAdjacent(self.cells[r][c], cell1) and self.isAdjacent(self.cells[r][c], cell2)):
                                        
                                        self.cells[r][c].removeOption(value,'skyscraper', self)
        for row in range(9):
            unknowns = [1,2,3,4,5,6,7,8,9]
            knowns = []
            for col in range(9):
                #eliminates all values already known
                if(self.cells[row][col].value in unknowns):
                    unknowns.remove(self.cells[row][col].value)
                if(self.cells[row][col].value in knowns and self.cells[row][col].value != 0):
                    return 'error'
                knowns.append(self.cells[row][col].value)
            unknownarr = np.asarray(unknowns)
            for u in range(unknownarr.size):
                counter = 0
                cols = []
                value = unknownarr[u]
                for col in range(9):
                    if (value in self.cells[row][col].options):
                        counter = counter + 1
                        rows.append(row)
                if(counter == 2):
                    for ro in range(row + 1, 9):
                        colstemp = []
                        for column in range(9):
                            if (value in self.cells[ro][column].options):
                                counter = counter + 1
                                colstemp.append(column)
                        if(len(colstemp) == 2 and (colstemp[0] in cols or colstemp[1] in cols) and cols != colstemp):
                            if(colstemp[0] in cols):
                                cell1 = self.cells[ro][colstemp[1]]
                                if(cols[0] in colstemp):
                                    cell2 = self.cells[row][cols[1]]
                                else:
                                    cell2 = self.cells[row][cols[0]]
                            else:
                                cell1 = self.cells[ro][colstemp[0]]
                        
                                if(cols[0] in colstemp):
                                    cell2 = self.cells[row][cols[1]]
                                   
                                else:
                                    cell2 = self.cells[row][cols[0]]
                                    
                            for r in range(9):
                                for c in range(9):
                                    if(self.cells[r][c].value == 0 and self.isAdjacent(self.cells[r][c], cell1) and self.isAdjacent(self.cells[r][c], cell2)):
                                        self.cells[r][c].removeOption(value,'skyscraper', self)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
    def checkDone(self):
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].value == 0):
                    return False
        return True
    def guessAndCheck(self):
        cellstor = copy.deepcopy(self.cells)
        i = 0
        j = 0
        runs = 0
        done = 0
        solved = self.cellsSolved
        while(done == 0 and runs < 1):
            if(self.cells[i][j].value == 0 and self.cells[i][j].options.size == 2):
                self.cells[i][j].value = self.cells[i][j].options[0]
                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                error = 0
                k = 0
                while(k < 3):
                    if (self.checkCells() == 'error'):
                        error+=1
                        print("found error at row" + str(i) + ", col" + str(j) + " checkcells")
                        self.cellsSolved = solved
                        self.cells = copy.deepcopy(cellstor)
                        self.cells[i][j].value = self.cells[i][j].options[1]
                        self.cells[i][j].removeOption(self.cells[i][j].options[0],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                        solved += 1
                        k = 20
                    if(error == 0):
                        if (self.checkBoxes() == 'error'):
                            error+=1
                            print("found error at row" + str(i) + ", col" + str(j) + " checkboxes")
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.checkColumns() == 'error'):
                            error+=1
                            print("found error at row" + str(i) + ", col" + str(j) + " checkcols")
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.checkRows() == 'error'):
                            error+=1
                            print("found error at row" + str(i) + ", col" + str(j) + " checkrows")
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.boxReduction() == 'error'):
                            error+=1
                            print("found error at row" + str(i) + ", col" + str(j) + " boxReduction")
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.colReduction() == 'error'):
                            error+=1
                            print("found error at row" + str(i) + ", col" + str(j) + " colReduction")
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.rowReduction() == 'error'):
                            error+=1
                            print("found error at row" + str(i) + ", col" + str(j) + " rowReduction")
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.nakedPairs() == 'error'):
                            error+=1
                            print("found error at row" + str(i) + ", col" + str(j) + " nakedPairs")
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.nakedTriple() == 'error'):
                            error+=1
                            print("found error at row" + str(i) + ", col" + str(j) + " nakedtriple")
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                            solved += 1
                            k = 20
                    if(error == 0):
                            if (self.xwing() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                    if(error == 0):
                            if (self.xywing() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                    k += 1
                if(error > 0):
                    cellstor = copy.deepcopy(self.cells)
                    runs = 1
                else:
                    self.cells = copy.deepcopy(cellstor)
                    self.cells[i][j].value = self.cells[i][j].options[1]
                    self.cells[i][j].removeOption(self.cells[i][j].options[0], 'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                    self.cellsSolved = solved
                    k = 0
                    while(k < 3):
                        if (self.checkCells() == 'error'):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[0]
                            self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                            solved += 1
                            k = 20
                        if(error == 0):    
                            if (self.checkBoxes() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.checkColumns() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.checkRows() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.boxReduction() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.colReduction() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.rowReduction() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.nakedPairs() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.nakedTriple() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.xwing() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.xywing() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'Guess and Check',self, 'Cell solved by Guess and Check (see methods page for more details)..')
                                solved += 1
                                k = 20
                        k += 1
                    if(error > 0):
                        cellstor = copy.deepcopy(self.cells)
                        runs = 1
                    else:
                        self.cells = copy.deepcopy(cellstor)
                        self.cellsSolved = solved
            if (self.checkDone() == True):
                done = 1
            error = 0
            if(j == 8):
                j = 0
                if(i == 8):
                    runs += 1
                    i = 0
                else:
                    i += 1
            else:
                j += 1
        
    def guessNakedPairs(self):
        cellstor = copy.deepcopy(self.cells)
        runs = 0
        i = 0
        j = 0
        done = 0
        solved = self.cellsSolved
        while(done == 0 and runs < 1):
            p = self.cells[i][j].options
            if(p.size == 2):
                identicalBoxes = 1
                vals = [j]
                for col in range(9):
                    if(np.array_equal(self.cells[i][col].options,p) and col!=j):
                        identicalBoxes += 1
                        vals.append(col)
                if(identicalBoxes == 2):
                    valsarr = np.asarray(vals)
                    a = p[0]
                    b = p[1]
                    self.cells[i][valsarr[0]].value = a
                    self.cells[i][valsarr[1]].value = b
                    self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                    self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                    k = 0
                    error = 0
                    while(k < 5):
                        if (self.checkCells() == 'error'):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][valsarr[0]].value = b
                            self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                            self.cells[i][valsarr[1]].value = a
                            self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                            solved += 2
                            k = 20
                        if(error == 0):
                            if (self.checkBoxes() == 'error' and error == 0):
                                error+=1
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][valsarr[0]].value = b
                                self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                                self.cells[i][valsarr[1]].value = a
                                self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                                solved += 2
                                self.cellsSolved = solved
                                k = 20
                        if(error == 0):
                            if (self.checkColumns() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][valsarr[0]].value = b
                                self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                                self.cells[i][valsarr[1]].value = a
                                self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                                solved += 2
                                k = 20
                        if(error == 0):
                            if (self.checkRows() == 'error' and error == 0):
                                error+=1
                                self.cells = copy.deepcopy(cellstor)
                                self.cellsSolved = solved
                                self.cells[i][valsarr[0]].value = b
                                self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                                self.cells[i][valsarr[1]].value = a
                                self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                                solved += 2
                                k = 20
                        if(error == 0):
                            if (self.boxReduction() == 'error' and error == 0):
                                error+=1
                                self.cells = copy.deepcopy(cellstor)
                                self.cellsSolved = solved
                                self.cells[i][valsarr[0]].value = b
                                self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                                self.cells[i][valsarr[1]].value = a
                                self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                                solved += 2
                                k = 20
                        if(error == 0):
                            if (self.colReduction() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][valsarr[0]].value = b
                                self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                                self.cells[i][valsarr[1]].value = a
                                self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                                solved += 2
                                k = 20
                        if(error == 0):
                            if (self.rowReduction() == 'error' and error == 0):
                                error+=1
                                self.cells = copy.deepcopy(cellstor)
                                self.cellsSolved = solved
                                self.cells[i][valsarr[0]].value = b
                                self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                                self.cells[i][valsarr[1]].value = a
                                self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                                solved += 2
                                k = 20
                        if(error == 0):
                            if (self.nakedPairs() == 'error' and error == 0):
                                error+=1
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][valsarr[0]].value = b
                                self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                                self.cells[i][valsarr[1]].value = a
                                self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                                solved += 2
                                self.cellsSolved = solved
                                k = 20
                        if(error == 0):
                            if (self.nakedTriple() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][valsarr[0]].value = b
                                self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                                self.cells[i][valsarr[1]].value = a
                                self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                                solved += 2
                                k = 20
                        k += 1
                    if(error > 0):
                        cellstor = copy.deepcopy(self.cells)
                        self.guessNaked += 1
                        self.cells[i][j].option = 'guessNakedPairs'
                        
                    else:
                        self.cells = copy.deepcopy(cellstor)
                        self.cells[i][valsarr[0]].value = b
                        self.cells[i][valsarr[0]].removeOption(a,'guessNakedPairs',self)
                        self.cells[i][valsarr[1]].value = a
                        self.cells[i][valsarr[1]].removeOption(b,'guessNakedPairs',self)
                        self.cellsSolved = solved
                        k = 0
                        while(k < 5):
                            if (self.checkCells() == 'error'):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][valsarr[0]].value = a
                                self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                                self.cells[i][valsarr[1]].value = b
                                self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                                solved += 2
                                k = 20
                            if(error == 0):
                                if (self.checkBoxes() == 'error' and error == 0):
                                    error+=1
                                    self.cellsSolved = solved
                                    self.cells = copy.deepcopy(cellstor)
                                    self.cells[i][valsarr[0]].value = a
                                    self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                                    self.cells[i][valsarr[1]].value = b
                                    self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                                    solved += 2
                                    k = 20
                            if(error == 0):
                                if (self.checkColumns() == 'error' and error == 0):
                                    error+=1
                                    self.cellsSolved = solved
                                    self.cells = copy.deepcopy(cellstor)
                                    self.cells[i][valsarr[0]].value = a
                                    self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                                    self.cells[i][valsarr[1]].value = b
                                    self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                                    solved += 2
                                    k = 20
                            if(error == 0):
                                if (self.checkRows() == 'error' and error == 0):
                                    error+=1
                                    self.cellsSolved = solved
                                    self.cells = copy.deepcopy(cellstor)
                                    self.cells[i][valsarr[0]].value = a
                                    self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                                    self.cells[i][valsarr[1]].value = b
                                    self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                                    solved += 2
                                    k = 20
                            if(error == 0):
                                if (self.boxReduction() == 'error' and error == 0):
                                    error+=1
                                    self.cellsSolved = solved
                                    self.cells = copy.deepcopy(cellstor)
                                    self.cells[i][valsarr[0]].value = a
                                    self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                                    self.cells[i][valsarr[1]].value = b
                                    self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                                    solved += 2
                                    k = 20
                            if(error == 0):
                                if (self.colReduction() == 'error' and error == 0):
                                    error+=1
                                    self.cellsSolved = solved
                                    self.cells = copy.deepcopy(cellstor)
                                    self.cells[i][valsarr[0]].value = a
                                    self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                                    self.cells[i][valsarr[1]].value = b
                                    self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                                    solved += 2
                                    k = 20
                            if(error == 0):
                                if (self.rowReduction() == 'error' and error == 0):
                                    error+=1
                                    self.cellsSolved = solved
                                    self.cells = copy.deepcopy(cellstor)
                                    self.cells[i][valsarr[0]].value = a
                                    self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                                    self.cells[i][valsarr[1]].value = b
                                    self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                                    solved += 2
                                    k = 20
                            if(error == 0):
                                if (self.nakedPairs() == 'error' and error == 0):
                                    error+=1
                                    self.cellsSolved = solved
                                    self.cells = copy.deepcopy(cellstor)
                                    self.cells[i][valsarr[0]].value = a
                                    self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                                    self.cells[i][valsarr[1]].value = b
                                    self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                                    solved += 1
                                    k = 20
                            if(error == 0):
                                if (self.nakedTriple() == 'error' and error == 0):
                                    error+=1
                                    self.cellsSolved = solved
                                    self.cells = copy.deepcopy(cellstor)
                                    self.cells[i][valsarr[0]].value = a
                                    self.cells[i][valsarr[0]].removeOption(b,'guessNakedPairs',self)
                                    self.cells[i][valsarr[1]].value = b
                                    self.cells[i][valsarr[1]].removeOption(a,'guessNakedPairs',self)
                                    solved += 1
                                    k = 20
                            k += 1
                        if(error > 0):
                            cellstor = copy.deepcopy(self.cells)
                            self.guessNaked += 1
                            self.cells[i][j].option = 'guessAndCheck'
                            
                        else:
                            self.cells = copy.deepcopy(cellstor)
                            self.cellsSolved = solved
                            if(len(p) == 2):
                                identicalBoxes = 1
                                vals = [i]
                                for row in range(9):
                                    if(np.array_equal(self.cells[row][j].options,p) and row!=i):
                                        identicalBoxes += 1
                                        vals.append(row)
                                if(identicalBoxes == 2):
                                    valsarr = np.asarray(vals)
                                    a = p[0]
                                    b = p[1]
                                    self.cells[valsarr[0]][j].value = a
                                    self.cells[valsarr[1]][j].value = b
                                    self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                    self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                    k = 0
                                    error = 0
                                    while(k < 5):
                                        if (self.checkCells() == 'error'):
                                            error+=1
                                            self.cellsSolved = solved
                                            self.cells = copy.deepcopy(cellstor)
                                            self.cells[valsarr[0]][j].value = b
                                            self.cells[valsarr[1]][j].value = a
                                            self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                            self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                            solved += 2
                                            k = 20
                                        if(error == 0):
                                            if (self.checkBoxes() == 'error' and error == 0):
                                                error+=1
                                                self.cellsSolved = solved
                                                self.cells = copy.deepcopy(cellstor)
                                                self.cells[valsarr[0]][j].value = b
                                                self.cells[valsarr[1]][j].value = a
                                                self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                                self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                                solved += 2
                                                k = 20
                                        if(error == 0):
                                            if (self.checkColumns() == 'error' and error == 0):
                                                error+=1
                                                self.cells = copy.deepcopy(cellstor)
                                                self.cellsSolved = solved
                                                self.cells[valsarr[0]][j].value = b
                                                self.cells[valsarr[1]][j].value = a
                                                self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                                self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                                solved += 2
                                                k = 20
                                        if(error == 0):
                                            if (self.checkRows() == 'error' and error == 0):
                                                error+=1
                                                self.cellsSolved = solved
                                                self.cells = copy.deepcopy(cellstor)
                                                self.cells[valsarr[0]][j].value = b
                                                self.cells[valsarr[1]][j].value = a
                                                self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                                self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                                solved += 2
                                                k = 20
                                        if(error == 0):
                                            if (self.boxReduction() == 'error' and error == 0):
                                                error+=1
                                                self.cellsSolved = solved
                                                self.cells = copy.deepcopy(cellstor)
                                                self.cells[valsarr[0]][j].value = b
                                                self.cells[valsarr[1]][j].value = a
                                                self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                                self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                                solved += 2
                                                k = 20
                                        if(error == 0):
                                            if (self.colReduction() == 'error' and error == 0):
                                                error+=1
                                                self.cellsSolved = solved
                                                self.cells = copy.deepcopy(cellstor)
                                                self.cells[valsarr[0]][j].value = b
                                                self.cells[valsarr[1]][j].value = a
                                                self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                                self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                                solved += 2
                                                k = 20
                                        if(error == 0):
                                            if (self.rowReduction() == 'error' and error == 0):
                                                error+=1
                                                self.cellsSolved = solved
                                                self.cells = copy.deepcopy(cellstor)
                                                self.cells[valsarr[0]][j].value = b
                                                self.cells[valsarr[1]][j].value = a
                                                self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                                self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                                solved += 2
                                                k = 20
                                        if(error == 0):
                                            if (self.nakedPairs() == 'error' and error == 0):
                                                error+=1
                                                self.cellsSolved = solved
                                                self.cells = copy.deepcopy(cellstor)
                                                self.cells[valsarr[0]][j].value = b
                                                self.cells[valsarr[1]][j].value = a
                                                self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                                self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                                solved += 2
                                                k = 20
                                        if(error == 0):
                                            if (self.nakedTriple() == 'error' and error == 0):
                                                error+=1
                                                self.cellsSolved = solved
                                                self.cells = copy.deepcopy(cellstor)
                                                self.cells[valsarr[0]][j].value = b
                                                self.cells[valsarr[1]][j].value = a
                                                self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                                self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                                solved += 2
                                                k = 20
                                        k += 1
                                    if(error > 0):
                                        cellstor = copy.deepcopy(self.cells)
                                        self.guessNaked += 1
                                        self.cells[i][j].option = 'guessNakedPairs'
                                        
                                    else:
                                        self.cells = copy.deepcopy(cellstor)
                                        self.cellsSolved = solved
                                        self.cells[valsarr[0]][j].value = b
                                        self.cells[valsarr[1]][j].value = a
                                        self.cells[valsarr[0]][j].removeOption(a,'guessNakedPairs',self)
                                        self.cells[valsarr[1]][j].removeOption(b,'guessNakedPairs',self)
                                        k = 0
                                        while(k < 5):
                                            if (self.checkCells() == 'error'):
                                                error+=1
                                                self.cellsSolved = solved
                                                self.cells = copy.deepcopy(cellstor)
                                                self.cells[valsarr[0]][j].value = a
                                                self.cells[valsarr[1]][j].value = b
                                                self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                                self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                                solved += 2
                                                k = 20
                                            if(error == 0):
                                                if (self.checkBoxes() == 'error' and error == 0):
                                                    error+=1
                                                    self.cellsSolved = solved
                                                    self.cells = copy.deepcopy(cellstor)
                                                    self.cells[valsarr[0]][j].value = a
                                                    self.cells[valsarr[1]][j].value = b
                                                    self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                                    self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                                    solved += 2
                                                    k = 20
                                            if(error == 0):
                                                if (self.checkColumns() == 'error' and error == 0):
                                                    error+=1
                                                    self.cellsSolved = solved
                                                    self.cells = copy.deepcopy(cellstor)
                                                    self.cells[valsarr[0]][j].value = a
                                                    self.cells[valsarr[1]][j].value = b
                                                    self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                                    self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                                    solved += 2
                                                    k = 20
                                            if(error == 0):
                                                if (self.checkRows() == 'error' and error == 0):
                                                    error+=1
                                                    self.cellsSolved = solved
                                                    self.cells = copy.deepcopy(cellstor)
                                                    self.cells[valsarr[0]][j].value = a
                                                    self.cells[valsarr[1]][j].value = b
                                                    self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                                    self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                                    solved += 2
                                                    k = 20
                                            if(error == 0):
                                                if (self.boxReduction() == 'error' and error == 0):
                                                    error+=1
                                                    self.cellsSolved = solved
                                                    self.cells = copy.deepcopy(cellstor)
                                                    self.cells[valsarr[0]][j].value = a
                                                    self.cells[valsarr[1]][j].value = b
                                                    self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                                    self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                                    solved += 2
                                                    k = 20
                                            if(error == 0):
                                                if (self.colReduction() == 'error' and error == 0):
                                                    error+=1
                                                    self.cellsSolved = solved
                                                    self.cells = copy.deepcopy(cellstor)
                                                    self.cells[valsarr[0]][j].value = a
                                                    self.cells[valsarr[1]][j].value = b
                                                    self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                                    self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                                    solved += 2
                                                    k = 20
                                            if(error == 0):
                                                if (self.rowReduction() == 'error' and error == 0):
                                                    error+=1
                                                    self.cellsSolved = solved
                                                    self.cells = copy.deepcopy(cellstor)
                                                    self.cells[valsarr[0]][j].value = a
                                                    self.cells[valsarr[1]][j].value = b
                                                    self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                                    self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                                    solved += 2
                                                    k = 20
                                            if(error == 0):
                                                if (self.nakedPairs() == 'error' and error == 0):
                                                    error+=1
                                                    self.cellsSolved = solved
                                                    self.cells = copy.deepcopy(cellstor)
                                                    self.cells[valsarr[0]][j].value = a
                                                    self.cells[valsarr[1]][j].value = b
                                                    self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                                    self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                                    solved += 2
                                                    k = 20
                                            if(error == 0):
                                                if (self.nakedTriple() == 'error' and error == 0):
                                                    error+=1
                                                    self.cellsSolved = solved
                                                    self.cells = copy.deepcopy(cellstor)
                                                    self.cells[valsarr[0]][j].value = a
                                                    self.cells[valsarr[1]][j].value = b
                                                    self.cells[valsarr[0]][j].removeOption(b,'guessNakedPairs',self)
                                                    self.cells[valsarr[1]][j].removeOption(a,'guessNakedPairs',self)
                                                    solved += 2
                                                    k = 20
                                            k += 1
                                        if(error > 0):
                                            cellstor = copy.deepcopy(self.cells)
                                            self.guessNaked += 1
                                            self.cells[i][j].option = 'guessNakedPairs'
                                            
                                        else:
                                            self.cells = copy.deepcopy(cellstor)
                                            self.cellsSolved = solved
            if (self.checkDone() == True):
                done = 1
            error = 0
            if(j == 8):
                j = 0
                if(i == 8):
                    runs += 1
                else:
                    i += 1
            else:
                j += 1
        

class Box(object):
    def __init__(self,cello,num):
        self.cells = np.array([[cello[0],cello[1],cello[2]],
                               [cello[3],cello[4],cello[5]],
                               [cello[6],cello[7],cello[8]]])
        self.value = "C"
        self.number = num
    def diags(self):
        if(self.cells[0][0].casefold() == self.cells[1][1].casefold() == self.cells[2][2].casefold() and self.cells[1][1] != "C"):
            self.value = self.cells[0][0]
        if(self.cells[2][0].casefold() == self.cells[1][1].casefold() == self.cells[0][2].casefold() and self.cells[1][1] != "C"):
            self.value = self.cells[0][2]
        return
    def rows(self):
        for i in range(3):
            if(self.cells[i][0].casefold() == self.cells[i][1].casefold() == self.cells[i][2].casefold() and self.cells[i][0] != "C"):
                self.value = self.cells[i][0]
        return
    def cols(self):
        for i in range(3):
            if(self.cells[0][i].casefold() == self.cells[1][i].casefold() == self.cells[2][i].casefold() and self.cells[0][i] != "C"):
                self.value = self.cells[0][i]
        return
app = Flask(__name__)
app.secret_key = "sudoku"
@app.route("/")
def no():
    return redirect(url_for("home"))
@app.route("/home")
def home():
    return render_template("index.html")
# puzzles fallback
@app.route("/puzzles")
def puzzles():
    return render_template("puzzles.html")
# puzzle app routes for each method
@app.route("/puzzles/checkcells/<dif>", methods=["GET","POST"])
def checkcellspuzzles(dif):
    c = ""
    n = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b", None)
        if("t" in session):
            session.pop("t", None)
        if("c" in session):
            session.pop("c", None)
        if("difficulty" in session):
            session.pop("difficulty", None)
        b = random.randint(0,8)
        session["difficulty"] = dif
        if(dif == "easy"):
            a = random.randint(1,5)
            if "ccpuz" in session:
                if(a == session["ccpuz"]):
                    if(a == 1):
                        a += 1
                    else:
                        a -= 1
            session["ccpuz"] = a
            if(a == 1):
                numbers = np.array([5,3,0,2,1,0,6,9,0,0,0,7,0,0,0,8,4,0,0,0,0,5,4,0,0,0,0])
                n = str(int((7+b-1) % 9) + 1)
                c = "A9"
                p = "number"
            if(a == 2):
                numbers = np.array([0,4,0,5,0,0,0,0,2,7,0,3,0,6,0,9,0,0,0,2,0,0,0,0,0,0,0,2,0,0,7,0,5,0,0,0,0,8,0,0,0,0,0,1,0,0,1,0,4,0,0,0,0,0])
                c = "B2"
                n = str(int((5+b-1) % 9) + 1)
                p = "number"
            if(a == 3):
                numbers = np.array([3,0,4,6,0,9,1,0,7,0,7,0,0,0,0,0,0,5,0,0,0,0,0,0,2,0,0])
                c = "A8"
                n = str(int((8+b-1) % 9) + 1)
                p = "number"
            if(a == 4):
                numbers = np.array([0,2,0,6,0,0,0,0,0,1,5,3,2,0,7,4,9,0,0,4,0,0,0,0,0,0,0])
                c = "B5"
                n = str(int((8+b-1) % 9) + 1)
                p = "number"
            if(a == 5):
                numbers = np.array([2,0,3,0,0,1,0,0,0,0,4,0,0,7,0,0,0,0,0,0,7,9,0,0,0,0,3,0,1,0,0,0,0,0,0,0,0,0,5,6,0,0,0,0,0,0,6,0,0,0,0,0,0,0,5,0,0,0,0,0,3,2,7,0,0,0,0,0,8,0,0,0,9,0,0,0,0,0,0,0,0])
                n = str(int((8+b-1) % 9) + 1)
                c = "G2"
                p = "number"
        if(dif == "medium"):
            a = random.randint(6,10)
            if "ccpuz" in session:
                if(a == session["ccpuz"]):
                    if(a == 6):
                        a += 1
                    else:
                        a -= 1
            session["ccpuz"] = a
            if(a == 6):
                numbers = np.array([1,0,2,0,4,0,0,0,0,4,3,0,5,0,9,6,0,0,0,0,7,0,0,0,8,3,4])
                c = "B3"
                p = "cell"
            if(a == 7):
                numbers = np.array([7,0,9,1,3,0,8,0,0,0,8,0,0,0,0,0,3,0,4,0,0,5,0,2,0,0,7,0,2,0,0,0,0,0,0,9,3,0,0,7,0,0,0,0,0,1,0,0,0,9,0,0,0,0,5,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,0])
                c = "B1"
                p = "cell"
            if(a == 8):
                numbers = np.array([9,0,0,5,0,2,0,0,0,0,7,4,8,0,1,3,0,0,2,0,0,6,0,0,0,4,0])
                c = "B5"
                p = "cell"
            if(a == 9):
                numbers = np.array([4,0,2,8,0,0,0,0,0,0,0,0,0,0,7,0,6,9,0,5,0,0,1,0,0,0,0,0,3,0,0,0,4,6,0,0,0,0,0,1,2,0,0,0,3,0,8,0,5,0,0,0,0,0])
                c = "B2"
                p = "cell"
            if(a == 10):
                numbers = np.array([8,0,0,5,0,0,0,0,0,1,2,0,4,0,0,0,0,0,0,0,3,0,0,0,7,0,9,0,4,0,0,7,0,0,0,0,6,0,0,8,0,2,0,0,0,7,0,0,0,0,0,9,6,0,0,9,0,1,0,0,0,0,0,3,0,0,0,0,0,5,0,0,0,0,0,0,0,0,3,0,0])
                p = "cell"
                c = "F4"
        if(dif == "hard"):
            a = random.randint(11,15)
            if "ccpuz" in session:
                if(a == session["ccpuz"]):
                    if(a == 11):
                        a += 1
                    else:
                        a -= 1
            session["ccpuz"] = a
            if(a == 11):
                numbers = np.array([0,0,0,5,0,0,7,9,8,0,9,8,0,0,0,3,0,0,5,7,2,3,0,0,0,0,0,3,4,0,0,9,0,5,0,0,7,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,4,0,3,0,5,2,1,2,0,0,0,0,0,0,0,0,0,4,0,6,0,8,0,1])
                c = "I1"
                p = "cell"
            if(a == 12):
                numbers = np.array([1,0,2,0,0,0,4,0,7,0,3,0,5,7,9,0,1,0,0,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,5,1,0,0,9,0,0,0,0,7,0,0,0,0,0,1,0,0,8,0,0,0,0,0,7,0,0,0,0,9,2,3,0,0,6,0,0,0,1,0,0,0,0,0,0])
                c = "H1"
                p = "cell"
            if(a == 13):
                numbers = np.array([7,4,0,2,1,9,5,0,0,1,2,0,0,0,0,4,9,0,3,9,5,6,4,0,0,0,0,0,0,0,7,0,0,1,0,0,0,0,3,0,0,0,0,0,0,0,0,9,0,2,0,0,0,0,0,0,1,0,8,0,0,0,9,0,3,2,0,0,0,0,6,5,0,7,0,0,0,0,0,0,8])
                c = "H7"
                p = "cell"
            if(a == 14):
                numbers = np.array([5,0,0,2,0,0,0,0,0,4,0,0,0,0,0,0,8,7,7,0,0,3,0,0,0,0,2,9,0,7,0,0,0,5,6,3,1,5,0,0,0,3,0,7,0,3,0,0,0,7,4,0,0,8,0,0,0,0,3,0,7,0,0,0,1,5,0,0,0,8,0,0,0,7,0,8,0,0,0,0,0])
                c = "D4"
                p = "cell"
            if(a == 15):
                numbers = np.array([0,0,0,4,0,0,0,0,0,0,9,0,0,7,2,0,0,4,0,0,8,0,0,1,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,0,6,0,0,0,0,0,7,0,0,0,0,9,4,5,0,1,0,0,0,0,0,0,0,0,2,0,8,0,3,0,0,0,0,0,0,7,0,0,0,0,1])
                c = "F6"
                p = "cell"
        session["b"] = b
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+b-1) % 9 + 1
        if(len(numbers) == 81):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            session["t"] = random.randint(0,2)
            if(session["t"] == 1):
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
            print(session["t"])
            print(c)
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        session["c"] = random.randint(0,2)
        print(session["c"])
        if(session["c"] == 1):
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
            c = c[0] + newcol
        if(session["c"] == 2):
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("checkcellspuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
        cell = request.form["cell"]
        if(session["ccpuz"] == 1):
            numbers = np.array([5,3,0,2,1,0,6,9,0,0,0,7,0,0,0,8,4,0,0,0,0,5,4,0,0,0,0])
            n = str(int((7+session["b"]-1) % 9) + 1)
            c = "A9"         
            p = "number"
            ref = 8
        if(session["ccpuz"] == 2):
            numbers = np.array([0,4,0,5,0,0,0,0,2,7,0,3,0,6,0,9,0,0,0,2,0,0,0,0,0,0,0,2,0,0,7,0,5,0,0,0,0,8,0,0,0,0,0,1,0,0,1,0,4,0,0,0,0,0])
            c = "B2"
            n = str(int((5+session["b"]-1) % 9) + 1)    
            p = "number"
            ref = 10
        if(session["ccpuz"] == 3):
            numbers = np.array([3,0,4,6,0,9,1,0,7,0,7,0,0,0,0,0,0,5,0,0,0,0,0,0,2,0,0])
            c = "A8"
            n = str(int((8+session["b"]-1) % 9) + 1)  
            p = "number"
            ref = 7
        if(session["ccpuz"] == 4):
            numbers = np.array([0,2,0,6,0,0,0,0,0,1,5,3,2,0,7,4,9,0,0,4,0,0,0,0,0,0,0])
            c = "B5"
            n = str(int((8+session["b"]-1) % 9) + 1) 
            p = "number"
            ref = 13
        if(session["ccpuz"] == 5):
            numbers = np.array([2,0,3,0,0,1,0,0,0,0,4,0,0,7,0,0,0,0,0,0,7,9,0,0,0,0,3,0,1,0,0,0,0,0,0,0,0,0,5,6,0,0,0,0,0,0,6,0,0,0,0,0,0,0,5,0,0,0,0,0,3,2,7,0,0,0,0,0,8,0,0,0,9,0,0,0,0,0,0,0,0])
            n = str(int((8+session["b"]-1) % 9) + 1)
            c = "G2"        
            p = "number"
            ref = 55
        if(session["ccpuz"] == 6):
            numbers = np.array([1,0,2,0,4,0,0,0,0,4,3,0,5,0,9,6,0,0,0,0,7,0,0,0,8,3,4])
            c = "B3" 
            p = "cell"
            ref = 11
            n = str(int((8+session["b"]-1) % 9) + 1)
        if(session["ccpuz"] == 7):
            numbers = np.array([7,0,9,1,3,0,8,0,0,0,8,0,0,0,0,0,3,0,4,0,0,5,0,2,0,0,7,0,2,0,0,0,0,0,0,9,3,0,0,7,0,0,0,0,0,1,0,0,0,9,0,0,0,0,5,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,0])
            c = "B1"
            p = "cell"
            ref = 9
            n = str(int((6+session["b"]-1) % 9) + 1)
        if(session["ccpuz"] == 8):
            numbers = np.array([9,0,0,5,0,2,0,0,0,0,7,4,8,0,1,3,0,0,2,0,0,6,0,0,0,4,0])
            c = "B5"  
            p = "cell"
            ref = 13
            n = str(int((9+session["b"]-1) % 9) + 1)
        if(session["ccpuz"] == 9):
            numbers = np.array([4,0,2,8,0,0,0,0,0,0,0,0,0,0,7,0,6,9,0,5,0,0,1,0,0,0,0,0,3,0,0,0,4,6,0,0,0,0,0,1,2,0,0,0,3,0,8,0,5,0,0,0,0,0])
            c = "B2" 
            p = "cell"
            ref = 10
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["ccpuz"] == 10):
            numbers = np.array([8,0,0,5,0,0,0,0,0,1,2,0,4,0,0,0,0,0,0,0,3,0,0,0,7,0,9,0,4,0,0,7,0,0,0,0,6,0,0,8,0,2,0,0,0,7,0,0,0,0,0,9,6,0,0,9,0,1,0,0,0,0,0,3,0,0,0,0,0,5,0,0,0,0,0,0,0,0,3,0,0])
            p = "cell"
            c = "F4"
            ref = 48
            n = str(int((3+session["b"]-1) % 9) + 1)
        if(session["ccpuz"] == 11):
            numbers = np.array([0,0,0,5,0,0,7,9,8,0,9,8,0,0,0,3,0,0,5,7,2,3,0,0,0,0,0,3,4,0,0,9,0,5,0,0,7,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,4,0,3,0,5,2,1,2,0,0,0,0,0,0,0,0,0,4,0,6,0,8,0,1])
            c = "I1"
            p = "cell"
            ref = 72
            n = str(int((9+session["b"]-1) % 9) + 1)
        if(session["ccpuz"] == 12):
            numbers = np.array([1,0,2,0,0,0,4,0,7,0,3,0,5,7,9,0,1,0,0,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,5,1,0,0,9,0,0,0,0,7,0,0,0,0,0,1,0,0,8,0,0,0,0,0,7,0,0,0,0,9,2,3,0,0,6,0,0,0,1,0,0,0,0,0,0])
            c = "H1" 
            p = "cell"
            ref = 63
            n = str(int((4+session["b"]-1) % 9) + 1)
        if(session["ccpuz"] == 13):
            numbers = np.array([7,4,0,2,1,9,5,0,0,1,2,0,0,0,0,4,9,0,3,9,5,6,4,0,0,0,0,0,0,0,7,0,0,1,0,0,0,0,3,0,0,0,0,0,0,0,0,9,0,2,0,0,0,0,0,0,1,0,8,0,0,0,9,0,3,2,0,0,0,0,6,5,0,7,0,0,0,0,0,0,8])
            c = "H7"
            p = "cell"
            ref = 69
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["ccpuz"] == 14):
            numbers = np.array([5,0,0,2,0,0,0,0,0,4,0,0,0,0,0,0,8,7,7,0,0,3,0,0,0,0,2,9,0,7,0,0,0,5,6,3,1,5,0,0,0,3,0,7,0,3,0,0,0,7,4,0,0,8,0,0,0,0,3,0,7,0,0,0,1,5,0,0,0,8,0,0,0,7,0,8,0,0,0,0,0])
            c = "D4"
            p = "cell"
            ref = 30
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["ccpuz"] == 15):
            numbers = np.array([0,0,0,4,0,0,0,0,0,0,9,0,0,7,2,0,0,4,0,0,8,0,0,1,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,0,6,0,0,0,0,0,7,0,0,0,0,9,4,5,0,1,0,0,0,0,0,0,0,0,2,0,8,0,3,0,0,0,0,0,0,7,0,0,0,0,1])
            c = "F6"
            p = "cell"
            ref = 50
            n = str(int((8+session["b"]-1) % 9) + 1)
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if("t" in session):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            if(session["t"] == 1):
                ref = (ref+54) % 81
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                ref = (ref+27) % 81
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        print(session["c"])
        if(session["c"] == 1):
            ref = 9*(ref//9) + (ref+6)%9
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        if(session["c"] == 2):
            ref = 9*(ref//9) + (ref+3)%9
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(g)
        if(p == "cell"):
            numslist[ref] = int(n)
            if(cell == c):
                return render_template("checkcellspuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=True, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
            else:
                return render_template("checkcellspuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=False, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
        else:
            red = []
            if(cell.isdigit()):
                numslist[ref] = int(cell)
                print(numslist)
                red = [ref]
            if(cell == n):
                return render_template("checkcellspuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=True, ans=n,difficulty=dif, blues=[ref], reds= [],grays=g, dif=session["difficulty"])
            else:
                return render_template("checkcellspuzzles.html", nums=numslist,length=len(numslist), lets=letters, result=False, ans=n,difficulty=dif, reds=red, blues=[], grays=g, dif=session["difficulty"] )
@app.route("/puzzles/checkboxes/<dif>", methods=["GET","POST"])
def checkboxespuzzles(dif):
    c = ""
    p = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b")
        if("t" in session):
            session.pop("t")
        if("c" in session):
            session.pop("c")
        if("difficulty" in session):
            session.pop("difficulty", None)
        b = random.randint(0,8)
        session["difficulty"] = dif
        if (dif == "easy"):
            a = random.randint(1,5)
            if "cbpuz" in session:
                if(a == session["cbpuz"]):
                    if(a == 1):
                        a += 1
                    else:
                        a -= 1
            session["cbpuz"] = a
            if(a == 1):
                numbers = np.array([2,1,0,0,0,3,5,0,0,0,0,6,7,5,0,0,0,0,0,0,4,0,0,0,7,0,0])
                n = str(int((7+b-1) % 9) + 1)
                c = "A3"
                p = "number"
                ref = 2
            if(a == 2):
                numbers = np.array([0,4,0,5,0,0,0,0,2,7,0,3,0,6,0,9,0,0,0,2,0,0,0,0,0,0,0,2,0,0,7,0,5,0,0,0,0,8,0,0,0,0,0,1,0,0,1,0,4,0,0,0,0,0])
                c = "D5"
                n = str(int((1+b-1) % 9) + 1)
                p = "number"
                ref = 31
            if(a == 3):
                numbers = np.array([9,2,0,0,0,0,0,0,8,0,4,0,8,2,0,1,0,0,0,6,0,7,0,1,0,0,0,5,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,3,0,0,0,3,0,0,0,0,8,0,0,0,7,0,0,0,0,0,0,8,0,9,0,0,0,0,0,7,0,0,0,0,0,7,0,0,0])
                c = "B1"
                n = str(int((7+b-1) % 9) + 1)
                p = "number"
                ref = 9
            if(a == 4):
                numbers = np.array([1,0,2,0,4,0,5,0,0,0,0,0,5,0,9,0,0,0,0,5,0,0,0,1,0,0,0,3,0,7,0,0,0,2,4,0,0,0,6,0,0,5,0,0,0,0,0,4,0,0,0,0,0,0,2,0,0,1,0,0,9,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0])
                c = "E4"
                n = str(int((4+b-1) % 9) + 1)
                p = "number"
                ref = 39
            if(a == 5):
                numbers = np.array([2,0,0,0,0,0,0,0,0,0,4,0,7,9,0,0,0,0,0,0,7,5,8,0,2,0,0,0,3,0,0,0,0,0,2,0,6,9,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,9,0,4,0,0,3,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,2])
                n = str(int((5+b-1) % 9) + 1)
                c = "I5"
                p = "number"
                ref = 76
        if(dif == "medium"):
            a = random.randint(6,10)
            if "cbpuz" in session:
                if(a == session["cbpuz"]):
                    if(a == 6):
                        a += 1
                    else:
                        a -= 1
            session["cbpuz"] = a
            if(a == 6):
                numbers = np.array([7,0,0,0,0,0,1,0,0,2,0,5,0,6,7,0,0,3,0,4,0,1,0,0,0,8,0])
                c = "B2"
                p = "cell"
                ref = 10
            if(a == 7):
                numbers = np.array([0,0,0,6,7,0,0,1,0,7,0,2,0,0,9,0,0,0,0,5,0,0,1,0,4,0,0])
                c = "B2"
                p = "cell"
                ref = 10
            if(a == 8):
                c = "E4"
                p = "cell"
                ref = 39
                numbers = np.array([3,0,0,4,0,0,0,0,0,4,0,0,0,0,3,0,0,0,0,6,7,0,0,1,0,0,8,0,9,1,0,0,0,5,0,4,0,8,6,0,5,0,0,0,0,0,0,0,7,2,0,0,0,0])
            if(a == 9):
                c = "E9"
                p = "cell"
                ref = 44
                numbers = np.array([0,9,0,0,0,0,0,0,3,0,5,2,0,0,9,7,0,0,0,3,0,1,4,7,0,0,0,8,0,6,2,0,0,0,0,0,0,0,0,5,0,0,4,3,0,0,0,0,8,7,0,0,0,0])
            if(a == 10):
                c = "A5"
                p = "cell"
                ref = 4
                numbers = np.array([0,1,0,9,0,0,0,0,0,8,9,5,2,7,0,0,0,0,0,0,0,0,0,0,9,4,0,1,4,0,0,0,0,7,0,0,5,7,0,0,2,4,1,0,0,0,0,9,0,3,0,4,0,5])
        if(dif == "hard"):
            a = random.randint(11,15)
            if "cbpuz" in session:
                if(a == session["cbpuz"]):
                    if(a == 11):
                        a += 1
                    else:
                        a -= 1
            session["cbpuz"] = a
            if(a == 11):
                numbers = np.array([0,0,0,0,3,0,0,4,2,0,0,0,0,6,2,0,0,0,2,9,5,0,0,0,0,3,0,7,0,0,2,0,0,0,0,0,0,1,3,0,0,0,0,0,9,0,0,0,4,0,7,0,0,0,0,0,0,0,0,0,0,9,0,1,0,0,0,8,5,0,0,0,0,0,7,0,0,0,0,0,0])
                c = "D6"
                p = "cell"
                ref = 32
            if(a == 12):
                numbers = np.array([0,0,0,0,0,0,2,0,0,5,4,0,0,6,0,0,9,0,0,0,0,7,0,3,0,0,0,0,9,3,0,0,0,0,0,0,0,1,0,6,0,7,0,0,0,0,2,0,0,0,0,0,0,3,0,0,0,0,2,0,0,5,0,9,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,1])
                c = "E5"
                p = "cell"
                ref = 40
            if(a == 13):
                numbers = np.array([1,3,0,4,0,0,0,0,0,0,0,0,0,0,0,9,7,0,8,0,0,0,0,0,0,0,0,0,0,0,1,0,4,0,9,5,5,0,0,0,2,9,0,0,0,9,7,0,0,0,3,0,0,0,0,1,2,0,0,5,0,0,0,0,0,0,0,3,8,5,0,1,0,0,0,7,0,0,0,0,0])
                c = "D5"
                p = "cell"
                ref = 31
            if(a == 14):
                numbers = np.array([0,7,0,2,5,0,1,0,0,1,5,0,3,7,0,0,4,0,0,0,9,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,3,0,0,0,0,2,1,0,0,0,0,7,0,5,9,0,0,2,0,0,0,0,1,0,0,0,0,6,3,8,0,0,0,0,1,0,0,0,0,0,0,0,0,9])
                c = "A8"
                p = "cell"
                ref = 7
            if(a == 15):
                numbers = np.array([5,0,0,6,0,0,4,0,0,4,6,0,0,0,0,8,0,0,0,0,0,1,0,0,0,0,5,9,3,0,4,0,0,0,0,0,8,5,0,0,7,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,7,3,8,0,6,0,0,0,4,0,0,9,0,0,1,0,0,0,0,0,0,0,0,0,2])
                c = "C8"
                p = "cell"
                ref = 25
        session["b"] = b
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+b-1) % 9 + 1
        if(len(numbers) == 81):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            session["t"] = random.randint(0,2)
            if(session["t"] == 1):
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
            print(session["t"])
            print(c)
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        session["c"] = random.randint(0,2)
        print(session["c"])
        if(session["c"] == 1):
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
            c = c[0] + newcol
        if(session["c"] == 2):
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("checkboxespuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
        cell = request.form["cell"]
        if(session["cbpuz"] == 1):
            numbers = np.array([2,1,0,0,0,3,5,0,0,0,0,6,7,5,0,0,0,0,0,0,4,0,0,0,7,0,0])
            n = str(int((7+session["b"]-1) % 9) + 1)
            c = "A3"
            p = "number"
            ref = 2
        if(session["cbpuz"] == 2):
            numbers = np.array([0,4,0,5,0,0,0,0,2,7,0,3,0,6,0,9,0,0,0,2,0,0,0,0,0,0,0,2,0,0,7,0,5,0,0,0,0,8,0,0,0,0,0,1,0,0,1,0,4,0,0,0,0,0])
            c = "D5"
            n = str(int((1+session["b"]-1) % 9) + 1)
            p = "number"
            ref = 31
        if(session["cbpuz"] == 3):
            numbers = np.array([9,2,0,0,0,0,0,0,8,0,4,0,8,2,0,1,0,0,0,6,0,7,0,1,0,0,0,5,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,3,0,0,0,3,0,0,0,0,8,0,0,0,7,0,0,0,0,0,0,8,0,9,0,0,0,0,0,7,0,0,0,0,0,7,0,0,0])
            c = "B1"
            n = str(int((7+session["b"]-1) % 9) + 1)
            p = "number"
            ref = 9
        if(session["cbpuz"] == 4):
            numbers = np.array([1,0,2,0,4,0,5,0,0,0,0,0,5,0,9,0,0,0,0,5,0,0,0,1,0,0,0,3,0,7,0,0,0,2,4,0,0,0,6,0,0,5,0,0,0,0,0,4,0,0,0,0,0,0,2,0,0,1,0,0,9,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0])
            c = "E4"
            n = str(int((4+session["b"]-1) % 9) + 1)
            p = "number"
            ref = 39
        if(session["cbpuz"] == 5):
            numbers = np.array([2,0,0,0,0,0,0,0,0,0,4,0,7,9,0,0,0,0,0,0,7,5,8,0,2,0,0,0,3,0,0,0,0,0,2,0,6,9,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,9,0,4,0,0,3,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,2])
            n = str(int((5+session["b"]-1) % 9) + 1)
            c = "I5"
            p = "number"
            ref = 76
        if(session["cbpuz"] == 6):
            numbers = np.array([7,0,0,0,0,0,1,0,0,2,0,5,0,6,7,0,0,3,0,4,0,1,0,0,0,8,0])
            c = "B2"
            p = "cell"
            ref = 10
            n = str(int((2+session["b"]-1) % 9) + 1)
        if(session["cbpuz"] == 7):
            numbers = np.array([0,0,0,6,7,0,0,1,0,7,0,2,0,0,9,0,0,0,0,5,0,0,1,0,4,7,0])
            c = "B2"
            p = "cell"
            ref = 10
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["cbpuz"] == 8):
            c = "E4"
            p = "cell"
            ref = 39
            n = str(int((2+session["b"]-1) % 9) + 1)
            numbers = np.array([3,0,0,4,0,0,0,0,0,4,0,0,0,0,3,0,0,0,0,6,7,0,0,1,0,0,8,0,9,1,0,0,0,5,0,4,0,8,6,0,5,0,0,0,0,0,0,0,7,2,0,0,0,0])
        if(session["cbpuz"] == 9):
            c = "E9"
            p = "cell"
            ref = 44
            n = str(int((9+session["b"]-1) % 9) + 1)
            numbers = np.array([0,9,0,0,0,0,0,0,3,0,5,2,0,0,9,7,0,0,0,3,0,1,4,7,0,0,0,8,0,6,2,0,0,0,0,0,0,0,0,5,0,0,4,3,0,0,0,0,8,7,0,0,0,0])
        if(session["cbpuz"] == 10):
            c = "A5"
            p = "cell"
            ref = 4
            n = str(int((1+session["b"]-1) % 9) + 1)
            numbers = np.array([0,1,0,9,0,0,0,0,0,8,9,5,2,7,0,0,0,0,0,0,0,0,0,0,9,4,0,1,4,0,0,0,0,7,0,0,5,7,0,0,2,4,1,0,0,0,0,9,0,3,0,4,0,5])
        if(session["cbpuz"] == 11):
            numbers = np.array([0,0,0,0,3,0,0,4,2,0,0,0,0,6,2,0,0,0,2,9,5,0,0,0,0,3,0,7,0,0,2,0,0,0,0,0,0,1,3,0,0,0,0,0,9,0,0,0,4,0,7,0,0,0,0,0,0,0,0,0,0,9,0,1,0,0,9,8,5,0,0,0,0,0,7,0,0,0,0,0,0])
            c = "D6"
            p = "cell"
            ref = 32
            n = str(int((3+session["b"]-1) % 9) + 1)
        if(session["cbpuz"] == 12):
            numbers = np.array([0,0,0,0,0,0,2,0,0,5,4,0,0,6,0,0,9,0,0,0,0,7,0,3,0,0,0,0,9,3,0,0,0,0,0,0,0,1,0,6,0,7,0,0,0,0,2,0,0,0,0,0,0,3,0,0,0,0,2,0,0,5,0,9,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,1])
            c = "E5"
            p = "cell"
            ref = 40
            n = str(int((3+session["b"]-1) % 9) + 1)
        if(session["cbpuz"] == 13):
            numbers = np.array([1,3,0,4,8,0,0,0,0,0,0,0,0,0,0,9,7,0,8,0,0,0,0,0,0,0,0,0,0,0,1,0,4,0,9,5,5,0,0,0,2,9,0,0,0,9,7,0,0,0,3,0,0,0,0,1,2,0,0,5,0,0,0,0,0,0,0,3,8,5,0,1,0,0,0,7,0,0,0,0,0])
            c = "D5"
            p = "cell"
            ref = 31
            n = str(int((3+session["b"]-1) % 9) + 1)
        if(session["cbpuz"] == 14):
            numbers = np.array([0,7,0,2,5,0,1,0,0,1,5,0,3,7,0,0,4,0,0,0,9,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,3,0,0,0,0,2,1,0,0,0,0,7,0,5,9,0,0,2,0,0,0,0,1,0,0,0,0,6,3,8,0,0,0,0,1,0,0,0,0,0,0,0,0,9])
            c = "A8"
            p = "cell"
            ref = 7
            n = str(int((6+session["b"]-1) % 9) + 1)
        if(session["cbpuz"] == 15):
            numbers = np.array([5,0,0,6,0,0,4,0,0,4,6,0,0,0,0,8,0,0,0,0,0,1,0,0,0,0,5,9,3,0,4,0,0,0,0,0,8,5,0,0,7,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,7,3,8,0,6,0,0,0,4,0,0,9,0,0,1,0,0,0,0,0,0,0,0,0,2])
            c = "C8"
            p = "cell"
            ref = 25
            n = str(int((6+session["b"]-1) % 9) + 1)
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if("t" in session):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            if(session["t"] == 1):
                ref = (ref+54) % 81
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                ref = (ref+27) % 81
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        print(session["c"])
        if(session["c"] == 1):
            ref = 9*(ref//9) + (ref+6)%9
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        if(session["c"] == 2):
            ref = 9*(ref//9) + (ref+3)%9
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(g)
        if(p == "cell"):
            numslist[ref] = int(n)
            if(cell == c):
                return render_template("checkboxespuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=True, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
            else:
                return render_template("checkboxespuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=False, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
        else:
            red = []
            if(cell.isdigit()):
                numslist[ref] = int(cell)
                print(numslist)
                red = [ref]
            if(cell == n):
                return render_template("checkboxespuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=True, ans=n,difficulty=dif, blues=[ref], reds= [],grays=g, dif=session["difficulty"])
            else:
                return render_template("checkboxespuzzles.html", nums=numslist,length=len(numslist), lets=letters, result=False, ans=n,difficulty=dif, reds=red, blues=[], grays=g, dif=session["difficulty"] )
@app.route("/puzzles/checkrows/<dif>", methods=["GET", "POST"])
def checkrowspuzzles(dif):
    c = ""
    n = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b")
        if("t" in session):
            session.pop("t")
        if("c" in session):
            session.pop("c")
        if("difficulty" in session):
            session.pop("difficulty", None)
        b = 0
        session["b"] = b
        session["difficulty"] = dif
        if(dif == "easy"):
            a = random.randint(1,5)
            if "rowpuz" in session:
                if(a == session["rowpuz"]):
                    if(a == 1):
                        a += 1
                    else:
                        a -= 1
            session["rowpuz"] = a
            if(a == 1):
                numbers = np.array([2,4,0,0,7,0,9,0,0,0,0,0,1,8,3,2,0,0,0,0,0,4,0,0,0,1,0])
                p = "number"
                n = str(int((1+session["b"]-1) % 9) + 1)
                c = "A3"
            if(a == 2):
                numbers = np.array([5,1,0,2,4,0,0,0,0,3,7,0,0,0,0,5,0,0,0,0,0,0,0,7,1,3,0])
                p = "number"
                n = str(int((3+session["b"]-1) % 9) + 1)
                c = "A6"
            if(a == 3):
                numbers = np.array([0,0,0,1,7,0,0,0,0,0,5,0,6,0,0,0,0,0,0,0,1,0,0,5,7,0,0,0,0,6,2,1,0,0,0,0,0,7,0,4,0,0,0,6,0,3,0,0,0,0,0,5,0,0])
                p = "number"
                n = str(int((5+session["b"]-1) % 9) + 1)
                c = "D1"
            if(a == 4):
                numbers = np.array([0,7,0,0,0,0,0,1,9,0,4,0,0,5,0,2,0,3,0,0,0,0,0,0,0,0,0,0,1,0,4,0,0,0,9,0,4,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,4,6,8,0,0,0,2,6,0,9,0,0,1,0,0,7,0,0,0,0,0])
                p = "number"
                n = str(int((4+session["b"]-1) % 9) + 1)
                c = "F8"
            if(a == 5):
                numbers = np.array([0,0,0,4,0,0,0,1,0,7,4,0,0,0,0,0,0,0,0,6,0,0,2,0,0,0,9,0,0,0,9,0,0,0,0,0,0,3,0,0,0,0,0,9,8,0,7,0,0,6,0,0,0,0,8,0,3,0,0,0,4,0,0,0,0,0,0,0,3,7,0,0,2,0,7,6,1,0,0,0,0])
                p = "number"
                n = str(int((4+session["b"]-1) % 9) + 1)
                c = "C8"
        if(dif == "medium"):
            a = random.randint(6,10)
            if "rowpuz" in session:
                if(a == session["rowpuz"]):
                    if(a == 6):
                        a += 1
                    else:
                        a -= 1
            session["rowpuz"] = a
            if(a == 6):
                numbers = np.array([0,3,4,0,9,0,0,1,0,2,0,0,0,1,5,0,0,0,0,7,0,0,0,0,0,0,3])
                c = "B4"
                p = "cell"
                n = str(int((3+session["b"]-1) % 9) + 1)
            if(a == 7):
                numbers = np.array([0,0,0,2,0,1,0,0,0,0,0,1,0,0,0,0,6,4,0,0,0,7,8,0,0,5,0,0,0,0,0,0,0,0,1,0,0,4,2,0,0,0,0,7,0,0,0,0,4,0,0,0,0,0])
                c = "D7"
                p = "cell"
            if(a == 8):
                numbers = np.array([2,0,0,0,1,0,4,7,0,9,3,0,7,0,0,8,0,0,1,0,0,0,4,2,0,0,0])
                c = "B3"
                p = "cell"
            if(a == 9):
                numbers = np.array([0,0,0,0,0,0,0,0,3,0,2,0,0,4,7,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,3,0,0,7,9,6,9,2,0,0,0,0,0,0,1,3,0,9,0,0,0,0,0])
                c = "B3"
                p = "cell"
            if(a == 10):
                numbers = np.array([0,0,0,2,0,9,7,0,0,0,1,7,5,0,0,0,0,0,0,5,0,0,0,0,4,0,0,1,4,0,0,0,0,0,9,0,2,8,9,7,0,0,0,3,0,0,0,0,0,0,5,0,0,0])
                c = "D9"
                p = "cell"
        if(dif == "hard"):
            a = random.randint(11,15)
            if "rowpuz" in session:
                if(a == session["rowpuz"]):
                    if(a == 11):
                        a += 1
                    else:
                        a -= 1
            session["rowpuz"] = a
            if(a == 11):
                numbers = np.array([0,0,0,0,1,7,0,0,0,0,0,0,0,0,2,0,5,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,6,7,0,8,0,9,0,0,4,0,8,0,0,0,0,0,0,0,0,0,0,0,4,0,0,8,0,0,9,0,5,0,1,0,0,0,2,0,0,0,0,3,0,0])
                c = "D8"
                p = "cell"
            if(a == 12):
                numbers = np.array([7,0,0,0,0,0,3,4,0,8,0,0,7,9,0,0,0,0,0,9,0,1,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,8,0,9,1,6,0,5,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,9,0,0,8,0,0,4,0,7,0,0,0,1,0,0,0,0,0,0])
                c = "H1"
                p = "cell"
            if(a == 13):
                numbers = np.array([0,9,0,0,0,0,0,1,0,5,0,1,2,6,0,0,0,7,0,0,0,0,1,0,0,5,0,0,0,3,0,0,0,7,0,1,0,0,9,0,0,0,0,4,0,0,0,0,5,0,1,0,0,9,9,0,0,0,0,0,0,7,0,7,0,0,6,8,4,0,0,0,0,8,0,0,3,0,0,0,0])
                c = "D2"
                p = "cell"
            if(a == 14):
                numbers = np.array([4,0,0,0,0,0,0,0,0,7,0,0,0,0,0,8,0,0,0,0,0,7,0,0,0,0,0,0,2,3,0,0,5,0,8,1,0,0,0,1,2,0,0,0,0,0,0,0,0,6,0,0,0,7,0,3,0,0,0,0,0,1,8,0,0,0,0,1,0,0,3,0,1,0,0,0,0,2,0,0,0])
                c = "D5"
                p = "cell"
            if(a == 15):
                numbers = np.array([0,0,0,0,0,4,0,0,0,2,3,0,0,0,0,7,1,0,0,0,0,0,0,0,0,0,0,0,0,0,9,6,0,0,0,0,7,6,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,8,0,0,0,0,0,8,0,0,0,0,0,0,0,9,0,7,1,0,0,0,0])
                c = "B9"
                p = "cell"
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+b-1) % 9 + 1
        if(len(numbers) == 81):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            session["t"] = random.randint(0,2)
            print('t:' + str(session["t"]))
            if(session["t"] == 1):
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        session["c"] = random.randint(0,2)
        print(session["c"])
        if(session["c"] == 1):
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
            c = c[0] + newcol
        if(session["c"] == 2):
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("checkrowspuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
        cell = request.form["cell"]
        if(session["rowpuz"] == 1):
            numbers = np.array([2,4,0,0,7,0,9,0,0,0,0,0,1,8,3,2,0,0,0,0,0,4,0,0,0,1,0])
            p = "number"
            n = str(int((1+session["b"]-1) % 9) + 1)
            c = "A3"
            ref = 2
        if(session["rowpuz"] == 2):
            numbers = np.array([5,1,0,2,4,0,0,0,0,3,7,0,0,0,0,5,0,0,0,0,0,0,0,7,1,3,0])
            p = "number"
            n = str(int((3+session["b"]-1) % 9) + 1)
            c = "A6"
            ref = 5
        if(session["rowpuz"] == 3):
            numbers = np.array([0,0,0,1,7,0,0,0,0,0,5,0,6,0,0,0,0,0,0,0,1,0,0,5,7,0,0,0,0,6,2,1,0,0,0,0,0,7,0,4,0,0,0,6,0,3,0,0,0,0,0,5,0,0])
            p = "number"
            n = str(int((5+session["b"]-1) % 9) + 1)
            c = "D1"
            ref = 28
        if(session["rowpuz"] == 4):
            numbers = np.array([0,7,0,0,0,0,0,1,9,0,4,0,0,5,0,2,0,3,0,0,0,0,0,0,0,0,0,0,1,0,4,0,0,0,9,0,4,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,4,6,8,0,0,0,2,6,0,9,0,0,1,0,0,7,0,0,0,0,0])
            p = "number"
            n = str(int((4+session["b"]-1) % 9) + 1)
            c = "F8"
            ref = 52
        if(session["rowpuz"] == 5):
            numbers = np.array([0,0,0,4,0,0,0,1,0,7,4,0,0,0,0,0,0,0,0,6,0,0,2,0,0,0,9,0,0,0,9,0,0,0,0,0,0,3,0,0,0,0,0,9,8,0,7,0,0,6,0,0,0,0,8,0,3,0,0,0,4,0,0,0,0,0,0,0,3,7,0,0,2,0,7,6,1,0,0,0,0])
            p = "number"
            n = str(int((4+session["b"]-1) % 9) + 1)
            c = "C8"
            ref = 25
        if(session["rowpuz"] == 6):
            numbers = np.array([0,3,4,0,9,0,0,1,0,2,0,0,0,1,5,0,0,0,0,7,0,0,0,0,0,0,3])
            c = "B4"
            p = "cell"
            ref = 12
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["rowpuz"] == 7):
            numbers = np.array([0,0,0,2,0,1,0,0,0,0,0,1,0,0,0,0,6,4,0,0,0,7,8,0,0,5,0,0,0,0,0,0,0,0,1,0,0,4,2,0,0,0,0,7,0,0,0,0,4,0,0,0,0,0])
            c = "D7"
            p = "cell"
            ref = 33
            n = str(int((3+session["b"]-1) % 9) + 1)
        if(session["rowpuz"] == 8):
            numbers = np.array([2,0,0,0,1,0,4,7,0,9,3,0,7,0,0,8,0,0,1,0,0,0,4,2,0,0,0])
            c = "B3"
            p = "cell"
            ref = 11
            n = str(int((4+session["b"]-1) % 9) + 1)
        if(session["rowpuz"] == 9):
            numbers = np.array([0,0,0,0,0,0,0,0,3,0,2,0,0,4,7,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,3,0,0,7,9,6,9,2,0,0,0,0,0,0,1,3,0,9,0,0,0,0,0])
            c = "B3"
            p = "cell"
            ref = 11
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["rowpuz"] == 10):
            numbers = np.array([0,0,0,2,0,9,7,0,0,0,1,7,5,0,0,0,0,0,0,5,0,0,0,0,4,0,0,1,4,0,0,0,0,0,9,0,2,8,9,7,0,0,0,3,0,0,0,0,0,0,5,0,0,0])
            c = "D9"
            p = "cell"
            ref = 35
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["rowpuz"] == 11):
            numbers = np.array([0,0,0,0,1,7,0,0,0,0,0,0,0,0,2,0,5,0,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,6,7,0,8,0,9,0,0,4,0,8,0,0,0,0,0,0,0,0,0,0,0,4,0,0,8,0,0,9,0,5,0,1,0,0,0,2,0,0,0,0,3,0,0])
            c = "D8"
            p = "cell"
            ref = 34
            n = str(int((8+session["b"]-1) % 9) + 1)
        if(session["rowpuz"] == 12):
            numbers = np.array([7,0,0,0,0,0,3,4,0,8,0,0,7,9,0,0,0,0,0,9,0,1,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,8,0,9,1,6,0,5,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,9,0,0,8,0,0,4,0,7,0,0,0,1,0,0,0,0,0,0])
            c = "H1"
            p = "cell"
            ref = 63
            n = str(int((9+session["b"]-1) % 9) + 1)
        if(session["rowpuz"] == 13):
            numbers = np.array([0,9,0,0,0,0,0,1,0,5,0,1,2,6,0,0,0,7,0,0,0,0,1,0,0,5,0,0,0,3,0,0,0,7,0,1,0,0,9,0,0,0,0,4,0,0,0,0,5,0,1,0,0,9,9,0,0,0,0,0,0,7,0,7,0,0,6,8,4,0,0,0,0,8,0,0,3,0,0,0,0])
            c = "D2"
            p = "cell"
            ref = 28
            n = str(int((5+session["b"]-1) % 9) + 1)
        if(session["rowpuz"] == 14):
            numbers = np.array([4,0,0,0,0,0,0,0,0,7,0,0,0,0,0,8,0,0,0,0,0,7,0,0,0,0,0,0,2,3,0,0,5,0,8,1,0,0,0,1,2,0,0,0,0,0,0,0,0,6,0,0,0,7,0,3,0,0,0,0,0,1,8,0,0,0,0,1,0,0,3,0,1,0,0,0,0,2,0,0,0])
            c = "D5"
            p = "cell"
            ref = 31
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["rowpuz"] == 15):
            numbers = np.array([0,0,0,0,0,4,0,0,0,2,3,0,0,0,0,7,1,0,0,0,0,0,0,0,0,0,0,0,0,0,9,6,0,0,0,0,7,6,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,8,0,0,0,0,0,8,0,0,0,0,0,0,0,9,0,7,1,0,0,0,0])
            c = "B9"
            p = "cell"
            ref = 17
            n = str(int((4+session["b"]-1) % 9) + 1)
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if("t" in session):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            if(session["t"] == 1):
                ref = (ref+54) % 81
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                ref = (ref+27) % 81
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        print(session["c"])
        if(session["c"] == 1):
            ref = 9*(ref//9) + (ref+6)%9
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        if(session["c"] == 2):
            ref = 9*(ref//9) + (ref+3)%9
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(g)
        if(p == "cell"):
            numslist[ref] = int(n)
            if(cell == c):
                return render_template("checkrowspuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=True, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
            else:
                return render_template("checkrowspuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=False, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
        else:
            red = []
            if(cell.isdigit()):
                numslist[ref] = int(cell)
                print(numslist)
                red = [ref]
            if(cell == n):
                return render_template("checkrowspuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=True, ans=n,difficulty=dif, blues=[ref], reds= [],grays=g, dif=session["difficulty"])
            else:
                return render_template("checkrowspuzzles.html", nums=numslist,length=len(numslist), lets=letters, result=False, ans=n,difficulty=dif, reds=red, blues=[], grays=g, dif=session["difficulty"] )
@app.route("/puzzles/checkcols/<dif>", methods=["GET", "POST"])
def checkcolumnspuzzles(dif):
    c = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b")
        if("t" in session):
            session.pop("t")
        if("c" in session):
            session.pop("c")
        if("difficulty" in session):
            session.pop("difficulty", None)
        b = 0
        session["b"] = b 
        session["difficulty"] = dif
        if(dif == "easy"):
            a = random.randint(1,5)
            if "colpuz" in session:
                if(a == session["colpuz"]):
                    if(a == 1):
                        a += 1
                    else:
                        a -= 1
            session["colpuz"] = a
            if(a == 1):
                numbers = np.array([7,0,0,0,0,3,0,1,0,0,0,0,0,2,7,1,0,8,0,0,0,2,5,9,0,8,0])
                c = "G2"
                n = str(int((7+session["b"]-1) % 9) + 1)
                p = "number"
            if(a == 2):
                numbers = np.array([0,3,0,0,8,0,0,5,0,3,1,0,0,8,0,0,2,0,0,0,0,0,3,0,0,2,0,0,7,1,0,0,0,0,0,0,2,0,0,0,0,7,3,0,7,0,0,0,0,0,0,1,0,0])
                c = "I6"
                n = str(int((3+session["b"]-1) % 9) + 1)
                p = "number"
            if(a == 3):
                numbers = np.array([0,0,0,0,7,0,0,0,0,0,0,0,0,4,0,0,0,0,7,0,0,0,0,0,5,4,0,0,0,0,0,0,0,0,0,7,0,7,0,0,0,8,0,0,0,4,0,0,0,0,7,0,0,0,0,0,7,0,0,0,0,0,0,1,0,0,4,5,0,0,0,0,0,0,0,7,0,0,0,9,1])
                c = "D6"
                n = str(int((4+session["b"]-1) % 9) + 1)
                p = "number"
            if(a == 4):
                numbers = np.array([0,0,7,0,0,1,0,0,0,8,0,0,0,6,0,0,9,7,2,0,0,9,7,0,0,0,0,0,2,0,1,0,8,0,0,0,0,0,0,0,0,0,8,0,0,0,0,6,0,0,0,2,0,0,0,0,4,0,1,3,5,0,0,0,0,0,0,8,7,0,1,0,6,0,0,0,0,0,0,0,0])
                c = "I3"
                n = str(int((8+session["b"]-1) % 9) + 1)
                p = "number"
            if(a == 5):
                numbers = np.array([0,3,1,0,0,9,9,0,0,0,4,0,0,0,7,3,0,0,0,4,0,0,0,0,0,0,9,0,5,0,0,0,0,0,0,0,0,0,8,0,0,0,0,1,0,7,0,0,7,0,0,0,0,4])
                c = "H3"
                n = str(int((4+session["b"]-1) % 9) + 1)
                p = "number"
        if(dif == "medium"):      
            a = random.randint(6,10)
            if "colpuz" in session:
                if(a == session["colpuz"]):
                    if(a == 6):
                        a += 1
                    else:
                        a -= 1
            session["colpuz"] = a
            if(a == 6):
                numbers = np.array([1,0,0,0,0,4,5,0,0,6,0,0,3,5,7,8,0,1,0,0,6,0,2,0,0,0,0])
                c = "B1"
                p = "cell"
            if(a == 7):
                numbers = np.array([0,0,0,0,6,4,2,0,3,0,0,0,0,1,9,3,0,0,4,5,0,9,7,0,0,0,0])
                c = "I2"
                p = "cell"
            if(a == 8):
                numbers = np.array([0,9,0,0,6,0,2,8,0,0,0,7,0,0,9,1,0,6,0,0,0,0,4,0,6,1,0])
                c = "G2"
                p = "cell"
            if(a == 9):
                numbers = np.array([0,0,0,0,7,0,0,9,3,0,0,4,5,0,0,8,2,0,0,0,6,3,1,0,7,0,0,0,0,0,0,5,0,0,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,7])
                c = "F4"
                p = "cell"
            if(a == 10):
                numbers = np.array([0,0,0,3,0,1,0,1,0,0,0,0,0,2,0,5,0,0,0,7,0,0,0,0,0,0,0,0,0,5,0,0,2,0,0,0,7,4,0,0,8,0,0,5,0,0,0,0,0,0,0,0,0,0])
                c = "I5"
                p = "cell"
        if(dif == "hard"):
            a = random.randint(11,15)
            if "colpuz" in session:
                if(a == session["colpuz"]):
                    if(a == 11):
                        a += 1
                    else:
                        a -= 1
            session["colpuz"] = a
            if(a == 11):
                numbers = np.array([0,4,0,0,2,0,0,0,0,0,0,0,0,1,0,7,9,0,0,2,0,9,8,0,0,0,0,0,0,0,0,0,0,2,4,5,4,6,0,0,3,0,0,0,0,0,0,0,0,0,9,0,1,0,5,3,0,0,7,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,7,0,0,0,0,0,0])
                c = "E8"
                p = "cell"
            if(a == 12):
                numbers = np.array([0,0,1,0,2,0,3,0,0,0,0,0,0,5,0,0,0,0,0,0,7,0,0,0,0,9,0,0,0,0,0,0,0,0,0,4,4,1,0,0,9,8,0,0,0,0,7,0,0,0,0,0,0,3,0,0,0,0,0,4,0,0,0,0,0,5,0,0,1,0,3,0,1,0,0,0,0,7,0,0,2])
                c = "D5"
                p = "cell"
            if(a == 13):
                numbers = np.array([0,1,0,9,0,0,0,2,0,0,0,0,2,0,0,1,3,0,0,0,3,0,0,1,0,0,0,0,8,0,0,2,0,0,0,0,0,3,9,0,0,8,0,0,0,0,0,0,0,0,0,0,7,0,0,6,0,0,5,0,0,0,0,5,0,0,0,0,6,0,0,0,0,0,0,4,0,0,8,0,6])
                c = "C8"
                p = "cell"
            if(a == 14):
                numbers = np.array([0,0,0,0,0,7,5,0,0,0,0,2,0,0,0,0,0,9,0,0,0,9,0,0,0,0,0,4,0,6,0,7,0,0,5,0,0,0,0,0,0,9,4,8,1,0,0,1,0,0,0,3,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,4,3,0,9,0,0,0,0,0,0,0])
                c = "A3"
                p = "cell"
            if(a == 15):
                numbers = np.array([0,0,0,1,0,0,5,0,7,7,0,0,3,0,0,0,0,9,9,5,0,0,7,0,0,0,0,0,0,5,0,3,0,1,0,8,6,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,8,0,0,0,0,3,8,0,0,0,4,0,7,0,0,0,0,0,0,0,0,0,0])
                c = "F7"
                p = "cell"
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+b-1) % 9 + 1
        tempnum = copy.deepcopy(numbers)
        newrow = ""
        print(c)
        session["t"] = random.randint(0,2)
        print(session["t"])
        if(session["t"] == 1):
            for i in range(2*len(numbers) // 3):
                numbers[i] = int(tempnum[i+len(numbers) // 3])
            for i in range(2*len(numbers) // 3,len(numbers)):
                numbers[i] = int(tempnum[i-2*len(numbers) // 3])
            for i in range(9):
               if(c[0] == letters[i]):
                   newrow = letters[(i+6)%9]
            c = newrow + c[1]
        if(session["t"] == 2):
            for i in range(len(numbers) // 3):
                numbers[i] = int(tempnum[i+2*len(numbers) // 3])
            for i in range(len(numbers) // 3,len(numbers)):
                numbers[i] = int(tempnum[i-len(numbers) // 3])
            for i in range(9):
               if(c[0] == letters[i]):
                   newrow = letters[(i+3)%9]
            c = newrow + c[1]
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("checkcolspuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
        cell = request.form["cell"]
        if(session["colpuz"] == 1):
            numbers = np.array([7,0,0,0,0,3,0,1,0,0,0,0,0,2,7,1,0,8,0,0,0,2,5,9,0,8,0])
            c = "G2"
            n = str(int((7+session["b"]-1) % 9) + 1)
            p = "number"
            ref = 19
        if(session["colpuz"] == 2):
            numbers = np.array([0,3,0,0,8,0,0,5,0,3,1,0,0,8,0,0,2,0,0,0,0,0,3,0,0,2,0,0,7,1,0,0,0,0,0,0,2,0,0,0,0,7,3,0,7,0,0,0,0,0,0,1,0,0])
            c = "I6"
            n = str(int((3+session["b"]-1) % 9) + 1)
            p = "number"
            ref = 53
        if(session["colpuz"] == 3):
            numbers = np.array([0,0,0,0,7,0,0,0,0,0,0,0,0,4,0,0,0,0,7,0,0,0,0,0,5,4,0,0,0,0,0,0,0,0,0,7,0,7,0,0,0,8,0,0,0,4,0,0,0,0,7,0,0,0,0,0,7,0,0,0,0,0,0,1,0,0,4,5,0,0,0,0,0,0,0,7,0,0,0,9,1])
            c = "D6"
            n = str(int((4+session["b"]-1) % 9) + 1)
            p = "number"
            ref = 33
        if(session["colpuz"] == 4):
            numbers = np.array([0,0,7,0,0,1,0,0,0,8,0,0,0,6,0,0,9,7,2,0,0,9,7,0,0,0,0,0,2,0,1,0,8,0,0,0,0,0,0,0,0,0,8,0,0,0,0,6,0,0,0,2,0,0,0,0,4,0,1,3,5,0,0,0,0,0,0,8,7,0,1,0,6,0,0,0,0,0,0,0,0])
            c = "I3"
            n = str(int((8+session["b"]-1) % 9) + 1)
            p = "number"
            ref = 74
        if(session["colpuz"] == 5):
            numbers = np.array([0,3,1,0,0,9,9,0,0,0,4,0,0,0,7,3,0,0,0,4,0,0,0,0,0,0,9,0,5,0,0,0,0,0,0,0,0,0,8,0,0,0,0,1,0,7,0,0,7,0,0,0,0,4])
            c = "H3"
            n = str(int((4+session["b"]-1) % 9) + 1)
            p = "number"
            ref = 44
        if(session["colpuz"] == 6):
            numbers = np.array([1,0,0,0,0,4,5,0,0,6,0,0,3,5,7,8,0,1,0,0,6,0,2,0,0,0,0])
            c = "B1"
            p = "cell"
            ref = 3
            n = str(int((2+session["b"]-1) % 9) + 1)
        if(session["colpuz"] == 7):
            numbers = np.array([0,0,0,0,6,4,2,0,3,0,0,0,0,1,9,3,0,0,4,5,0,9,7,0,0,0,0])
            c = "I2"
            p = "cell"
            ref = 25
            n = str(int((3+session["b"]-1) % 9) + 1)
        if(session["colpuz"] == 8):
            numbers = np.array([0,9,0,0,6,0,2,8,0,0,0,7,0,0,9,1,0,6,0,0,0,0,4,0,6,1,0])
            c = "G2"
            p = "cell"
            ref = 19
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["colpuz"] == 9):
            numbers = np.array([0,0,0,0,7,0,0,9,3,0,0,4,5,0,0,8,2,0,0,0,6,3,1,0,7,0,0,0,0,0,0,5,0,0,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,7])
            c = "F4"
            p = "cell"
            ref = 33
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["colpuz"] == 10):
            numbers = np.array([0,0,0,3,0,1,0,1,0,0,0,0,0,2,0,5,0,0,0,7,0,0,0,0,0,0,0,0,0,5,0,0,2,0,0,0,7,4,0,0,8,0,0,5,0,0,0,0,0,0,0,0,0,0])
            c = "I5"
            p = "cell"
            ref = 52
            n = str(int((5+session["b"]-1) % 9) + 1)
        if(session["colpuz"] == 11):
            numbers = np.array([0,4,0,0,2,0,0,0,0,0,0,0,0,1,0,7,9,0,0,2,0,9,8,0,0,0,0,0,0,0,0,0,0,2,4,5,4,6,0,0,3,0,0,0,0,0,0,0,0,0,9,0,1,0,5,3,0,0,7,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,7,0,0,0,0,0,0])
            c = "E8"
            p = "cell"
            ref = 43
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["colpuz"] == 12):
            numbers = np.array([0,0,1,0,2,0,3,0,0,0,0,0,0,5,0,0,0,0,0,0,7,0,0,0,0,9,0,0,0,0,0,0,0,0,0,4,4,1,0,0,9,8,0,0,0,0,7,0,0,0,0,0,0,3,0,0,0,0,0,4,0,0,0,0,0,5,0,0,1,0,3,0,1,0,0,0,0,7,0,0,2])
            c = "D5"
            p = "cell"
            ref = 31
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["colpuz"] == 13):
            numbers = np.array([0,1,0,9,0,0,0,2,0,0,0,0,2,0,0,1,3,0,0,0,3,0,0,1,0,0,0,0,8,0,0,2,0,0,0,0,0,3,9,0,0,8,0,0,0,0,0,0,0,0,0,0,7,0,0,6,0,0,5,0,0,0,0,5,0,0,0,0,6,0,0,0,0,0,0,4,0,0,8,0,6])
            c = "C8"
            p = "cell"
            ref = 25
            n = str(int((8+session["b"]-1) % 9) + 1)
        if(session["colpuz"] == 14):
            numbers = np.array([0,0,0,0,0,7,5,0,0,0,0,2,0,0,0,0,0,9,0,0,0,9,0,0,0,0,0,4,0,6,0,7,0,0,5,0,0,0,0,0,0,9,4,8,1,0,0,1,0,0,0,3,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,4,3,0,9,0,0,0,0,0,0,0])
            c = "A3"
            p = "cell"
            ref = 2
            n = str(int((9+session["b"]-1) % 9) + 1)
        if(session["colpuz"] == 15):
            numbers = np.array([0,0,0,1,0,0,5,0,7,7,0,0,3,0,0,0,0,9,9,5,0,0,7,0,0,0,0,0,0,5,0,3,0,1,0,8,6,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,8,0,0,0,0,3,8,0,0,0,4,0,7,0,0,0,0,0,0,0,0,0,0])
            c = "F7"
            p = "cell"
            ref = 52
            n = str(int((7+session["b"]-1) % 9) + 1)
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if("t" in session):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            print(session["t"])
            if(session["t"] == 1):
                ref = (ref + 2*len(numbers) // 3) % len(numbers)
                for i in range(2*len(numbers) // 3):
                    numbers[i] = int(tempnum[i+len(numbers) // 3])
                for i in range(2*len(numbers) // 3,len(numbers)):
                    numbers[i] = int(tempnum[i-2*len(numbers) // 3])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                ref = (ref + len(numbers) // 3) % len(numbers)
                for i in range(len(numbers) // 3):
                    numbers[i] = int(tempnum[i+2*len(numbers) // 3])
                for i in range(len(numbers) // 3,len(numbers)):
                    numbers[i] = int(tempnum[i-len(numbers) // 3])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
            print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(g)
        if(p == "cell"):
            numslist[ref] = int(n)
            if(cell == c):
                return render_template("checkcolspuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=True, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
            else:
                return render_template("checkcolspuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=False, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
        else:
            red = []
            if(cell.isdigit()):
                numslist[ref] = int(cell)
                print(numslist)
                red = [ref]
            if(cell == n):
                return render_template("checkcolspuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=True, ans=n,difficulty=dif, blues=[ref], reds= [],grays=g, dif=session["difficulty"])
            else:
                return render_template("checkcolspuzzles.html", nums=numslist,length=len(numslist), lets=letters, result=False, ans=n,difficulty=dif, reds=red, blues=[], grays=g, dif=session["difficulty"] )
@app.route("/puzzles/nakedpairs/<dif>", methods=["GET", "POST"])
def nakedpairspuzzles(dif):
    c = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b")
        if("t" in session):
            session.pop("t")
        if("c" in session):
            session.pop("c")
        if("difficulty" in session):
            session.pop("difficulty", None)
        b = 0
        session["difficulty"] = dif
        session["b"] = b
        if(dif == "easy"):
            a = random.randint(1,5)
            if "nspuz" in session:
                if(a == session["nspuz"]):
                    if(a == 1):
                        a += 1
                    else:
                        a -= 1
            session["nspuz"] = a
            if(a == 1):
                numbers = np.array([4,0,0,0,0,3,0,8,0,0,5,6,0,0,0,0,7,0,8,7,9,0,0,0,5,0,0])
                p = "number"
                c = "B1"
                n = str(int((3+session["b"]-1) % 9) + 1) 
            if(a == 2):
                numbers = np.array([4,5,1,3,6,0,0,8,0,0,0,9,4,0,0,0,7,1,8,0,0,0,0,0,5,3,0])
                p = "number"
                c = "B7"
                n = str(int((6+session["b"]-1) % 9) + 1) 
            if(a == 3):
                numbers = np.array([7,0,2,1,0,0,0,0,5,0,6,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,3,0,0,0,0,0,0,0,0,2,0,0,0,0,0,7,0,0])
                p = "number"
                c = "A2"
                n = str(int((3+session["b"]-1) % 9) + 1)
            if(a == 4):
                numbers = np.array([3,0,7,0,0,0,4,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,5,0,7,0,0,0,5,6,9,0,8,0,0,3,2,0,0,0,6,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,4,0,5,0,0,0,0,0,0,0,0,0,0,9,8,5])
                p = "number"
                c = "E7"
                n = str(int((7+session["b"]-1) % 9) + 1)
            if(a == 5):
                numbers = np.array([0,6,0,0,2,0,0,0,1,0,8,0,0,5,0,0,0,7,0,0,0,0,0,0,0,0,0,7,0,5,0,0,1,0,0,0,1,0,0,0,0,0,7,0,0,0,3,0,0,0,0,0,0,0,0,4,0,9,0,0,0,8,0,6,1,0,4,8,0,0,7,0,8,0,0,0,0,0,0,0,0])
                p = "number"
                c = "F1"
                n = str(int((4+session["b"]-1) % 9) + 1)
        if(dif == "medium"):
            a = random.randint(6,10)
            if "nspuz" in session:
                if(a == session["nspuz"]):
                    if(a == 6):
                        a += 1
                    else:
                        a -= 1
            session["nspuz"] = a
            if(a == 6):
                numbers = np.array([0,0,3,0,5,7,1,4,0,0,5,6,0,0,4,7,0,0,0,2,0,0,0,0,0,0,0])
                c = "B1"   
                p = "cell"
            if(a == 7):
                numbers = np.array([9,1,0,0,0,4,2,6,3,0,0,0,0,1,9,0,0,0,4,0,0,0,7,0,0,0,0])
                c = "A3"
                p = "cell"
            if(a == 8):
                numbers = np.array([0,0,0,0,0,0,7,0,1,4,0,5,3,0,0,0,2,0,1,7,0,0,0,0,9,0,0])
                c = "B2"
                p = "cell"
            if(a == 9):
                numbers = np.array([0,0,0,0,4,0,9,0,0,9,0,0,0,7,0,0,0,1,0,0,8,0,0,0,0,0,0,0,0,0,8,0,9,0,1,0,4,0,0,1,0,6,0,2,0,0,0,0,0,2,7,0,0,0])
                c = "F4"
                p = "cell"
            if(a == 10):
                numbers = np.array([5,2,0,0,0,0,0,6,0,0,7,0,0,3,4,0,0,9,0,0,1,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,4,1,0,0,9,0,0,0,0,9,0,0,0,0,0,8,0,0])
                c = "C1"
                p = "cell"
        if(dif == "hard"):
            a = random.randint(11,15)
            if "nspuz" in session:
                if(a == session["nspuz"]):
                    if(a == 11):
                        a += 1
                    else:
                        a -= 1
            session["nspuz"] = a
            if(a == 11):
                numbers = np.array([7,5,3,0,0,0,0,0,0,0,1,0,0,5,0,0,0,0,0,2,0,0,0,0,0,3,0,0,0,0,0,1,5,0,6,0,0,0,4,0,0,0,0,0,0,2,0,6,0,0,0,0,0,0,0,0,2,0,0,0,7,1,0,0,0,0,5,9,0,0,4,0,0,0,0,0,0,0,0,0,0])
                c = "D3"
                p = "cell"
            if(a == 12):
                numbers = np.array([0,0,0,0,9,0,0,0,0,5,0,7,0,0,0,9,0,1,1,0,0,0,8,0,0,0,0,0,2,0,1,0,0,0,8,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,9,4,3,0,0,0,8,1,7,0,0,1,3,0,0,0,9,2,0,0,6,0,0,0,0,3,0])
                c = "H7"
                p = "cell"
            if(a == 13):
                numbers = np.array([7,0,0,0,0,1,0,0,2,0,0,0,0,4,0,7,5,8,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,6,0,8,0,0,0,1,0,0,2,0,0,0,2,9,0,0,0,0,0,0,7,9,0,0,0,2,0,0,5,1,3,0,7,0,4,0,0,0,0,0,0,0,9,0,0,0])
                c = "B3"
                p = "cell"
            if(a == 14):
                numbers = np.array([0,0,0,0,0,0,0,0,0,0,8,1,4,0,0,0,2,6,0,0,0,2,9,0,8,7,4,0,0,2,3,0,0,0,0,0,4,0,0,0,1,0,0,0,0,1,0,0,0,0,7,0,0,0,0,0,0,6,0,0,0,0,0,0,0,3,8,7,4,9,6,1,0,0,0,0,0,0,0,0,0])
                c = "I4"
                p = "cell"
            if(a == 15):
                numbers = np.array([0,1,4,0,0,0,0,0,0,2,7,0,0,0,0,0,9,0,0,0,0,0,6,0,0,7,3,0,0,0,0,1,0,0,0,0,0,0,0,4,0,2,9,1,0,5,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,2,0,0,5,0,9,0,0,8,0,0])
                c = "C3"
                p = "cell"
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+b-1) % 9 + 1
        if(len(numbers) == 81):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            session["t"] = random.randint(0,2)
            if(session["t"] == 1):
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        session["c"] = random.randint(0,2)
        print(session["c"])
        if(session["c"] == 1):
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
            c = c[0] + newcol
        if(session["c"] == 2):
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("nakedpairspuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
        cell = request.form["cell"]
        if(session["nspuz"] == 1):
            numbers = np.array([4,0,0,0,0,3,0,8,0,0,5,6,0,0,0,0,7,0,8,7,9,0,0,0,5,0,0])
            p = "number"
            c = "B1"
            n = str(int((3+session["b"]-1) % 9) + 1) 
            ref = 9
            nakedpairref = [1,2]
            nakedpairoptions = str(int((1+session["b"]-1) % 9) + 1) + str(int((2+session["b"]-1) % 9) + 1)
            
        if(session["nspuz"] == 2):
            numbers = np.array([4,5,1,3,6,0,0,8,0,0,0,9,0,0,0,0,7,1,8,0,0,0,0,0,5,3,0])
            p = "number"
            c = "B7"
            n = str(int((6+session["b"]-1) % 9) + 1)
            ref = 15
            nakedpairref = [6,8]
            nakedpairoptions = str(int((2+session["b"]-1) % 9) + 1) + str(int((9+session["b"]-1) % 9) + 1)
            
        if(session["nspuz"] == 3):
            numbers = np.array([7,0,2,1,0,0,0,0,5,0,6,0,0,0,0,0,0,0,0,8,4,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,3,0,0,0,0,0,0,0,0,2,0,0,0,0,0,7,0,0])
            p = "number"
            c = "A2"
            n = str(int((3+session["b"]-1) % 9) + 1)
            ref = 1
            nakedpairref = [9,18]
            nakedpairoptions = str(int((5+session["b"]-1) % 9) + 1) + str(int((9+session["b"]-1) % 9) + 1)
            
        if(session["nspuz"] == 4):
            numbers = np.array([3,0,7,0,0,0,4,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,5,0,7,0,0,0,5,6,9,0,8,0,0,3,2,0,0,0,6,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,4,0,5,0,0,0,0,0,0,0,0,0,0,9,8,5])
            p = "number"
            c = "E7"
            n = str(int((7+session["b"]-1) % 9) + 1)
            ref = 42
            nakedpairref = [39,41]
            nakedpairoptions = str(int((1+session["b"]-1) % 9) + 1) + str(int((4+session["b"]-1) % 9) + 1)
            
        if(session["nspuz"] == 5):
            numbers = np.array([0,6,0,0,2,0,0,0,1,0,8,0,0,5,0,0,0,7,0,0,0,0,0,0,0,0,0,7,0,5,0,0,1,0,0,0,1,0,0,0,0,0,7,0,0,0,3,0,0,0,0,0,0,0,0,4,0,9,0,0,0,8,0,6,1,0,4,8,0,0,7,0,8,0,0,0,0,0,0,0,0])
            p = "number"
            c = "F1"
            n = str(int((4+session["b"]-1) % 9) + 1)
            ref = 45
            nakedpairref = [28,37]
            nakedpairoptions = str(int((2+session["b"]-1) % 9) + 1) + str(int((9+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 6):
            numbers = np.array([0,0,3,0,5,7,1,4,0,0,5,6,0,0,4,7,0,0,0,2,0,0,0,0,0,0,0])
            c = "B1"   
            p = "cell"
            ref = 9
            nakedpairref = [0,1]
            nakedpairoptions = str(int((8+session["b"]-1) % 9) + 1) + str(int((9+session["b"]-1) % 9) + 1)
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 7):
            numbers = np.array([9,1,0,0,0,4,2,6,3,0,0,0,0,1,9,0,0,0,4,0,0,0,7,0,0,0,0])
            c = "A3"
            p = "cell"
            ref = 2
            nakedpairref = [3,4]
            nakedpairoptions = str(int((5+session["b"]-1) % 9) + 1) + str(int((8+session["b"]-1) % 9) + 1)
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 8):
            numbers = np.array([0,0,0,0,0,0,7,0,1,4,0,5,3,0,0,0,2,0,1,7,0,0,0,0,9,0,0])
            c = "B2"
            p = "cell"
            ref = 10
            nakedpairref = [15,17]
            nakedpairoptions = str(int((6+session["b"]-1) % 9) + 1) + str(int((8+session["b"]-1) % 9) + 1)
            n = str(int((9+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 9):
            numbers = np.array([0,0,0,0,4,0,9,0,0,9,0,0,0,7,0,0,0,1,0,0,8,0,0,0,0,0,0,0,0,0,8,0,9,0,1,0,4,0,0,1,0,6,0,2,0,0,0,0,0,2,7,0,0,0])
            c = "F4"
            p = "cell"
            ref = 48
            nakedpairref = [31,40]
            nakedpairoptions = str(int((3+session["b"]-1) % 9) + 1) + str(int((5+session["b"]-1) % 9) + 1)
            n = str(int((4+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 10):
            numbers = np.array([5,2,0,0,0,0,0,6,0,0,7,0,0,3,4,0,0,9,0,0,1,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,4,1,0,0,9,0,0,0,0,9,0,0,0,0,0,8,0,0])
            c = "C1"
            p = "cell"
            ref = 18
            nakedpairref = [9,11]
            nakedpairoptions = str(int((6+session["b"]-1) % 9) + 1) + str(int((8+session["b"]-1) % 9) + 1)
            n = str(int((3+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 11):
            numbers = np.array([7,5,3,0,0,0,0,0,0,0,1,0,0,5,0,0,0,0,0,2,0,0,0,0,0,3,0,0,0,0,0,1,5,0,6,0,0,0,4,0,0,0,0,0,0,2,0,6,0,0,0,0,0,0,0,0,2,0,0,0,7,1,0,0,0,0,5,9,0,0,4,0,0,0,0,0,0,0,0,0,0])
            c = "D3"
            p = "cell"
            ref = 29
            nakedpairref = [11,20]
            nakedpairoptions = str(int((8+session["b"]-1) % 9) + 1) + str(int((9+session["b"]-1) % 9) + 1)
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 12):
            numbers = np.array([0,0,0,0,9,0,0,0,0,5,0,7,0,0,0,9,0,1,1,0,0,0,8,0,0,0,0,0,2,0,1,0,0,5,8,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,9,4,3,0,0,0,8,1,7,0,0,1,3,0,0,0,9,2,0,0,6,0,0,0,0,3,0])
            c = "H7"
            p = "cell"
            ref = 69
            nakedpairref = [78,80]
            nakedpairoptions = str(int((4+session["b"]-1) % 9) + 1) + str(int((5+session["b"]-1) % 9) + 1)
            n = str(int((6+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 13):
            numbers = np.array([7,0,0,0,0,1,0,0,2,0,0,0,0,4,0,7,5,8,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,6,0,8,0,0,0,1,0,0,2,0,0,0,2,9,0,0,0,0,0,0,7,9,0,0,0,2,0,0,5,1,3,0,7,0,4,0,0,0,0,0,0,0,9,0,0,0])
            c = "B3"
            p = "cell"
            ref = 11
            nakedpairref = [12,14]
            nakedpairoptions = str(int((3+session["b"]-1) % 9) + 1) + str(int((6+session["b"]-1) % 9) + 1)
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 14):
            numbers = np.array([0,0,0,0,0,0,0,0,0,0,8,1,4,0,0,0,2,6,0,0,0,2,9,0,8,7,4,0,0,2,3,0,0,0,0,0,4,0,0,0,1,0,0,0,0,1,0,0,0,0,7,0,0,0,0,0,0,6,0,0,0,0,0,0,0,3,8,7,4,9,6,1,0,0,0,0,0,0,0,0,0])
            c = "I4"
            p = "cell"
            ref = 75
            nakedpairref = [39,48]
            nakedpairoptions = str(int((5+session["b"]-1) % 9) + 1) + str(int((9+session["b"]-1) % 9) + 1)
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["nspuz"] == 15):
            numbers = np.array([0,1,4,0,0,0,0,0,0,2,7,0,0,0,0,0,9,0,0,0,0,0,6,0,0,7,3,0,0,0,0,1,0,0,0,0,0,0,0,4,0,2,9,1,0,5,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,2,0,0,5,0,9,0,0,8,0,0])
            c = "C3"
            p = "cell"
            ref = 20
            nakedpairref = [18,19]
            nakedpairoptions = str(int((8+session["b"]-1) % 9) + 1) + str(int((9+session["b"]-1) % 9) + 1)
            n = str(int((5+session["b"]-1) % 9) + 1)
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if("t" in session):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            if(session["t"] == 1):
                ref = (ref+54) % 81
                nakedpairref[0] = (nakedpairref[0] + 54) % 81
                nakedpairref[1] = (nakedpairref[1] + 54) % 81
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                ref = (ref+27) % 81
                nakedpairref[0] = (nakedpairref[0] + 27) % 81
                nakedpairref[1] = (nakedpairref[1] + 27) % 81
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        print(session["c"])
        if(session["c"] == 1):
            ref = 9*(ref//9) + (ref+6)%9
            nakedpairref[0] = 9*(nakedpairref[0]//9) + (nakedpairref[0]+6)%9
            nakedpairref[1] = 9*(nakedpairref[1]//9) + (nakedpairref[1]+6)%9
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        if(session["c"] == 2):
            ref = 9*(ref//9) + (ref+3)%9
            nakedpairref[0] = 9*(nakedpairref[0]//9) + (nakedpairref[0]+3)%9
            nakedpairref[1] = 9*(nakedpairref[1]//9) + (nakedpairref[1]+3)%9
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(g)
        numslist[nakedpairref[0]] = int(nakedpairoptions)
        numslist[nakedpairref[1]] = int(nakedpairoptions)
        if(p == "cell"):
            numslist[ref] = int(n)
            
            if(cell == c):
                return render_template("nakedpairspuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=True, ans=c,difficulty=dif, blues=nakedpairref, reds=[], grays=g, dif=session["difficulty"])
            else:
                return render_template("nakedpairspuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=False, ans=c,difficulty=dif, blues=nakedpairref, reds=[], grays=g, dif=session["difficulty"])
        else:
            red = []
            if(cell.isdigit()):
                numslist[ref] = int(cell)
                print(numslist)
                red = [ref]
            if(cell == n):
                nakedpairref.append(ref)
                return render_template("nakedpairspuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=True, ans=n,difficulty=dif, blues=nakedpairref, reds= [],grays=g, dif=session["difficulty"])
            else:
                return render_template("nakedpairspuzzles.html", nums=numslist,length=len(numslist), lets=letters, result=False, ans=n,difficulty=dif, reds=red, blues=nakedpairref, grays=g, dif=session["difficulty"], )
@app.route("/puzzles/hiddenpairs/<dif>", methods=["GET", "POST"])
def hiddenpairspuzzles(dif):
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b")
        if("c" in session):
            session.pop("c")
        if("difficulty" in session):
            session.pop("difficulty", None)
        if("t" in session):
            session.pop("t")
        session["b"] = 0
        session["difficulty"] = dif
        numbers = np.array([1,0,3,0,0,6,0,4,0,0,5,0,2,7,0,0,0,0,0,0,8,0,0,0,6,5,9])
        p = "cell"
        c = "A2"
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if(len(numbers) == 81):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            session["t"] = random.randint(0,2)
            if(session["t"] == 1):
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        session["c"] = random.randint(0,2)
        print(session["c"])
        if(session["c"] == 1):
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
            c = c[0] + newcol
        if(session["c"] == 2):
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("hiddenpairspuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
        cell = request.form["cell"]
        numbers = np.array([1,0,3,0,0,6,0,4,0,0,5,0,2,7,0,0,0,0,0,0,8,0,0,0,6,5,9])
        p = "cell"
        c = "A2"
        n = str(int((9+session["b"]-1)%9) + 1)
        ref = 1
        nakedpairref = [6,8]
        nakedpairoptions = str(int((2+session["b"]-1) % 9) + 1) + str(int((7+session["b"]-1) % 9) + 1)
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if("t" in session):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            if(session["t"] == 1):
                ref = (ref+54) % 81
                nakedpairref[0] = (nakedpairref[0] + 54) % 81
                nakedpairref[1] = (nakedpairref[1] + 54) % 81
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                ref = (ref+27) % 81
                nakedpairref[0] = (nakedpairref[0] + 27) % 81
                nakedpairref[1] = (nakedpairref[1] + 27) % 81
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        print(session["c"])
        if(session["c"] == 1):
            ref = 9*(ref//9) + (ref+6)%9
            nakedpairref[0] = 9*(nakedpairref[0]//9) + (nakedpairref[0]+6)%9
            nakedpairref[1] = 9*(nakedpairref[1]//9) + (nakedpairref[1]+6)%9
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        if(session["c"] == 2):
            ref = 9*(ref//9) + (ref+3)%9
            nakedpairref[0] = 9*(nakedpairref[0]//9) + (nakedpairref[0]+3)%9
            nakedpairref[1] = 9*(nakedpairref[1]//9) + (nakedpairref[1]+3)%9
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        numslist[ref] = int(n)
        numslist[nakedpairref[0]] = nakedpairoptions
        numslist[nakedpairref[1]] = nakedpairoptions
        nakedpairref.append(ref)
        if(c == cell):
            return render_template("hiddenpairspuzzles.html",nums=numslist, length=len(numslist), grays = g, lets=letters, result=True, ans=c,difficulty=dif, blues=nakedpairref, reds=[])
        else:
            return render_template("hiddenpairspuzzles.html",nums=numslist, length=len(numslist), grays = g, lets=letters, result=True, ans=c,difficulty=dif, blues=nakedpairref, reds=[])
@app.route("/puzzles/boxreduction/<dif>", methods=["GET", "POST"])
def boxreductionpuzzles(dif):
    c = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b")
        if("t" in session):
            session.pop("t")
        if("c" in session):
            session.pop("c")
        if("difficulty" in session):
            session.pop("difficulty", None)
        b = 0
        session["difficulty"] = dif
        session["b"] = b
        if(dif == "easy"):
            a = random.randint(1,5)
            if "brpuz" in session:
                if(a == session["brpuz"]):
                    if(a == 1):
                        a += 1
                    else:
                        a -= 1
            session["brpuz"] = a
            if(a == 1):
                numbers = np.array([1,0,0,7,4,0,0,5,9,0,0,0,6,0,0,8,0,0,5,3,8,0,0,0,2,0,0])
                c = "A7"
                n = str(int((3+session["b"]-1) % 9) + 1) 
                p = "number"
            if(a == 2):
                numbers = np.array([4,0,0,0,0,0,0,9,3,0,0,0,0,0,5,8,7,6,3,8,6,7,0,0,1,0,0])
                c = "A7"
                n = str(int((2+session["b"]-1) % 9) + 1) 
                p = "number"
            if(a == 3):
                numbers = np.array([6,0,0,0,4,0,0,0,0,0,2,0,0,0,0,0,1,0,4,0,0,0,0,0,0,0,0,0,5,9,0,0,0,0,0,8,0,0,2,4,5,6,0,0,0,0,0,0,0,7,0,1,0,0])
                c = "F1"
                n = str(int((3+session["b"]-1) % 9) + 1) 
                p = "number"
            if(a == 4):
                numbers = np.array([9,0,1,0,3,5,0,0,8,6,0,0,0,0,0,5,7,9,0,0,2,0,0,4,0,0,0])
                c = "A2"
                n = str(int((7+session["b"]-1) % 9) + 1) 
                p = "number"
            if(a == 5):
                numbers = np.array([0,0,0,0,0,0,3,0,0,0,7,4,0,0,0,0,0,9,0,8,1,5,0,0,0,0,0,0,0,6,2,5,0,8,0,4,0,9,7,0,0,0,0,0,0,0,0,0,7,1,0,0,0,0])
                c = "D1"
                n = str(int((1+session["b"]-1) % 9) + 1) 
                p = "number"
        if(dif == "medium"):
            a = random.randint(6,10)
            if "brpuz" in session:
                if(a == session["brpuz"]):
                    if(a == 6):
                        a += 1
                    else:
                        a -= 1
            session["brpuz"] = a
            if(a == 6):
                numbers = np.array([0,3,0,0,0,0,9,8,0,0,0,0,7,9,6,0,5,0,4,0,7,0,0,0,0,6,2])
                c = "C7"
                p = "cell"
            if(a == 7):
                numbers = np.array([9,8,0,0,5,0,4,0,0,0,0,0,0,4,0,3,0,0,0,0,5,0,0,0,1,0,0,3,6,1,0,0,0,5,0,0,0,0,0,0,0,7,0,0,0,0,2,0,8,0,0,0,9,0])
                c = "F7"
                p = "cell"
            if(a == 8):
                numbers = np.array([4,7,0,0,6,0,2,0,0,0,1,0,7,3,8,0,0,0,0,0,0,0,0,0,0,0,9,0,0,3,0,1,0,0,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,7])
                c = "A3"
                p = "cell"
            if(a == 9):
                numbers = np.array([1,0,0,0,0,0,0,0,2,0,3,0,9,5,6,0,0,4,8,6,9,0,0,0,7,5,0])
                c = "C9"
                p = "cell"
            if(a == 10):
                numbers = np.array([4,0,0,0,3,9,7,1,0,5,6,9,0,0,0,2,0,0,0,0,0,8,0,0,0,6,0])
                c = "A9"
                p = "cell"
        if(dif == "hard"):
            a = random.randint(11,15)
            if "brpuz" in session:
                if(a == session["brpuz"]):
                    if(a == 11):
                        a += 1
                    else:
                        a -= 1
            session["brpuz"] = a
            if(a == 11):
                numbers = np.array([7,0,0,1,4,0,8,0,5,0,0,0,2,0,0,0,0,3,5,9,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,4,5,0,0,0,2,0,6,0,0,0,4,0,0])
                c = "A6"
                p = "cell"
            if(a == 12):
                numbers = np.array([0,6,0,0,0,0,8,0,0,0,0,0,0,0,0,7,0,0,0,5,0,0,1,0,0,0,0,0,0,9,0,0,0,0,0,3,0,3,0,1,2,7,0,0,0,2,0,0,0,0,0,0,4,0,0,0,0,0,0,0,5,0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,1,6,9])
                c = "F7"
                p = "cell"
            if(a == 13):
                numbers = np.array([0,1,0,0,0,0,0,0,0,5,0,2,0,4,0,7,0,0,0,9,0,0,0,0,3,6,1,0,0,0,2,0,6,0,0,0,0,0,0,0,0,0,0,7,0,3,0,0,0,9,0,0,0,0,0,0,1,0,7,0,0,0,0,0,8,9,0,0,1,0,0,0,0,0,4,0,0,0,1,6,9])
                c = "B2"
                p = "cell"
            if(a == 14):
                numbers = np.array([5,0,0,0,0,0,0,0,7,0,0,0,0,0,0,4,0,0,0,0,9,0,0,0,2,0,0,7,0,0,0,0,0,9,0,6,0,5,0,0,0,0,0,2,0,0,6,0,0,0,0,1,0,4,0,0,1,8,0,0,0,0,9,0,0,4,0,0,0,0,3,0,0,0,5,7,2,4,0,0,0])
                c = "E3"
                p = "cell"
            if(a == 15):
                numbers = np.array([0,0,0,0,0,7,0,0,9,2,9,5,0,0,0,0,3,0,0,0,0,0,5,4,0,1,2,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2,0,0,0,9,0,0,0,7,0,0,0,0,8,9,0,0,4,8,2,9,3,0,0,0,1,0,9,0,0,0,0,4,0])
                c = "C7"
                p = "cell"
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+b-1) % 9 + 1
        if(len(numbers) == 81):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            session["t"] = random.randint(0,2)
            if(session["t"] == 1):
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        session["c"] = random.randint(0,2)
        print(session["c"])
        if(session["c"] == 1):
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
            c = c[0] + newcol
        if(session["c"] == 2):
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("boxelimpuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
        cell = request.form["cell"]
        if(session["brpuz"] == 1):
            numbers = np.array([1,0,0,7,4,0,0,5,9,0,0,0,6,0,0,8,0,0,5,3,8,0,0,0,2,0,0])
            c = "A7"
            n = str(int((3+session["b"]-1) % 9) + 1) 
            p = "number"            
            ref = 6
        if(session["brpuz"] == 2):
            numbers = np.array([4,0,0,0,0,0,0,9,3,0,0,0,0,0,5,8,7,6,3,8,6,7,0,0,1,0,0])
            c = "A7"
            n = str(int((2+session["b"]-1) % 9) + 1) 
            p = "number"
            ref = 6
        if(session["brpuz"] == 3):
            numbers = np.array([6,0,0,0,4,0,0,0,0,0,2,0,0,0,0,0,1,0,4,0,0,0,0,0,0,0,0,0,5,9,0,0,0,0,0,8,0,0,2,4,5,6,0,0,0,0,0,0,0,7,0,1,0,0])
            c = "F1"
            n = str(int((3+session["b"]-1) % 9) + 1) 
            p = "number"
            ref = 45
        if(session["brpuz"] == 4):
            numbers = np.array([9,0,1,0,3,5,0,0,8,6,0,0,0,0,0,5,7,9,0,0,2,0,0,4,0,0,0])
            c = "A2"
            n = str(int((7+session["b"]-1) % 9) + 1) 
            p = "number"
            ref = 1
        if(session["brpuz"] == 5):
            numbers = np.array([0,0,0,0,0,0,3,0,0,0,7,4,0,0,0,0,0,9,0,8,1,5,0,0,0,0,0,0,0,6,2,5,0,8,0,4,0,9,7,0,0,0,0,0,0,0,0,0,7,1,0,0,0,0])
            c = "D1"
            n = str(int((1+session["b"]-1) % 9) + 1) 
            p = "number"
            ref = 27
        if(session["brpuz"] == 6):
            numbers = np.array([0,3,0,0,0,0,9,8,0,0,0,0,7,9,6,0,5,0,4,0,7,0,0,0,0,6,2])
            c = "C7"
            p = "cell"
            ref = 24
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["brpuz"] == 7):
            numbers = np.array([9,8,0,0,5,0,4,0,0,0,0,0,0,4,0,3,0,0,0,0,5,0,0,0,1,0,0,3,6,1,0,0,0,5,0,0,0,0,0,0,0,7,0,0,0,0,2,0,8,0,0,0,9,0])
            c = "F7"        
            p = "cell"
            ref = 51
            n = str(int((6+session["b"]-1) % 9) + 1)
        if(session["brpuz"] == 8):
            numbers = np.array([4,7,0,0,6,0,2,0,0,0,1,0,7,3,8,0,0,0,0,0,0,0,0,0,0,0,9,0,0,3,0,1,0,0,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,7])
            c = "A3"
            p = "cell"
            ref = 2
            n = str(int((8+session["b"]-1) % 9) + 1)
        if(session["brpuz"] == 9):
            numbers = np.array([1,0,0,0,0,0,0,0,2,0,3,0,9,5,6,0,0,4,8,6,9,0,0,0,7,5,0])
            c = "C9"
            p = "cell"
            ref = 26
            n = str(int((3+session["b"]-1) % 9) + 1)
        if(session["brpuz"] == 10):
            numbers = np.array([4,0,0,0,3,9,7,1,0,5,6,9,0,0,0,2,0,0,0,0,0,8,0,0,0,6,0])
            c = "A9"
            p = "cell"
            ref = 8
            n = str(int((5+session["b"]-1) % 9) + 1)
        if(session["brpuz"] == 11):
            numbers = np.array([7,0,0,1,4,0,8,0,5,0,0,0,2,0,0,0,0,3,5,9,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,4,5,0,0,0,2,0,6,0,0,0,4,0,0])
            c = "A6"
            p = "cell"
            ref = 5
            n = str(int((9+session["b"]-1) % 9) + 1)
        if(session["brpuz"] == 12):
            numbers = np.array([0,6,0,0,0,0,8,0,0,0,0,0,0,0,0,7,0,0,0,5,0,0,1,0,0,0,0,0,0,9,0,0,0,0,0,3,0,3,0,1,2,7,0,0,0,2,0,0,0,0,0,0,4,0,0,0,0,0,0,0,5,0,0,0,8,0,0,0,0,0,0,0,0,0,0,8,0,0,1,6,9])
            c = "F7"
            p = "cell"
            ref = 51
            n = str(int((6+session["b"]-1) % 9) + 1)
        if(session["brpuz"] == 13):
            numbers = np.array([0,1,0,0,0,0,0,0,0,5,0,2,0,4,0,7,0,0,0,9,0,0,0,0,3,6,1,0,0,0,2,0,6,0,0,0,0,0,0,0,0,0,0,7,0,3,0,0,0,9,0,0,0,0,0,0,1,0,7,0,0,0,0,0,8,9,0,0,1,0,0,0,0,0,4,0,0,0,1,6,9])
            c = "B2"
            p = "cell"
            ref = 10
            n = str(int((6+session["b"]-1) % 9) + 1)
        if(session["brpuz"] == 14):
            numbers = np.array([5,0,0,0,0,0,0,0,7,0,0,0,0,0,0,4,0,0,0,0,9,0,0,0,2,0,0,7,0,0,0,0,0,9,0,6,0,5,0,0,0,0,0,2,0,0,6,0,0,0,0,1,0,4,0,0,1,8,0,0,0,0,9,0,0,4,0,0,0,0,3,0,0,0,5,7,2,4,0,0,0])
            c = "E3"
            p = "cell"
            ref = 38
            n = str(int((8+session["b"]-1) % 9) + 1)
        if(session["brpuz"] == 15):
            numbers = np.array([0,0,0,0,0,7,0,0,9,2,9,5,0,0,0,0,3,0,0,0,0,0,5,4,0,1,2,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2,0,0,0,9,0,0,0,7,0,0,0,0,8,9,0,0,4,8,2,9,3,0,0,0,1,0,9,0,0,0,0,4,0])
            c = "C7"
            p = "cell"
            ref = 24
            n = str(int((6+session["b"]-1) % 9) + 1)
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if("t" in session):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            if(session["t"] == 1):
                ref = (ref+54) % 81
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                ref = (ref+27) % 81
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        print(session["c"])
        if(session["c"] == 1):
            ref = 9*(ref//9) + (ref+6)%9
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        if(session["c"] == 2):
            ref = 9*(ref//9) + (ref+3)%9
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(g)
        if(p == "cell"):
            numslist[ref] = int(n)
            
            if(cell == c):
                return render_template("boxelimpuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=True, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
            else:
                return render_template("boxelimpuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=False, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
        else:
            red = []
            if(cell.isdigit()):
                numslist[ref] = int(cell)
                print(numslist)
                red = [ref]
            if(cell == n):
                return render_template("boxelimpuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=True, ans=n,difficulty=dif, blues=[ref], reds= [],grays=g, dif=session["difficulty"])
            else:
                return render_template("boxelimpuzzles.html", nums=numslist,length=len(numslist), lets=letters, result=False, ans=n,difficulty=dif, reds=red, blues=[], grays=g, dif=session["difficulty"] )
@app.route("/puzzles/colreduction/<dif>", methods=["GET", "POST"])
def colreductionpuzzles(dif):
    c = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b")
        if("t" in session):
            session.pop("t")
        if("c" in session):
            session.pop("c")
        if("difficulty" in session):
            session.pop("difficulty", None)
        b = 0
        session["difficulty"] = dif
        session["b"] = b
        if(dif == "easy"):
            a = random.randint(1,5)
            if "cepuz" in session:
                if(a == session["cepuz"]):
                    if(a == 1):
                        a += 1
                    else:
                        a -= 1
            session["cepuz"] = a
            if(a == 1):
                numbers = np.array([8,9,2,0,6,0,0,0,1,0,0,3,5,0,0,0,0,0,0,2,4,0,8,0,0,3,0])
                c = "B3"
                p = "number"
                n = str(int((7+session["b"]-1) % 9) + 1) 
            if(a == 2):
                numbers = np.array([5,0,0,0,6,0,0,7,0,4,0,0,0,0,0,0,0,1,0,2,0,9,0,6,3,0,7])
                c = "G1"
                p = "number"
                n = str(int((8+session["b"]-1) % 9) + 1) 
            if(a == 3):
                numbers = np.array([0,0,0,5,4,0,7,0,0,0,2,3,0,9,8,0,0,0,0,0,9,0,0,0,0,0,0,0,1,0,0,0,0,6,0,0,0,0,4,0,0,7,9,0,6,0,0,4,0,0,7,0,0,5])
                c = "C4"
                p = "number"
                n = str(int((7+session["b"]-1) % 9) + 1) 
            if(a == 4):
                numbers = np.array([1,2,0,7,0,0,0,0,0,0,0,0,0,1,0,4,6,0,9,0,0,0,0,0,5,0,0,0,0,1,0,0,0,0,9,0,0,0,7,0,0,0,0,2,8,0,3,0,8,4,0,0,7,0,0,5,0,0,0,0,9,0,0,0,1,0,0,5,0,0,0,3,0,0,0,0,0,1,0,0,0])
                c = "A7"
                p = "number"
                n = str(int((8+session["b"]-1) % 9) + 1) 
            if(a == 5):
                numbers = np.array([0,0,3,0,0,0,0,4,0,0,0,0,0,0,3,0,7,0,9,0,0,0,0,0,0,3,1,0,1,0,4,0,0,0,0,0,0,0,0,0,9,0,0,0,2,0,3,0,0,0,0,0,0,9,1,0,0,0,2,5,7,0,0,0,0,8,0,0,0,0,5,0,5,4,0,0,0,0,0,0,0])
                c = "G3"
                p = "number"
                n = str(int((6+session["b"]-1) % 9) + 1) 
        if(dif == "medium"):
            a = random.randint(6,10)
            if "cepuz" in session:
                if(a == session["cepuz"]):
                    if(a == 6):
                        a += 1
                    else:
                        a -= 1
            session["cepuz"] = a
            if(a == 6):
                numbers = np.array([8,0,0,9,0,0,4,5,0,0,4,6,0,3,0,0,0,0,1,2,0,0,7,9,0,0,0])
                c = "I2"
                p = "cell"
            if(a == 7):
                numbers = np.array([0,7,6,2,0,8,0,0,0,0,0,3,0,4,1,0,0,7,9,0,0,7,0,5,3,0,0])
                c = "C3"
                p = "cell"
            if(a == 8):
                numbers = np.array([0,3,0,7,1,0,0,5,0,4,0,0,0,0,6,0,0,0,0,2,0,5,0,1,3,0,9])
                c = "G1"
                p = "cell"
            if(a == 9):
                numbers = np.array([5,0,0,0,0,0,0,1,6,0,8,0,4,2,0,0,0,1,0,0,0,0,5,0,7,0,0,3,9,0,0,8,0,0,4,0,3,0,0,5,0,0,9,0,0,6,0,7,0,0,0,0,0,0])
                c = "C4"
                p = "cell"
            if(a == 10):
                numbers = np.array([3,0,0,0,0,0,0,0,0,9,0,4,2,0,0,0,6,0,0,0,0,5,0,0,6,3,7,1,2,0,1,0,0,0,0,0,0,9,0,0,8,0,0,2,0,0,1,0,0,0,0,0,7,0])
                c = "E6"
                p = "cell"
        if(dif == "hard"):
            a = random.randint(11,15)
            if "cepuz" in session:
                if(a == session["cepuz"]):
                    if(a == 11):
                        a += 1
                    else:
                        a -= 1
            session["cepuz"] = a
            if(a == 11):
                numbers = np.array([7,0,0,0,0,5,0,0,1,0,1,3,0,0,0,0,0,0,0,0,0,0,8,1,0,0,0,0,0,0,3,0,0,1,5,0,0,0,9,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,4,0,0,0,0,2,5,1,0,0,9,0,0,0,0,9,0,0,0,0,0])
                c = "G5"
                p = "cell"
            if(a == 12):
                numbers = np.array([2,0,0,0,0,9,0,0,0,0,4,0,0,7,8,2,3,0,0,5,0,0,0,1,0,6,0,8,0,0,0,0,0,0,0,0,3,0,0,6,0,0,0,4,0,4,0,0,0,0,0,0,0,1,0,9,0,0,0,0,5,0,0,0,0,0,7,3,0,0,2,9,0,0,6,0,0,0,0,0,0])
                c = "B3"
                p = "cell"
            if(a == 13):
                numbers = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,6,0,0,1,0,0,0,0,0,0,3,0,0,0,3,0,0,0,0,0,1,0,0,4,0,0,0,2,9,0,0,0,7,0,0,0,0,0,0,4,0,8,2,0,1,5,0,0,0,0,0,7,0,0,0,2,2,0,0,0,6,0,0,0,0])
                c = "G6"
                p = "cell"
            if(a == 14):
                numbers = np.array([0,0,0,1,0,0,0,0,0,0,8,0,0,0,0,3,0,6,9,0,0,0,3,0,0,0,0,0,0,7,0,0,0,4,1,0,0,0,6,0,9,0,5,0,0,0,0,5,0,0,0,0,0,0,5,0,1,2,4,0,0,0,7,0,0,0,0,0,0,0,3,0,0,6,0,0,0,0,0,0,0])
                c = "G2"
                p = "cell"
            if(a == 15):
                numbers = np.array([0,0,2,0,0,0,0,0,0,5,0,0,4,0,3,2,0,7,9,0,0,2,0,0,0,0,0,0,0,3,0,2,0,1,0,0,0,0,1,0,4,0,0,2,0,2,0,7,0,6,0,0,0,0,6,2,0,0,0,0,0,5,0,0,0,0,0,7,4,0,0,2,0,8,0,0,0,2,0,0,0])
                c = "B2"
                p = "cell"
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+b-1) % 9 + 1
        tempnum = copy.deepcopy(numbers)
        newrow = ""
        print(c)
        session["t"] = random.randint(0,2)
        print(session["t"])
        if(session["t"] == 1):
            for i in range(2*len(numbers) // 3):
                numbers[i] = int(tempnum[i+len(numbers) // 3])
            for i in range(2*len(numbers) // 3,len(numbers)):
                numbers[i] = int(tempnum[i-2*len(numbers) // 3])
            for i in range(9):
               if(c[0] == letters[i]):
                   newrow = letters[(i+6)%9]
            c = newrow + c[1]
        if(session["t"] == 2):
            for i in range(len(numbers) // 3):
                numbers[i] = int(tempnum[i+2*len(numbers) // 3])
            for i in range(len(numbers) // 3,len(numbers)):
                numbers[i] = int(tempnum[i-len(numbers) // 3])
            for i in range(9):
               if(c[0] == letters[i]):
                   newrow = letters[(i+3)%9]
            c = newrow + c[1]
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("colelimpuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
        n = ""
        cell = request.form["cell"]
        if(session["cepuz"] == 1):
            numbers = np.array([8,9,2,0,6,0,0,0,1,0,0,3,5,0,0,0,0,0,0,2,4,0,8,0,0,3,0])
            c = "B3"
            p = "number"
            n = str(int((7+session["b"]-1) % 9) + 1) 
            ref = 5
        if(session["cepuz"] == 2):
            numbers = np.array([5,0,0,0,6,0,0,7,0,4,0,0,0,0,0,0,0,1,0,2,0,9,0,6,3,0,7])
            c = "G1"
            p = "number"
            n = str(int((8+session["b"]-1) % 9) + 1) 
            ref = 18
        if(session["cepuz"] == 3):
            numbers = np.array([0,0,0,5,4,0,7,0,0,0,2,3,0,9,8,0,0,0,0,0,9,0,0,0,0,0,0,0,1,0,0,0,0,6,0,0,0,0,4,0,0,7,9,0,6,0,0,4,0,0,7,0,0,5])
            c = "C4"
            p = "number"
            n = str(int((7+session["b"]-1) % 9) + 1) 
            ref = 15
        if(session["cepuz"] == 4):
            numbers = np.array([1,2,0,7,0,0,0,0,0,0,0,0,0,1,0,4,6,0,9,0,0,0,0,0,5,0,0,0,0,1,0,0,0,0,9,0,0,0,7,0,0,0,0,2,8,0,3,0,8,4,0,0,7,0,0,5,0,0,0,0,9,0,0,0,1,0,0,5,0,0,0,3,0,0,0,0,0,1,0,0,0])
            c = "A7"
            p = "number"
            n = str(int((8+session["b"]-1) % 9) + 1) 
            ref = 6
        if(session["cepuz"] == 5):
            numbers = np.array([0,0,3,0,0,0,0,4,0,0,0,0,0,0,3,0,7,0,9,0,0,0,0,0,0,3,1,0,1,0,4,0,0,0,0,0,0,0,0,0,9,0,0,0,2,0,3,0,0,0,0,0,0,9,1,0,0,0,2,5,7,0,0,0,0,8,0,0,0,0,5,0,5,4,0,0,0,0,0,0,0])
            c = "G3"
            p = "number"
            n = str(int((6+session["b"]-1) % 9) + 1) 
            ref = 56
        if(session["cepuz"] == 6):
            numbers = np.array([8,0,0,9,0,0,4,5,0,0,4,6,0,3,0,0,0,0,1,2,0,0,7,9,0,0,0])
            c = "I2"
            p = "cell"
            ref = 25
            n = str(int((8+session["b"]-1) % 9) + 1)
        if(session["cepuz"] == 7):
            numbers = np.array([0,7,6,2,0,8,0,0,0,0,0,3,0,4,1,0,0,7,9,0,0,7,0,5,3,0,0])
            c = "C3"
            p = "cell"
            ref = 8
            n = str(int((9+session["b"]-1) % 9) + 1) 
        if(session["cepuz"] == 8):
            numbers = np.array([0,3,0,7,1,0,0,5,0,4,0,0,0,0,6,0,0,0,0,2,0,5,0,1,3,0,9])
            c = "G1"
            p = "cell"
            ref = 18
            n = str(int((8+session["b"]-1) % 9) + 1) 
        if(session["cepuz"] == 9):
            numbers = np.array([5,0,0,0,0,0,0,1,6,0,8,0,4,2,0,0,0,1,0,0,0,0,5,0,7,0,0,3,9,0,0,8,0,0,4,0,3,0,0,5,0,0,9,0,0,6,0,7,0,0,0,0,0,0])
            c = "C4"
            p = "cell"
            ref = 15
            n = str(int((9+session["b"]-1) % 9) + 1) 
        if(session["cepuz"] == 10):
            numbers = np.array([3,0,0,0,0,0,0,0,0,9,0,4,2,0,0,0,6,0,0,0,0,5,0,0,6,3,7,1,2,0,1,0,0,0,0,0,0,9,0,0,8,0,0,2,0,0,1,0,0,0,0,0,7,0])
            c = "E6"
            p = "cell"
            ref = 29
            n = str(int((8+session["b"]-1) % 9) + 1)
        if(session["cepuz"] == 11):
            numbers = np.array([7,0,0,0,0,5,0,0,1,0,1,3,0,0,0,0,0,0,0,0,0,0,8,1,0,0,0,0,0,0,3,0,0,1,5,0,0,0,9,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,4,0,0,0,0,2,5,1,0,0,9,0,0,0,0,9,0,0,0,0,0])
            c = "G5"
            p = "cell"
            ref = 58
            n = str(int((6+session["b"]-1) % 9) + 1) 
        if(session["cepuz"] == 12):
            numbers = np.array([2,0,0,0,0,9,0,0,0,0,4,0,0,7,8,2,3,0,0,5,0,0,0,1,0,6,0,8,0,0,0,0,0,0,0,0,3,0,0,6,0,0,0,4,0,4,0,0,0,0,0,0,0,1,0,9,0,0,0,0,5,0,0,0,0,0,7,3,0,0,2,9,0,0,6,0,0,0,0,0,0])
            c = "B3"
            p = "cell"
            ref = 11
            n = str(int((1+session["b"]-1) % 9) + 1) 
        if(session["cepuz"] == 13):
            numbers = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,6,0,0,1,0,0,0,0,0,0,3,0,0,0,3,0,0,0,0,0,1,0,0,4,0,0,0,2,9,0,0,0,7,0,0,0,0,0,0,4,0,8,2,0,1,5,0,0,0,0,0,7,0,0,0,2,2,0,0,0,6,0,0,0,0])
            c = "G6"
            p = "cell"
            ref = 59
            n = str(int((3+session["b"]-1) % 9) + 1) 
        if(session["cepuz"] == 14):
            numbers = np.array([0,0,0,1,0,0,0,0,0,0,8,0,0,0,0,3,0,6,9,0,0,0,3,0,0,0,0,0,0,7,0,0,0,4,1,0,0,0,6,0,9,0,5,0,0,0,0,5,0,0,0,0,0,0,5,0,1,2,4,0,0,0,7,0,0,0,0,0,0,0,3,0,0,6,0,0,0,0,0,0,0])
            c = "G2"
            p = "cell"
            ref = 55
            n = str(int((3+session["b"]-1) % 9) + 1) 
        if(session["cepuz"] == 15):
            numbers = np.array([0,0,2,0,0,0,0,0,0,5,0,0,4,0,3,2,0,7,9,0,0,2,0,0,0,0,0,0,0,3,0,2,0,1,0,0,0,0,1,0,4,0,0,2,0,2,0,7,0,6,0,0,0,0,6,2,0,0,0,0,0,5,0,0,0,0,0,7,4,0,0,2,0,8,0,0,0,2,0,0,0])
            c = "B2"
            p = "cell"
            ref = 10
            n = str(int((1+session["b"]-1) % 9) + 1) 
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        tempnum = copy.deepcopy(numbers)
        if(session["t"] == 1):
                ref = (ref + 2*len(numbers) // 3) % len(numbers)
                for i in range(2*len(numbers) // 3):
                    numbers[i] = int(tempnum[i+len(numbers) // 3])
                for i in range(2*len(numbers) // 3,len(numbers)):
                    numbers[i] = int(tempnum[i-2*len(numbers) // 3])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
        if(session["t"] == 2):
            ref = (ref + len(numbers) // 3) % len(numbers)
            for i in range(len(numbers) // 3):
                numbers[i] = int(tempnum[i+2*len(numbers) // 3])
            for i in range(len(numbers) // 3,len(numbers)):
                numbers[i] = int(tempnum[i-len(numbers) // 3])
            for i in range(9):
               if(c[0] == letters[i]):
                   newrow = letters[(i+3)%9]
            c = newrow + c[1]
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(g)
        if(p == "cell"):
            numslist[ref] = int(n)
            if(cell == c):
                return render_template("colelimpuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=True, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
            else:
                return render_template("colelimpuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=False, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
        else:
            red = []
            if(cell.isdigit()):
                numslist[ref] = int(cell)
                print(numslist)
                red = [ref]
            if(cell == n):
                return render_template("colelimpuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=True, ans=n,difficulty=dif, blues=[ref], reds= [],grays=g, dif=session["difficulty"])
            else:
                return render_template("colelimpuzzles.html", nums=numslist,length=len(numslist), lets=letters, result=False, ans=n,difficulty=dif, reds=red, blues=[], grays=g, dif=session["difficulty"] )
@app.route("/puzzles/rowreduction/<dif>", methods=["GET", "POST"])
def rowreductionpuzzles(dif):
    c = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b")
        if("t" in session):
            session.pop("t")
        if("c" in session):
            session.pop("c")
        if("difficulty" in session):
            session.pop("difficulty", None)
        b = random.randint(0,8)
        session["b"] = b
        session["difficulty"] = dif
        if(dif == "easy"):
            a = random.randint(1,5)
            if "repuz" in session:
                if(a == session["repuz"]):
                    if(a == 1):
                        a += 1
                    else:
                        a -= 1
            session["repuz"] = a
            if(a == 1):
                numbers = np.array([0,0,0,7,1,2,0,5,0,9,0,0,0,0,0,1,3,0,6,1,7,0,0,0,2,8,0])
                c = "C9"
                n = str(int((4+session["b"]-1) % 9) + 1) 
                p = "number"
            if(a == 2):
                numbers = np.array([0,8,6,2,0,0,3,0,7,0,0,4,0,0,0,1,0,0,0,5,0,3,9,6,0,0,0])
                c = "A1"
                n = str(int((9+session["b"]-1) % 9) + 1) 
                p = "number"
            if(a == 3):
                numbers = np.array([0,0,0,0,1,0,3,4,0,3,5,2,0,0,0,0,7,0,0,1,0,6,0,0,5,0,0,0,0,7,2,0,0,0,0,9,0,3,0,1,4,7,0,0,8,1,0,0,0,0,0,0,0,0])
                c = "A9"
                n = str(int((2+session["b"]-1) % 9) + 1) 
                p = "number"
            if(a == 4):
                numbers = np.array([0,0,0,0,0,7,0,0,1,7,0,1,0,3,0,0,0,9,0,0,0,1,0,0,0,0,0,0,0,0,4,2,9,0,5,0,0,4,0,6,0,0,1,3,0,0,0,8,0,0,0,0,7,0])
                c = "E9"
                n = str(int((2+session["b"]-1) % 9) + 1) 
                p = "number"
            if(a == 5):
                numbers = np.array([0,0,0,0,0,7,0,0,0,0,0,0,0,3,0,6,4,0,3,0,0,0,0,0,0,0,0,0,0,0,0,2,0,8,1,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,3,9,0,0,0,0,9,1,4,0,0,0,1,0,0,0,5,0,0,0,0])
                c = "I7"
                n = str(int((2+session["b"]-1) % 9) + 1) 
                p = "number"
        if(dif == "medium"):
            a = random.randint(6,10)
            if "repuz" in session:
                if(a == session["repuz"]):
                    if(a == 6):
                        a += 1
                    else:
                        a -= 1
            session["repuz"] = a
            if(a == 6):
                numbers = np.array([0,3,0,0,0,0,9,8,0,0,0,0,7,9,6,0,5,0,4,0,7,0,0,0,0,6,2])
                c = "C7"
                p = "cell"
            if(a == 7):
                numbers = np.array([9,8,7,0,5,0,4,0,0,0,0,0,0,4,0,3,0,0,0,0,5,0,0,0,1,0,0,3,6,1,0,0,0,5,0,0,0,0,0,0,0,7,0,0,0,0,2,0,8,0,0,0,9,0])
                c = "F7"
                p = "cell"
            if(a == 8):
                numbers = np.array([1,0,0,7,4,0,0,5,9,0,0,0,6,0,0,8,0,0,4,3,8,0,0,0,2,0,0])
                c = "A7"
                p = "cell"
            if(a == 9):
                numbers = np.array([5,1,0,0,2,3,9,0,6,0,0,3,7,0,0,0,0,0,0,4,0,0,0,0,8,3,9])
                c = "A3"
                p = "cell"
            if(a == 10):
                c = "D1"
                p = "cell"
                numbers = np.array([2,0,0,0,0,0,0,8,3,0,3,0,4,5,7,0,9,0,1,0,0,0,0,0,0,0,0,0,0,0,7,6,0,3,0,0,0,9,0,0,0,0,6,7,8,0,0,5,0,0,4,0,0,0])
        if(dif == "hard"):
            a = random.randint(11,15)
            if "repuz" in session:
                if(a == session["repuz"]):
                    if(a == 11):
                        a += 1
                    else:
                        a -= 1
            session["repuz"] = a
            if(a == 11):
                numbers = np.array([0,8,0,0,0,0,7,0,0,0,0,0,0,0,0,6,0,0,0,0,9,0,4,0,0,0,0,0,5,0,0,2,0,0,3,1,0,0,0,6,3,1,0,7,0,9,0,0,0,0,0,0,0,5,6,0,0,0,0,0,0,0,0,1,0,0,0,7,0,4,0,0,0,0,0,0,0,0,0,0,0])
                c = "D7"
                p = "cell"
            if(a == 12):
                numbers = np.array([0,0,0,0,4,0,0,1,9,9,1,2,0,8,0,0,0,3,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,4,0,6,0,4,9,0,0,0,0,0,0,0,5,2,0,0,0,1,5,7,0,0,0,0,0,0,0,0,0,8,9,0,4,0,2,0,0,0,0,3,0,2,0,0,0])
                c = "G9"
                p = "cell"
            if(a == 13):
                numbers = np.array([0,0,0,2,5,3,0,0,0,0,0,1,0,0,8,0,0,0,0,0,0,0,0,1,0,0,4,5,0,0,9,8,0,0,0,3,8,0,0,0,0,0,7,5,0,0,0,0,5,4,0,0,0,0,0,1,0,0,0,4,0,0,2,0,0,2,0,7,0,0,0,9,0,0,0,6,0,0,0,0,0])
                c = "E9"
                p = "cell"
            if(a == 14):
                numbers = np.array([0,0,0,6,0,0,0,0,7,6,8,0,0,0,7,0,0,3,0,0,0,0,0,0,0,0,5,2,1,3,0,0,0,0,0,0,8,0,0,0,0,9,0,0,0,0,0,0,0,0,2,7,8,0,0,0,0,0,0,0,0,0,1,0,4,8,0,1,5,0,0,0,1,0,0,0,7,0,0,0,4])
                c = "F9"
                p = "cell"
            if(a == 15):
                numbers = np.array([0,0,0,1,0,0,0,0,0,0,9,0,0,0,0,0,7,0,3,0,0,0,0,0,0,5,0,0,4,0,0,0,3,0,0,0,0,0,0,5,1,7,0,0,6,2,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,9,0,0,6,9,0,4,0,0,1,0,0,0,0,0,0,1,0,0,0])
                c = "D8"
                p = "cell"
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if(len(numbers) == 81):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            session["t"] = random.randint(0,2)
            if(session["t"] == 1):
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        session["c"] = random.randint(0,2)
        print(session["c"])
        if(session["c"] == 1):
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
            c = c[0] + newcol
        if(session["c"] == 2):
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
            c = c[0] + newcol
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("rowelimpuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
            cell = request.form["cell"]
            if(session["repuz"] == 1):
                numbers = np.array([0,0,0,7,1,2,0,5,0,9,0,0,0,0,0,1,3,0,6,1,7,0,0,0,2,8,0])
                c = "C9"
                n = str(int((4+session["b"]-1) % 9) + 1) 
                p = "number"
                ref = 26
            if(session["repuz"] == 2):
                numbers = np.array([0,8,6,2,0,0,3,0,7,0,0,4,0,0,0,1,0,0,0,5,0,3,9,6,0,0,0])
                c = "A1"
                n = str(int((9+session["b"]-1) % 9) + 1) 
                p = "number"
                ref = 0
            if(session["repuz"] == 3):
                numbers = np.array([0,0,0,0,1,0,3,4,0,3,5,2,0,0,0,0,7,0,0,1,0,6,0,0,5,0,0,0,0,7,2,0,0,0,0,9,0,3,0,1,4,7,0,0,8,1,0,0,0,0,0,0,0,0])
                c = "A9"
                n = str(int((2+session["b"]-1) % 9) + 1) 
                p = "number"
                ref = 8
            if(session["repuz"] == 4):
                numbers = np.array([0,0,0,0,0,7,0,0,1,7,0,1,0,3,0,0,0,9,0,0,0,1,0,0,0,0,0,0,0,0,4,2,9,0,5,0,0,4,0,6,0,0,1,3,0,0,0,8,0,0,0,0,7,0])
                c = "E9"
                n = str(int((2+session["b"]-1) % 9) + 1) 
                p = "number"
                ref = 44
            if(session["repuz"] == 5):
                numbers = np.array([0,0,0,0,0,7,0,0,0,0,0,0,0,3,0,6,4,0,3,0,0,0,0,0,0,0,0,0,0,0,0,2,0,8,1,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,3,9,0,0,0,0,9,1,4,0,0,0,1,0,0,0,5,0,0,0,0])
                c = "I7"
                n = str(int((2+session["b"]-1) % 9) + 1) 
                p = "number"
                ref = 78
            if(session["repuz"] == 6):
                numbers = np.array([0,3,0,0,0,0,9,8,0,0,0,0,7,9,6,0,5,0,4,0,7,0,0,0,0,6,2])
                c = "C7"
                p = "cell"
                ref = 24
                n = str(int((1+session["b"]-1) % 9) + 1) 
            if(session["repuz"] == 7):
                numbers = np.array([9,8,7,0,5,0,4,0,0,0,0,0,0,4,0,3,0,0,0,0,5,0,0,0,1,0,0,3,6,1,0,0,0,5,0,0,0,0,0,0,0,7,0,0,0,0,2,0,8,0,0,0,9,0])
                c = "F7"
                p = "cell"
                ref = 51       
                n = str(int((6+session["b"]-1) % 9) + 1) 
            if(session["repuz"] == 8):
                numbers = np.array([1,0,0,7,4,0,0,5,9,0,0,0,6,0,0,8,0,0,4,3,8,0,0,0,2,0,0])
                c = "A7"
                p = "cell"
                ref = 6
                n = str(int((3+session["b"]-1) % 9) + 1) 
            if(session["repuz"] == 9):
                numbers = np.array([5,1,0,0,2,3,9,0,6,0,0,3,7,0,0,0,0,0,0,4,0,0,0,0,8,3,9])
                c = "A3"
                p = "cell"
                ref = 2
                n = str(int((8+session["b"]-1) % 9) + 1) 
            if(session["repuz"] == 10):
                c = "D1"
                p = "cell"
                ref = 27
                n = str(int((8+session["b"]-1) % 9) + 1) 
                numbers = np.array([2,0,0,0,0,0,0,8,3,0,3,0,4,5,7,0,9,0,1,0,0,0,0,0,0,0,0,0,0,0,7,6,0,3,0,0,0,9,0,0,0,0,6,7,8,0,0,5,0,0,4,0,0,0])
            if(session["repuz"] == 11):
                numbers = np.array([0,8,0,0,0,0,7,0,0,0,0,0,0,0,0,6,0,0,0,0,9,0,4,0,0,0,0,0,5,0,0,2,0,0,3,1,0,0,0,6,3,1,0,7,0,9,0,0,0,0,0,0,0,5,6,0,0,0,0,0,0,0,0,1,0,0,0,7,0,4,0,0,0,0,0,0,0,0,0,0,0])
                c = "D7"
                p = "cell"
                ref = 33
                n = str(int((8+session["b"]-1) % 9) + 1) 
            if(session["repuz"] == 12):
                numbers = np.array([0,0,0,0,4,0,0,1,9,9,1,2,0,8,0,0,0,3,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,4,0,6,0,4,9,0,0,0,0,0,0,0,5,2,0,0,0,1,5,7,0,0,0,0,0,0,0,0,0,8,9,0,4,0,2,0,0,0,0,3,0,2,0,0,0])
                c = "G9"
                p = "cell"
                ref = 62
                n = str(int((6+session["b"]-1) % 9) + 1) 
            if(session["repuz"] == 13):
                numbers = np.array([0,0,0,2,5,3,0,0,0,0,0,1,0,0,8,0,0,0,0,0,0,0,0,1,0,0,4,5,0,0,9,8,0,0,0,3,8,0,0,0,0,0,7,5,0,0,0,0,5,4,0,0,0,0,0,1,0,0,0,4,0,0,2,0,0,2,0,7,0,0,0,9,0,0,0,6,0,0,0,0,0])
                c = "E9"
                p = "cell"
                ref = 44
                n = str(int((6+session["b"]-1) % 9) + 1) 
            if(session["repuz"] == 14):
                numbers = np.array([0,0,0,6,0,0,0,0,7,6,8,0,0,0,7,0,0,3,0,0,0,0,0,0,0,0,5,2,1,3,0,0,0,0,0,0,8,0,0,0,0,9,0,0,0,0,0,0,0,0,2,7,8,0,0,0,0,0,0,0,0,0,1,0,4,8,0,1,5,0,0,0,1,0,0,0,7,0,0,0,4])
                c = "F9"
                p = "cell"
                ref = 53
                n = str(int((6+session["b"]-1) % 9) + 1) 
            if(session["repuz"] == 15):
                numbers = np.array([0,0,0,1,0,0,0,0,0,0,9,0,0,0,0,0,7,0,3,0,0,0,0,0,0,5,0,0,4,0,0,0,3,0,0,0,0,0,0,5,1,7,0,0,6,2,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,9,0,0,6,9,0,4,0,0,1,0,0,0,0,0,0,1,0,0,0])
                c = "D8"
                p = "cell"
                ref = 34
                n = str(int((8+session["b"]-1) % 9) + 1) 
            for i in range(numbers.size):
                if(numbers[i] != 0):
                    numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
            if("t" in session):
                tempnum = copy.deepcopy(numbers)
                newrow = ""
                print(c)
                if(session["t"] == 1):
                    ref = (ref+54) % 81
                    for i in range(54):
                        numbers[i] = int(tempnum[i+27])
                    for i in range(54,81):
                        numbers[i] = int(tempnum[i-54])
                    for i in range(9):
                       if(c[0] == letters[i]):
                           newrow = letters[(i+6)%9]
                    c = newrow + c[1]
                if(session["t"] == 2):
                    ref = (ref+27) % 81
                    for i in range(27):
                        numbers[i] = int(tempnum[i+54])
                    for i in range(27,81):
                        numbers[i] = int(tempnum[i-27])
                    for i in range(9):
                       if(c[0] == letters[i]):
                           newrow = letters[(i+3)%9]
                    c = newrow + c[1]
            tempnum = copy.deepcopy(numbers)
            newcol = ""
            print(c)
            print(session["c"])
            if(session["c"] == 1):
                ref = 9*(ref//9) + (ref+6)%9
                for i in range(6):
                   for j in range(len(numbers) // 9):
                       numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
                for i in range(6,9):
                    for j in range(len(numbers) // 9):
                        numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
                for i in range(9):
                   if(int(c[1]) == i+1):
                       newcol = str(int((i+6)%9) + 1)
                       print(newcol)
                c = c[0] + newcol
            if(session["c"] == 2):
                ref = 9*(ref//9) + (ref+3)%9
                for i in range(3):
                    for j in range(len(numbers) // 9):
                        numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
                for i in range(3,9):
                    for j in range(len(numbers) // 9):
                        numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
                for i in range(9):
                   if(int(c[1]) == i+1):
                       newcol = str(int((i+3)%9) + 1)
                       print(newcol)
                c = c[0] + newcol
            g = []
            for k in range(numbers.size):
                if(numbers[k] != 0):
                    g.append(k)
            numslist = numbers.tolist()
            print(g)
            if(p == "cell"):
                numslist[ref] = int(n)
                
                if(cell == c):
                    return render_template("rowelimpuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=True, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
                else:
                    return render_template("rowelimpuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=False, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
            else:
                red = []
                if(cell.isdigit()):
                    numslist[ref] = int(cell)
                    print(numslist)
                    red = [ref]
                if(cell == n):
                    return render_template("rowelimpuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=True, ans=n,difficulty=dif, blues=[ref], reds= [],grays=g, dif=session["difficulty"])
                else:
                    return render_template("rowelimpuzzles.html", nums=numslist,length=len(numslist), lets=letters, result=False, ans=n,difficulty=dif, reds=red, blues=[], grays=g, dif=session["difficulty"] )
@app.route("/puzzles/nakedtriples/<dif>", methods=["GET", "POST"])
def nakedtriplepuzzles(dif):
    c = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if("b" in session):
            session.pop("b")
        if("t" in session):
            session.pop("t")
        if("c" in session):
            session.pop("c")
        if("difficulty" in session):
            session.pop("difficulty", None)
        b = 0
        session["b"] = b
        session["difficulty"] = dif
        if(dif == "easy"):
            a = random.randint(1,5)
            if "ntpuz" in session:
                if(a == session["ntpuz"]):
                    if(a == 1):
                        a += 1
                    else:
                        a -= 1
            session["ntpuz"] = a
            if(a == 1):
                numbers = np.array([0,0,0,0,0,6,7,0,0,0,7,4,0,0,0,1,2,0,1,3,5,0,7,0,0,0,0])
                p = "number"
                c = "B1"
                n = str(int((6+session["b"]-1) % 9) + 1) 
            if(a == 2):
                numbers = np.array([0,0,0,5,1,6,7,0,0,8,4,0,0,0,0,5,0,0,1,7,0,0,2,0,0,0,0])
                p = "number"
                c = "B3"
                n = str(int((6+session["b"]-1) % 9) + 1) 
            if(a == 3):
                numbers = np.array([7,9,0,0,0,4,0,0,0,0,0,0,9,7,0,3,5,0,0,0,0,0,0,0,0,6,0])
                p = "number"
                c = "B9"
                n = str(int((4+session["b"]-1) % 9) + 1)
            if(a == 4):
                numbers = np.array([0,0,0,8,0,5,7,0,0,9,4,0,0,0,7,0,0,5,0,0,1,0,0,0,0,0,0])
                p = "number"
                c = "B3"
                n = str(int((8+session["b"]-1) % 9) + 1)
            if(a == 5):
                numbers = np.array([0,0,0,0,2,0,1,9,0,5,0,0,0,0,0,0,0,0,0,7,6,9,0,0,0,0,2])
                c = "C1"   
                p = "number"
                n = str(int((1+session["b"]-1) % 9) + 1)
        if(dif == "medium"):
            a = random.randint(6,10)
            if "ntpuz" in session:
                if(a == session["ntpuz"]):
                    if(a == 6):
                        a += 1
                    else:
                        a -= 1
            session["ntpuz"] = a
            if(a == 6):
                numbers = np.array([8,0,0,1,0,4,0,3,0,0,1,5,7,6,0,0,2,0,3,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,1,0,0,0,0,0,0,7,0,0,0,4,0,6,0,2,0,4,7,0,0,0,2,1,9,0,7,0,0,0,0,0,3,0,0,0,0,0,0])
                p = "number"
                c = "I1"
                n = str(int((7+session["b"]-1) % 9) + 1)
            if(a == 7):
                numbers = np.array([0,0,0,1,2,0,6,5,0,3,7,0,0,0,0,2,0,1,6,0,0,0,8,0,0,0,0])
                c = "B3"
                p = "cell"
            if(a == 8):
                numbers = np.array([8,0,0,0,1,0,0,0,9,0,0,0,2,9,5,1,0,0,0,7,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,3,0,4,0,7,0,0,0,1,0,0,5,0,0,0,0,0,0])
                c = "A3"
                p = "cell"
            if(a == 9):
                numbers = np.array([0,0,0,8,7,6,4,0,0,7,1,0,0,0,9,8,6,0,0,5,0,3,0,0,7,0,0])
                c = "B3"
                p = "cell"
            if(a == 10):
                numbers = np.array([0,5,0,3,0,0,7,0,0,7,1,0,0,0,9,8,6,0,0,0,0,8,7,6,0,0,4])
                c = "B3"
                p = "cell"
        if(dif == "hard"):
            a = random.randint(11,15)
            if "ntpuz" in session:
                if(a == session["ntpuz"]):
                    if(a == 11):
                        a += 1
                    else:
                        a -= 1
            session["ntpuz"] = a
            if(a == 11):
                numbers = np.array([0,0,5,6,0,0,1,0,0,0,0,0,0,0,0,0,2,0,4,0,6,9,5,0,0,0,0,1,0,0,0,0,0,0,4,0,3,0,0,0,0,0,0,7,2,0,0,0,0,9,0,0,0,0,0,0,7,0,0,0,0,6,0,0,0,0,0,3,9,0,0,0,0,0,1,0,0,0,0,0,0])
                c = "A8"
                p = "cell"
            if(a == 12):
                numbers = np.array([7,4,0,0,0,2,0,0,0,0,6,0,3,9,0,0,5,0,0,0,0,0,0,0,0,0,0,6,0,1,8,4,0,0,0,0,0,0,5,0,0,0,7,0,0,0,0,9,0,0,0,0,0,1,0,0,0,0,0,5,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0])
                c = "B1"
                p = "cell"
            if(a == 13):
                numbers = np.array([0,0,0,0,2,0,4,9,6,5,0,0,0,0,0,0,0,0,0,6,7,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,6,0,0,3,8,0,0,0,0,0,7,2,0,0,9,0,0,6,1,0,6,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
                c = "C1"
                p = "cell"
            if(a == 14):
                numbers = np.array([0,0,5,0,0,0,0,0,0,0,0,7,0,4,5,6,0,0,0,0,2,0,0,0,9,0,0,0,0,0,0,0,0,7,0,0,4,9,0,0,0,0,0,0,2,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,5,0,3,0,0,0,0,1,0,7,0,0,0,0,0,0,0,0])
                c = "F1"
                p = "cell"
            if(a == 15):
                numbers = np.array([0,6,0,0,0,0,0,0,4,0,1,0,0,0,7,0,8,0,0,0,4,0,0,0,0,0,0,0,0,7,0,2,0,4,1,0,0,0,5,0,0,6,8,0,0,0,3,0,0,0,0,9,0,0,0,0,1,0,0,0,0,0,0,0,4,6,0,5,0,0,0,0,0,0,0,0,0,9,6,4,0])
                c = "D1"
                p = "cell"
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+b-1) % 9 + 1
        if(len(numbers) == 81):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            session["t"] = random.randint(0,2)
            if(session["t"] == 1):
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        session["c"] = random.randint(0,2)
        print(session["c"])
        if(session["c"] == 1):
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
            c = c[0] + newcol
        if(session["c"] == 2):
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(numslist)
        print(g)
        return render_template("nakedtriplespuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=2, puztype=p, cell=c,difficulty=dif, blues=[], reds=[], grays=g, dif=session["difficulty"])
    else:
        cell = request.form["cell"]
        if(session["ntpuz"] == 1):
            numbers = np.array([0,0,0,0,0,6,7,0,0,0,7,4,0,0,0,1,2,0,1,3,5,0,7,0,0,0,0])
            p = "number"
            c = "B1"
            ref = 9
            n = str(int((6+session["b"]-1) % 9) + 1) 
        if(session["ntpuz"] == 2):
            numbers = np.array([0,0,0,5,1,6,7,0,0,8,4,0,0,0,0,5,0,0,1,7,0,0,2,0,0,0,0])
            p = "number"
            c = "B3"
            ref = 11
            n = str(int((6+session["b"]-1) % 9) + 1) 
        if(session["ntpuz"] == 3):
            numbers = np.array([7,9,0,0,0,4,0,0,0,0,0,0,9,7,0,3,5,0,0,0,0,0,0,0,0,6,0])
            p = "number"
            c = "B9"
            ref = 17
            n = str(int((4+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 4):
            numbers = np.array([0,0,0,8,0,5,7,0,0,9,4,0,0,0,7,0,0,5,0,0,1,0,0,0,0,0,0])
            p = "number"
            c = "B3"
            ref = 11
            n = str(int((8+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 5):
            numbers = np.array([0,0,0,0,2,0,1,9,0,5,0,0,0,0,0,0,0,0,0,7,6,9,0,0,0,0,2])
            c = "C1"   
            p = "number"
            ref = 18
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 6):
            numbers = np.array([8,0,0,1,0,4,0,3,0,0,1,5,7,6,0,0,2,0,3,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,1,0,0,0,0,0,0,7,0,0,0,4,0,6,0,2,0,4,7,0,0,0,2,1,9,0,7,0,0,0,0,0,3,0,0,0,0,0,0])
            p = "number"
            c = "I1"
            ref = 72
            n = str(int((7+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 7):
            numbers = np.array([0,0,0,1,2,0,6,5,0,3,7,0,0,0,0,2,0,1,6,0,0,0,8,0,0,0,0])
            c = "B3"
            ref = 11
            p = "cell" 
            n = str(int((5+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 8):
            numbers = np.array([8,0,0,0,1,0,0,0,9,0,0,0,2,9,5,1,0,0,0,7,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,3,0,4,0,7,0,0,0,1,0,0,5,0,0,0,0,0,0])
            c = "A3"
            ref = 2
            p = "cell"
            n = str(int((2+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 9):
            numbers = np.array([0,0,0,8,7,6,4,0,0,7,1,0,0,0,9,8,6,0,0,5,0,3,0,0,7,0,0])
            c = "B3"
            ref = 11
            p = "cell"
            n = str(int((4+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 10):
            numbers = np.array([0,5,0,3,0,0,7,0,0,7,1,0,0,0,9,8,6,0,0,0,0,8,7,6,0,0,4])
            c = "B3"
            ref = 11
            p = "cell"
            n = str(int((4+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 11):
            numbers = np.array([0,0,5,6,0,0,1,0,0,0,0,0,0,0,0,0,2,0,4,0,6,9,5,0,0,0,0,1,0,0,0,0,0,0,4,0,3,0,0,0,0,0,0,7,2,0,0,0,0,9,0,0,0,0,0,0,7,0,0,0,0,6,0,0,0,0,0,3,9,0,0,0,0,0,1,0,0,0,0,0,0])
            c = "A8"
            ref = 11
            p = "cell"
            n = str(int((9+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 12):
            numbers = np.array([7,4,0,0,0,2,0,0,0,0,6,0,3,9,0,0,5,0,0,0,0,0,0,0,0,0,0,6,0,1,8,4,0,0,0,0,0,0,5,0,0,0,7,0,0,0,0,9,0,0,0,0,0,1,0,0,0,0,0,5,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0])
            c = "B1"
            ref = 9
            p = "cell"
            n = str(int((1+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 13):
            numbers = np.array([0,0,0,0,2,0,4,9,6,5,0,0,0,0,0,0,0,0,0,6,7,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,6,0,0,3,8,0,0,0,0,0,7,2,0,0,9,0,0,6,1,0,6,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            c = "C1"
            ref = 18
            p = "cell"
            n = str(int((4+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 14):
            numbers = np.array([0,0,5,0,0,0,0,0,0,0,0,7,0,4,5,6,0,0,0,0,2,0,0,0,9,0,0,0,0,0,0,0,0,7,0,0,4,9,0,0,0,0,0,0,2,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,5,0,3,0,0,0,0,1,0,7,0,0,0,0,0,0,0,0])
            c = "F1"
            ref = 45
            p = "cell"
            n = str(int((2+session["b"]-1) % 9) + 1)
        if(session["ntpuz"] == 15):
            numbers = np.array([0,6,0,0,0,0,0,0,4,0,1,0,0,0,7,0,8,0,0,0,4,0,0,0,0,0,0,0,0,7,0,2,0,4,1,0,0,0,5,0,0,6,8,0,0,0,3,0,0,0,0,9,0,0,0,0,1,0,0,0,0,0,0,0,4,6,0,5,0,0,0,0,0,0,0,0,0,9,6,4,0])
            c = "D1"
            ref = 27
            p = "cell"
            n = str(int((6+session["b"]-1) % 9) + 1)
        for i in range(numbers.size):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+session["b"]-1) % 9 + 1
        if("t" in session):
            tempnum = copy.deepcopy(numbers)
            newrow = ""
            print(c)
            if(session["t"] == 1):
                ref = (ref+54) % 81
                for i in range(54):
                    numbers[i] = int(tempnum[i+27])
                for i in range(54,81):
                    numbers[i] = int(tempnum[i-54])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+6)%9]
                c = newrow + c[1]
            if(session["t"] == 2):
                ref = (ref+27) % 81
                for i in range(27):
                    numbers[i] = int(tempnum[i+54])
                for i in range(27,81):
                    numbers[i] = int(tempnum[i-27])
                for i in range(9):
                   if(c[0] == letters[i]):
                       newrow = letters[(i+3)%9]
                c = newrow + c[1]
        tempnum = copy.deepcopy(numbers)
        newcol = ""
        print(c)
        print(session["c"])
        if(session["c"] == 1):
            ref = 9*(ref//9) + (ref+6)%9
            for i in range(6):
               for j in range(len(numbers) // 9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+6)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        if(session["c"] == 2):
            ref = 9*(ref//9) + (ref+3)%9
            for i in range(3):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(len(numbers) // 9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
            for i in range(9):
               if(int(c[1]) == i+1):
                   newcol = str(int((i+3)%9) + 1)
                   print(newcol)
            c = c[0] + newcol
        print(c)
        g = []
        for k in range(numbers.size):
            if(numbers[k] != 0):
                g.append(k)
        numslist = numbers.tolist()
        print(g)
        if(p == "cell"):
            numslist[ref] = int(n)
            if(cell == c):
                return render_template("nakedtriplespuzzles.html", nums=numslist, length=len(numslist), lets=letters, result=True, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
            else:
                return render_template("nakedtriplespuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=False, ans=c,difficulty=dif, blues=[ref], reds=[], grays=g, dif=session["difficulty"])
        else:
            red = []
            if(cell.isdigit()):
                numslist[ref] = int(cell)
                print(numslist)
                red = [ref]
            if(cell == n):
                return render_template("nakedtriplespuzzles.html", nums=numslist, length=len(numslist),lets=letters, result=True, ans=n,difficulty=dif, blues=[ref], reds= [],grays=g, dif=session["difficulty"])
            else:
                return render_template("nakedtriplespuzzles.html", nums=numslist,length=len(numslist), lets=letters, result=False, ans=n,difficulty=dif, reds=red, blues=[], grays=g, dif=session["difficulty"] )
@app.route("/puzzles/xwing/<dif>", methods=["GET", "POST"])
def xwingpuzzles(dif):
    return render_template("puzzles.html")
@app.route("/puzzles/xywing/<dif>", methods=["GET", "POST"])
def xywingpuzzles(dif):
    return render_template("puzzles.html")
@app.route("/puzzles/swordfish/<dif>", methods=["GET", "POST"])
def swordfishpuzzles(dif):
    return render_template("puzzles.html")
# traveler iq challenge recreated
@app.route("/traveleriq", methods=["GET","POST"])
def traveleriq():
    if(request.method == "GET"):
        session.pop("i", None)
        session.pop("level",None)
        session.pop("minimum",None)
        return render_template("traveleriq.html",i=0,n='no', s=0, round = 0, m=0, x=0, y=0, mobx = 0, moby = 0, loc="none")
    if(request.method == "POST"):
        session["destinations"] = [0,5,5,5,6,6]
        session["nextround"] = ['no', 'no', 'Cities (Medium)',  'World Landmarks', 'Cities (Hard)', 'Cities (Impossible)']
        if not "i" in session:
            session["i"] = 1
        if not "level" in session:
            session["level"] = 1
        else:
            session["i"] += 1
        session["minimum"] = int(session["level"] % 6 * 10000 + 10000)
        if(session["i"] > session["destinations"][session["level"]]):
            session["i"] = 0
            if(session["level"] == 5):
                minimum = 60000
                return render_template("traveleriq.html",i=0,n=session["nextround"][session["level"]],s=minimum, round=99, m=minimum, x=0, y=0, mobx = 0, moby = 0,loc="none")
            session["level"] += 1
            minimum = int(session["level"] % 6 * 10000 + 10000)
            return render_template("traveleriq.html", i=0,n=session["nextround"][session["level"]], s=minimum, round=session["level"], m=minimum, x=0, y=0, mobx = 0, moby = 0, loc="none")
        i = session["i"]
        if(session["level"] == 1):
            if(i == 1):
                mapx = 131
                mapy = 101
                place = "Chicago, Illinois, USA"
            if(i == 2):
                mapx = 600.5
                mapy = 298
                place = "Perth, Australia"
            if(i == 3):
                mapx = 620
                mapy = 113
                place = "Seoul, South Korea"
            if(i == 4):
                mapx = 320.5
                mapy = 106
                place = "Madrid, Spain"
            if(i == 5):
                mapx = 222
                mapy = 273
                place = "Rio de Janeiro, Brazil"
        if(session["level"] == 2):
            if(i == 1):
                mapx = 382.3
                mapy = 110
                place = "Athens, Greece"
            if(i == 2):
                mapx = 577
                mapy = 205.1
                place = "Kuala Lumpur, Malaysia"
            if(i == 3):
                mapx = 601
                mapy = 154.1
                place = "Hong Kong, China"
            if(i == 4):
                mapx = 141
                mapy = 246.1
                place = "Lima, Peru"
            if(i == 5):
                mapx = 417
                mapy = 214.2
                place = "Nairobi, Kenya"
        if(session["level"] == 3):
            if(i == 1):
                mapx = 357
                mapy = 101
                place = "The Pantheon (the old one)"
            if(i == 2):
                mapx = 534
                mapy = 136
                place = "Mount Everest"
            if(i == 3):
                mapx = 77
                mapy = 94
                place = "Yellowstone"
            if(i == 4):
                mapx = 391
                mapy = 261
                place = "Victoria Falls"
            if(i == 5):
                mapx = 412
                mapy = 64
                place = "St. Basil's Cathedral"
        if(session["level"] == 4):
            if(i == 1):
                mapx = 370
                mapy = 272
                place = "Windhoek, Namibia"
            if(i == 2):
                mapx = 647
                mapy = 247
                place = "Darwin, Australia"
            if(i == 3):
                mapx = 370
                mapy = 95
                place = "Sarajevo, Bosnia and Herzegovina"
            if(i == 4):
                mapx = 518
                mapy = 163
                place = "Hyderabad, India"
            if(i == 5):
                mapx = 183
                mapy = 352
                place = "Punta Arenas, Chile"
            if(i == 6):
                mapx = 391
                mapy = 33
                place = "Murmansk, Russia"
        if(session["level"] == 5):
            if(i == 1):
                mapx = 623
                mapy = 97
                place = "Vladivostok"
            if(i == 2):
                mapx = 178
                mapy = 222
                place = "Manaus"
            if(i == 3):
                mapx = 759
                mapy = 261.2
                place = "Suva"
            if(i == 4):
                mapx = 443
                mapy = 260
                place = "Antananarivo"
            if(i == 5):
                mapx = 567
                mapy = 162
                place = "Chiang Mai"
            if(i == 6):
                mapx = 176
                mapy = 184
                place = "Port-of-Spain"
        xmobile = mapx * 3 / 8
        ymobile = mapy * 3 / 8
        return render_template("traveleriq.html", i=session["i"],m=0, n=session["nextround"][session["level"]],s=session["minimum"],round=session["level"], x=mapx, y=mapy, mobx = xmobile, moby = ymobile, loc=place)
# groups thing for dad
@app.route("/groups", methods=["GET", "POST"])
def groupGenerator():
    if(request.method == "GET"):
        return(render_template("namegenerator.html", method = 'get', n=["bob"], g=2))
    if(request.method == "POST"): 
        names = request.form["names"]
        namelist = []
        a = 0
        for i in range(len(names)):
            if(names[i] == ','):
                namelist.append(names[a:i])
                a = i+1
            if(i == len(names) - 1):
                namelist.append(names[a:i+1])
        newnumbers = []
        nameObjects = []    
        if not (request.form["groups"].isnumeric()):
            flash("Put in a number for the number of groups")
            return(render_template("namegenerator.html", method = 'get', n=["bob"], g=2))
        groups = int(request.form["groups"])
        pergroup = math.ceil(len(names) / groups)
        newnames = np.empty(len(namelist),dtype=object)
        for i in range(len(namelist)):
            nameObjects.append(Name(namelist[i]))
        index = 0
        while(index < len(namelist)):
            k = random.randint(0,len(namelist)-1)
            if k not in newnumbers:
                nameObjects[index].number = k
                newnumbers.append(k)
                index+=1
        for i in range(len(nameObjects)):
            newnames[nameObjects[i].number] = nameObjects[i].name
        print(newnames)
        return(render_template("namegenerator.html", method='post',n=newnames, g=groups))
# methods page
@app.route("/methods")
def methods():
    return render_template("methods.html")
# takes in sudoku, solves it
@app.route("/solver", methods=["GET","POST"])
def buildSudoku():
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if request.method == "GET":
        return render_template("sudokuform.html",lets=letters)
    else:
        if("sudoku" in session):
            session.pop("sudoku",None)
            session.pop("solution",None)
            session.pop("methods",None)
            session.pop("numberOfSteps",None)
            session.pop("stepsDisplayed",None)
            session.pop("givens", None)
            session.pop("bluenums", None)
            session.pop("storeOriginal", None)
            session.pop("graynums", None)
            session.pop("solverexplain", None)
        if(request.form["stringOfNums"] != ""):
            if(len(request.form["stringOfNums"]) != 81):
                return(render_template("incomplete.html"))
            rows = np.empty((9,9))
            a = request.form["stringOfNums"]
            for i in range(81):
                rows[i//9][i%9] = a[i]
        else:
            numbercheck = ["1","2","3","4","5","6","7","8","9",1,2,3,4,5,6,7,8,9]
            rows, cols = (9, 9)
            coords = [[0 for i in range(cols)] for j in range(rows)]
            for i in range(9):
                for j in range(9):
                    coords[i][j] = letters[i] + str(j + 1)
            rows = np.empty((9,9))
            anynumbers = False
            for i in range(9):
                for j in range(9):
                    if(request.form[coords[i][j]] == ""):
                        rows[i][j] = 0
                    else:
                        anynumbers = True
                        if(request.form[coords[i][j]] not in numbercheck):
                            return(render_template("incomplete.html"))
                        rows[i][j] = request.form[coords[i][j]]
            if(anynumbers == False):
                rows = np.array([[0,1,0,3,0,0,7,0,8],[0,0,0,0,0,2,0,0,0],[0,0,8,6,0,5,0,4,9],[0,0,3,0,5,0,9,6,0],[0,6,0,4,0,0,0,0,5],[8,0,0,0,0,1,0,3,0],[7,0,0,0,2,0,0,0,0],[0,0,2,9,8,0,5,0,0],[0,5,0,0,0,0,3,0,0]])
        #initialize the grid
        done = 0
        iter = 0
        session["givens"] = 0
        session["bluenums"] = ""
        init = []
        cells = np.empty((9,9),dtype=object)
        for i in range(9):
            for j in range(9):
                if(rows[i][j] != 0):
                    session["givens"] += 1
                cells[i][j] = Cell(int(rows[i][j]))
                init.append(int(rows[i][j]))
        session["sudoku"] = init
        sudoku = sudokuGrid(cells)      
        temp = copy.deepcopy(sudoku)
        #cycle through sudoku operations
        i = 0
        while(done == 0 and i < 100):
            a = sudoku.cellsSolved
            sudoku.checkCells()
            if(a == sudoku.cellsSolved):
                sudoku.checkBoxes()
                if(a == sudoku.cellsSolved):
                    sudoku.checkColumns()
                    if(a == sudoku.cellsSolved):
                        sudoku.checkRows()
                        if(a == sudoku.cellsSolved):
                            sudoku.nakedPairs()
                            if(a == sudoku.cellsSolved):
                                sudoku.boxReduction()
                                if(a == sudoku.cellsSolved):
                                    sudoku.colReduction()
                                    if(a == sudoku.cellsSolved):
                                        sudoku.rowReduction()
                                        if(a == sudoku.cellsSolved):
                                            sudoku.nakedTriple()
                                            if(a == sudoku.cellsSolved):
                                                i += 10
            
        
            i+=1
            iter+=1
       
            #check if all values are filled in
            if (sudoku.checkDone() == True):
                done = 1
        if(done == 0):
            sudoku.xwing()
            sudoku.xywing()
            if(a == sudoku.cellsSolved):
                sudoku.guessAndCheck()
            i = 0
            while(done == 0 and i < 100):
                a = sudoku.cellsSolved
                sudoku.checkCells()
                if(a == sudoku.cellsSolved):
                    sudoku.checkBoxes()
                    if(a == sudoku.cellsSolved):
                        sudoku.checkColumns()
                        if(a == sudoku.cellsSolved):
                            sudoku.checkRows()
                            if(a == sudoku.cellsSolved):
                                sudoku.nakedPairs()
                                if(a == sudoku.cellsSolved):
                                    sudoku.boxReduction()
                                    if(a == sudoku.cellsSolved):
                                        sudoku.colReduction()
                                        if(a == sudoku.cellsSolved):
                                            sudoku.rowReduction()
                                            if(a == sudoku.cellsSolved):
                                                sudoku.nakedTriple()
                                                if(a == sudoku.cellsSolved):
                                                    sudoku.xwing()
                                                    if(a == sudoku.cellsSolved):
                                                        sudoku.xywing()
                                                        if(a == sudoku.cellsSolved):
                                                           sudoku.guessAndCheck()
                                                           if(a == sudoku.cellsSolved):
                                                               i+=50
                
            
                i+=1
                iter+=1
           
                #check if all values are filled in
                if (sudoku.checkDone() == True):
                    done = 1
        answer = []
        listOfMethods = ""
        listOfOrders = ""
        listOfExplains = ""
        #prints completed sudoku
        k = 0
        for i in range(9):
                for j in range(9):
                    answer.append(int(sudoku.cells[i][j].value))
                    listOfOrders = listOfOrders + str(int(sudoku.cells[i][j].order)) + ","
        while(k <= sudoku.cellsSolved):
            for i in range(9):
                for j in range(9):
                    if(sudoku.cells[i][j].order == k):
                        if(sudoku.cells[i][j].method != 'given'):
                            listOfExplains = listOfExplains + sudoku.cells[i][j].explain
                            listOfMethods = listOfMethods + 'Step ' + str(k) + ': cell ' + str(letters[i]) + str(j+1) + ' was solved by ' + sudoku.cells[i][j].method + ","
            k += 1
        graynums = []
        numlist = []
        for i in range(81):
            if(session["sudoku"][i] != 0):
                graynums.append(i)
        session["solverexplain"] = listOfExplains
        session["grays"] = graynums
        session["solution"] = answer
        session["methods"] = listOfMethods
        session["orders"] = listOfOrders
        session["numOfSteps"] = sudoku.cellsSolved
        session["stepsDisplayed"] = 0
        session["storeOriginal"] = session["sudoku"]
        if(done == 0):
            return render_template("incomplete.html")
        else:
            return render_template("sudoku formatting.html", nums=session["sudoku"], explain = [], methods=[], lets=letters, steps=0, blues = [], grays=graynums)
# solve entire sudoku and display steps
@app.route("/solver/solve", methods=["GET","POST"])
def solveSudoku():
    if not "sudoku" in session:
        return redirect(url_for("buildSudoku"))
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    m = session["methods"]
    b = session["orders"]
    e = session["solverexplain"]
    listOfOrders = []
    listOfMethods = []
    listOfBluenums = []
    listOfExplains = []
    a = 0
    for x in range(len(m)):
        if(m[x] == ","):
            listOfMethods.append(m[a:x])
            a = x+1
    a = 0
    for x in range(len(b)):
        if(b[x] == ","):
            listOfOrders.append(session["orders"][a:x])
            a = x+1
    for p in range(81):
        if(int(listOfOrders[p]) > 0):
            session["bluenums"] = session["bluenums"] + str(p) + ","
            num = p
    a = 0
    for x in range(len(e)):
        if(x != 0):
            if(e[x-1] == "." and e[x] == '.'):
                listOfExplains.append(e[a:x])
                a = x+1
    a = 0
    for x in range(len(session["bluenums"])):
        if(session["bluenums"][x] == ","):
            listOfBluenums.append(int(session["bluenums"][a:x]))
            a = x+1 
    return render_template("sudoku formatting.html", nums=session["solution"], explain = listOfExplains, methods=listOfMethods, lets=letters,steps=81,blues=listOfBluenums, grays=session["grays"])
# solve one step at a time for sudoku solver
@app.route("/solver/onestep", methods=["GET","POST"])
def onestep():
    if not "sudoku" in session:
        return redirect(url_for("buildSudoku"))
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(session["stepsDisplayed"] < session["numOfSteps"]):
        session["stepsDisplayed"] += 1
    b = session["orders"]
    m = session["methods"]
    e = session["solverexplain"]
    session["bluenums"] = ""
    listOfMethods = []
    listOfOrders = []
    listOfBluenums = []
    listOfExplains = []
    a = 0
    for x in range(len(m)):
        if(m[x] == ","):
            listOfMethods.append(session["methods"][a:x])
            a = x+1
    a = 0
    for x in range(len(b)):
        if(b[x] == ","):
            listOfOrders.append(session["orders"][a:x])
            a = x+1
    num = 0
    for p in range(81):
        if(int(listOfOrders[p]) <= session["stepsDisplayed"] and int(listOfOrders[p]) != 0):
            session["sudoku"][p] = int(session["solution"][p])
            session["bluenums"] = session["bluenums"] + str(p) + ","
            num = p
    a = 0
    for x in range(len(e)):
        if(x != 0):
            if(e[x-1] == "." and e[x] == '.'):
                listOfExplains.append(e[a:x])
                a = x+1
    print(session["sudoku"])
    a = 0
    for x in range(len(session["bluenums"])):
        if(session["bluenums"][x] == ","):
            listOfBluenums.append(int(session["bluenums"][a:x]))
            a = x+1
    return render_template("sudoku formatting.html", nums=session["sudoku"], lets=letters, explain = np.array([listOfExplains[session["stepsDisplayed"] - 1]]), methods=np.array([listOfMethods[session["stepsDisplayed"] - 1]]), steps=1, blues=listOfBluenums, grays=session["grays"])
# back one step for sudoku solver
@app.route("/solver/backone", methods = ["GET","POST"])
def backone():
    if not "sudoku" in session:
        return redirect(url_for("buildSudoku"))
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(session["stepsDisplayed"] > 0):
        session["stepsDisplayed"] -= 1
    else:
        return render_template("sudoku formatting.html", nums=session["storeOriginal"], explain = [], methods=[], lets=letters, steps=0, blues = [], grays = session["grays"])
    b = session["orders"]
    m = session["methods"]
    e = session["solverexplain"]
    listOfMethods = []
    listOfOrders = []
    listOfBluenums = []
    listOfExplains = []
    a = 0
    for x in range(len(m)):
        if(m[x] == ","):
            listOfMethods.append(session["methods"][a:x])
            a = x+1
    a = 0
    for x in range(len(b)):
        if(b[x] == ","):
            listOfOrders.append(session["orders"][a:x])
            a = x+1
    a = 0
    for x in range(len(e)):
        if(x != 0):
            if(e[x-1] == "." and e[x] == '.'):
                listOfExplains.append(e[a:x])
                a = x+1
    num = 0
    for p in range(81):
        if(int(listOfOrders[p]) == session["stepsDisplayed"] + 1):
            session["sudoku"][p] = int(session["storeOriginal"][p])
            if(p < 10):
                session["bluenums"] = session["bluenums"][0:len(session["bluenums"])-2]
            else:
                session["bluenums"] = session["bluenums"][0:len(session["bluenums"])-3]
            num = p
    a = 0
    for x in range(len(session["bluenums"])):
        if(session["bluenums"][x] == ","):
            listOfBluenums.append(int(session["bluenums"][a:x]))
            a = x+1
    if(session["stepsDisplayed"] == 0):
        return render_template("sudoku formatting.html", nums=session["sudoku"], lets=letters, explain = [], methods=[], steps=0, blues=[], grays=session["grays"])
    else:   
        return render_template("sudoku formatting.html", nums=session["sudoku"], lets=letters, explain = np.array([listOfExplains[session["stepsDisplayed"] - 1]]), methods=np.array([listOfMethods[session["stepsDisplayed"] - 1]]), steps=1, blues=listOfBluenums, grays=session["grays"])
# clears grid for sudoku solver
@app.route("/solver/clear", methods=["GET", "POST"])
def clearGrid():
    if not "sudoku" in session:
        return redirect(url_for("buildSudoku"))
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    listOfBluenums = []
    a = 0
    for x in range(len(session["bluenums"])):
        if(session["bluenums"][x] == ","):
            listOfBluenums.append(int(session["bluenums"][a:x]))
            a = x+1
    print(listOfBluenums)
    for x in range(len(session["sudoku"])):
        if x in listOfBluenums:
            session["sudoku"][x] = 0
    session["bluenums"] = ""
    session["stepsDisplayed"] = 0
    return render_template("sudoku formatting.html", nums=session["sudoku"], explain = [], methods = [], lets=letters, steps=0, blues=[], grays=session["grays"])
# solves cell for sudoku solver
@app.route("/solver/solvecell", methods=["GET", "POST"])
def solveCell():
    if not "sudoku" in session:
        return redirect(url_for("buildSudoku"))
    cell = request.form["cell"]
    listOfBluenums = []
    a = 0
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    index = 0
    validcell = False
    for j in range(9):
        if(cell[0] == letters[j]):
            for i in range(1,10):
                if(cell[1] == str(i)):
                    index = 9*j + i - 1
                    validcell = True
    if(validcell == False):
        flash("Invalid cell input, try again.")
        for x in range(len(session["bluenums"])):
            if(session["bluenums"][x] == ","):
                listOfBluenums.append(int(session["bluenums"][a:x]))
                a = x+1
        return(render_template("sudoku formatting.html", nums=session["sudoku"], explain = [], methods= [], lets=letters, steps=0, blues=listOfBluenums,grays=session["grays"]))
    if(session["sudoku"][index] == int(session["solution"][index])):
        flash("Cell already solved!")
        for x in range(len(session["bluenums"])):
            if(session["bluenums"][x] == ","):
                listOfBluenums.append(int(session["bluenums"][a:x]))
                a = x+1
        return(render_template("sudoku formatting.html", nums=session["sudoku"], explain = [], methods= [], lets=letters, steps=0, blues=listOfBluenums,grays=session["grays"]))
    else:
        session["bluenums"] = session["bluenums"] + str(index) + ","
        session["sudoku"][index] = int(session["solution"][index])
        for x in range(len(session["bluenums"])):
            if(session["bluenums"][x] == ","):
                listOfBluenums.append(int(session["bluenums"][a:x]))
                a = x+1
        return(render_template("sudoku formatting.html", nums=session["sudoku"], methods= [], explain = [], lets=letters, steps=0, blues=listOfBluenums,grays=session["grays"]))
# play sudoku default page
@app.route("/playsudoku")
def playsudoku():
    session.pop("graynums", None)
    session.pop("sol", None)
    session.pop("puzzle", None)
    session.pop("numblues", None)
    session.pop("numreds", None)
    session.pop("methods",None)
    session.pop("orders",None)
    session.pop("numOfSteps", None)
    session.pop("smalls", None)
    session.pop("stepsDisplayed", None)
    session.pop('explain', None)    
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    return render_template("playsudokunew.html", solution = [0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], nums=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], methods = ["no"], lets=letters, blues = [82], grays = [82], reds = [82], s = [], dif="none")
# solves entire sudoku (playsudoku)
@app.route("/play/solve", methods=["GET","POST"])
def solvePuzzle():
    if not "puzzle" in session:
        return redirect(url_for("playsudoku"))
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    m = session["methods"]
    b = session["orders"]
    e = session["explain"]
    bluenums = []
    listOfOrders = []
    listOfMethods = []
    listOfExplains = []
    a = 0
    for x in range(len(m)):
        if(m[x] == ","):
            listOfMethods.append(m[a:x])
            a = x+1
    a = 0
    for x in range(len(b)):
        if(b[x] == ","):
            listOfOrders.append(b[a:x])
            a = x+1
    a = 0
    for x in range(len(e)):
        if(x != 0):
            if(e[x-1] == "." and e[x] == '.'):
                listOfExplains.append(e[a:x])
                a = x+1
    for p in range(81):
        if(int(listOfOrders[p]) > 0):
            bluenums.append(p)
    a = 0
    session["smalls"] = []
    session["numreds"] = []
    return render_template("playsudokunew.html", s=[],nums=session["sol"], explain = listOfExplains, solution = session["sol"], methods=listOfMethods, lets=letters, grays=session["graynums"], reds = [], blues=bluenums, dif = session["difficulty"])
@app.route("/play/onestep", methods=["GET","POST"])
def oneStepPlay():
    if not "puzzle" in session:
        return redirect(url_for("playsudoku"))
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    guesses = []
    numblues = session["numblues"]
    numreds = []
    smalls = session["smalls"]
    for i in range(81):
        if('#' + letters[i//9] + str(int(i%9 + 1)) in request.form):
            print('#' + letters[i//9] + str(int(i%9 + 1)))
            if(request.form['#' + letters[i//9] + str(int(i%9 + 1))] != ""):
                if(request.form['#' + letters[i//9] + str(int(i%9 + 1))].isnumeric()):
                    session["puzzle"][i] = int(request.form['#' + letters[i//9] + str(int(i%9 + 1))])
                    smalls.append(i)
        else:
            print(letters[i//9] + str(int(i%9 + 1)))
            if i not in session["graynums"]:
                if(request.form[letters[i//9] + str(int(i%9 + 1))] != "" ):
                    if(request.form[letters[i//9] + str(int(i%9 + 1))].isnumeric()):
                        session["puzzle"][i] = int(request.form[letters[i//9] + str(int(i%9 + 1))])
                        guesses.append(int(i))
                if(i in smalls):
                    smalls.remove(i)
    for n in guesses:
        if(request.form[letters[n//9] + str(int(n%9 + 1))] == str(session["sol"][n]) and n not in numblues):
            numblues.append(n)
            if n in numreds:
                for num in numreds:
                    if(num == n):
                        numreds.remove(num)
        else:
            if(n not in numblues):
                numreds.append(n)
    for i in smalls:
        if('#' + letters[i//9] + str(int(i%9 + 1)) in request.form):
            if(request.form['#' + letters[i//9] + str(int(i%9 + 1))] == ""):
                smalls.remove(i)
        else:
            if(request.form[letters[i//9] + str(int(i%9 + 1))] == ""):
                smalls.remove(i)
    session["smalls"] = smalls
    session["numblues"] = numblues
    session["numreds"] = numreds
    m = session["methods"]
    b = session["orders"]
    e = session["explain"]
    listOfOrders = []
    listOfMethods = []
    listOfExplains = []
    a = 0
    for x in range(len(m)):
        if(m[x] == ","):
            listOfMethods.append(m[a:x])
            a = x+1
    a = 0
    for x in range(len(b)):
        if(b[x] == ","):
            listOfOrders.append(b[a:x])
            a = x+1
    a = 0
    for x in range(len(e)):
        if(x != 0):
            if(e[x-1] == "." and e[x] == '.'):
                listOfExplains.append(e[a:x])
                a = x+1
    session["stepsDisplayed"] += 1
    found = 0
    print(listOfOrders)
    print(session["stepsDisplayed"])
    print(session["numblues"])
    explanation = ""
    while(session["stepsDisplayed"] < len(listOfMethods) and found == 0):
        for i in range(81):
            if(int(listOfOrders[i]) == session["stepsDisplayed"]):
                if(i in session["numblues"]):
                    session["stepsDisplayed"] += 1
                else:
                    session["numblues"].append(i)
                    found = 1
                    print(i)
                    print(session["numblues"])
                    session["puzzle"][i] = session["sol"][i]
                    explanation = listOfExplains[session["stepsDisplayed"] - 1]
    if(explanation == ""):
        return render_template("playsudokunew.html", s=smalls,nums=session["puzzle"], explain = [], methods = ["no"], solution = session["sol"], lets=letters, grays=session["graynums"], reds = session["numreds"], blues=session["numblues"], dif = session["difficulty"])
    method = listOfMethods[session["stepsDisplayed"] - 1]
    return render_template("playsudokunew.html", s=[],nums=session["puzzle"], explain = [explanation], methods = [method], solution = session["sol"], lets=letters, grays=session["graynums"], reds = session["numreds"], blues=session["numblues"], dif = session["difficulty"])
# clears grid to remove all human entries
@app.route("/play/clear", methods=["GET", "POST"])
def clear():
    if not "puzzle" in session:
        return redirect(url_for("playsudoku"))
    session["stepsDisplayed"] = 0
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    listOfBluenums = []
    a = 0
    for x in range(len(session["numblues"])):
        if(session["numblues"][x] == ","):
            listOfBluenums.append(int(session["numblues"][a:x]))
            a = x+1
    for x in range(len(session["puzzle"])):
        if x in listOfBluenums:
            session["puzzle"][x] = 0
    session["numblues"] = []
    session["numreds"] = []
    session["smalls"] = []
    return render_template("playsudokunew.html", s = [], solution = session["sol"], nums=session["puzzle"], methods = ["no"], lets=letters, grays = session["graynums"], reds = [], blues=[], dif = session["difficulty"])
# solves a particular cell (play sudoku)
@app.route("/play/solvecell", methods=["GET", "POST"])
def cellSolve():
    if not "puzzle" in session:
        return redirect(url_for("playsudoku"))
    cell = request.form["cell"]
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    index = -1
    for j in range(9):
        if(cell[0] == letters[j]):
            for i in range(1,10):
                if(cell[1] == str(i)):
                    index = 9*j + i - 1
    if(index == -1):
        flash('invalid cell, try again')
        return(render_template("playsudokunew.html", solution = session["sol"], nums=session["puzzle"], s = session["smalls"],methods= ["no"], lets=letters, grays=session["graynums"], blues=session["numblues"], dif = session["difficulty"], reds=session["numreds"]))
    if(index in session["numreds"]):
        numreds = session["numreds"]
        numreds.remove(index)
        session["numreds"] = numreds
    if(index in session["smalls"]):
        smalls = session["smalls"]
        smalls.remove(index)
        session["smalls"] = smalls
    if(index in session["numblues"]):
        flash("Cell already solved!")
        return(render_template("playsudokunew.html", solution = session["sol"], nums=session["puzzle"], s = session["smalls"],methods= ["no"], lets=letters, grays=session["graynums"], blues=session["numblues"], dif = session["difficulty"], reds=session["numreds"]))
    else:
        numblues = session["numblues"]
        numblues.append(index)
        session["puzzle"][index] = session["sol"][index]
        session["numblues"] = numblues
        return(render_template("playsudokunew.html", solution = session["sol"], s = session["smalls"],nums=session["puzzle"], methods= ["no"], lets=letters, grays=session["graynums"], blues=session["numblues"], dif = session["difficulty"], reds=session["numreds"]))
# generates sudoku by removing numbers from completed sudoku and trying to resolve it
@app.route("/playsudoku/<dif>", methods = ["GET", "POST"])
def makeSudoku(dif):
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        if(dif != "easy" and dif != "medium" and dif != "hard"):
            return redirect(url_for("playsudoku"))
        session.clear()
        session["difficulty"] = dif
        done = 0
        cells = np.empty((9,9),dtype=object)
        coinflip = random.randint(1,2)
        if(coinflip == 1):
            numbers = np.array([1,4,9,2,6,5,7,3,8,2,3,6,8,7,9,4,1,5,5,7,8,1,4,3,2,6,9,3,5,1,4,8,7,6,9,2,6,2,7,9,3,1,5,8,4,8,9,4,6,5,2,1,7,3,7,1,2,3,9,4,8,5,6,4,8,3,5,1,6,9,2,7,9,6,5,7,2,8,3,4,1])
        else:
            numbers = np.array([2,3,5,7,1,4,6,9,8,1,4,9,6,8,2,5,3,7,8,7,6,9,3,5,1,4,2,3,5,8,4,7,1,2,6,9,4,2,1,3,9,6,7,8,5,6,9,7,5,2,8,4,1,3,7,1,3,2,6,9,8,5,4,9,6,4,8,5,7,3,2,1,5,8,2,1,4,3,9,7,6])
        tempnum = copy.deepcopy(numbers)
        t = random.randint(0,2)
        if(t == 1):
            for i in range(54):
                numbers[i] = int(tempnum[i+27])
            for i in range(54,81):
                numbers[i] = int(tempnum[i-54])
        if(t == 2):
            for i in range(27):
                numbers[i] = int(tempnum[i+54])
            for i in range(27,81):
                numbers[i] = int(tempnum[i-27])
        tempnum = copy.deepcopy(numbers)
        c = random.randint(0,2)
        if(c == 1):
            for i in range(6):
               for j in range(9):
                   numbers[i+(9*j)] = int(tempnum[i+3+(9*j)])
            for i in range(6,9):
                for j in range(9):
                    numbers[i+(9*j)] = int(tempnum[i-6+(9*j)])
        if(c == 2):
            for i in range(3):
                for j in range(9):
                    numbers[i+(9*j)] = int(tempnum[i+6+(9*j)])
            for i in range(3,9):
                for j in range(9):
                    numbers[i+(9*j)] = int(tempnum[i-3+(9*j)])
        b = random.randint(0,8)
        for i in range(81):
            if(numbers[i] != 0):
                numbers[i] = (numbers[i]+b-1) % 9 + 1
        for i in range(81):
            cells[i//9][i%9] = Cell(numbers[i])
        sudoku = sudokuGrid(cells)
        runcap = 50
        if(dif == "medium"):
            runcap += 10
        if(dif == "hard"):
            runcap += 20
        runs = 0
        numlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
        while(runs < runcap):
            c = numlist[random.randint(0,len(numlist) - 1)]
            numlist.remove(c)
            s = sudoku.cells[c//9][c%9]
            if(s.value != 0):
                tempsud = copy.deepcopy(sudoku)
                runs+=1
                s.value = 0
                s.options = np.array([1,2,3,4,5,6,7,8,9])
                i = 0
                done = 0
                reset = copy.deepcopy(sudoku)
                while(done == 0 and i < 100):
                    if(runs <= 50):
                            a = sudoku.cellsSolved
                            if(s.value == 0):
                                sudoku.checkCells()
                            if(s.value == 0):
                                sudoku.checkBoxes()
                            if(s.value == 0):
                                sudoku.checkColumns()
                            if(s.value == 0):
                                sudoku.checkRows()
                            if(a == sudoku.cellsSolved):
                                i = 100
                    if(dif == "medium" and runs > 50):
                            a = sudoku.cellsSolved
                            if(s.value == 0):
                                sudoku.checkCells()
                            if(s.value == 0):
                                sudoku.checkBoxes()
                            if(s.value == 0):
                                sudoku.checkColumns()
                            if(s.value == 0):
                                sudoku.checkRows()
                            if(s.value == 0):
                                sudoku.nakedPairs()
                            if(s.value == 0):
                                sudoku.boxReduction()
                            if(s.value == 0):
                                sudoku.colReduction()
                            if(s.value == 0):
                                sudoku.rowReduction()
                            if(a == sudoku.cellsSolved):
                                i = 100
                    if(dif == "hard" and runs > 50):
                        a = sudoku.cellsSolved
                        if(s.value == 0):
                            sudoku.checkCells()
                        if(s.value == 0):
                             sudoku.checkBoxes()
                        if(s.value == 0):
                            sudoku.checkColumns()
                        if(s.value == 0):
                            sudoku.checkRows()
                        if(s.value == 0):
                            sudoku.xwing()
                        if(s.value == 0):
                            sudoku.xywing()
                        if(s.value == 0):
                            sudoku.nakedPairs()
                        if(s.value == 0):
                            sudoku.boxReduction()
                        if(s.value == 0):
                            sudoku.colReduction()
                        if(s.value == 0):
                              sudoku.rowReduction()
                        if(s.value == 0):
                            sudoku.nakedTriple()
                        if(a == sudoku.cellsSolved):
                            i = 100
                                                                               
                    i+=1
                    if(s.value != 0):  
                        sudoku = copy.deepcopy(reset)
                        done = 1
                    if(i >= 100):
                        sudoku = copy.deepcopy(tempsud)
        listOfMethods = ""
        listOfOrders = ""
        listOfExplains = ""
        store = copy.deepcopy(sudoku)
        if(dif == "easy"):
            i = 0
            while(i < 100):
                store.checkCells()
                store.checkBoxes()
                store.checkColumns()
                store.checkRows()
                if(store.checkDone == True):
                    i = 100
                i+=1
        if(dif == "medium"):
            i = 0
            while(i < 100):
                a = store.cellsSolved
                store.checkCells()
                store.checkBoxes()
                store.checkColumns()
                store.checkRows()    
                if(store.checkDone() == False):
                    store.nakedPairs()
                if(store.checkDone() == False):
                    store.boxReduction()
                if(store.checkDone() == False):
                    store.colReduction()
                if(store.checkDone() == False):
                    store.rowReduction()
                if(store.checkDone == True):
                    i = 100
                i+=1
        if(dif == "hard"):
            i = 0
            while(i < 100):
                a = store.cellsSolved
                store.checkCells()
                store.checkBoxes()
                store.checkColumns()
                store.checkRows()
                if(store.checkDone() == False):
                        store.xwing()
                if(store.checkDone() == False):
                        store.xywing()
                if(store.checkDone() == False):
                    store.nakedPairs()
                if(store.checkDone() == False):
                    store.boxReduction()
                if(store.checkDone() == False):
                    store.colReduction()
                if(store.checkDone() == False):
                    store.rowReduction()
                if(store.checkDone() == False):
                    store.nakedTriple()
                if(store.checkDone == True):
                    i = 100
                i+=1
        k = 0
        for i in range(9):
                for j in range(9):
                    listOfOrders = listOfOrders + str(int(store.cells[i][j].order)) + ","
        while(k <= store.cellsSolved):
            for i in range(9):
                for j in range(9):
                    if(store.cells[i][j].order == k):                
                        if(store.cells[i][j].method != 'given'):
                            listOfExplains = listOfExplains + store.cells[i][j].explain
                            listOfMethods = listOfMethods + 'Step ' + str(k) + ': cell ' + str(letters[i]) + str(j+1) + ' was solved by ' + store.cells[i][j].method + ","
            k += 1
        session["explain"] = listOfExplains
        session["methods"] = listOfMethods
        session["orders"] = listOfOrders
        session["numOfSteps"] = store.cellsSolved
        solution = []
        puzzle = []
        graynums = []
        for row in range(9):
            for col in range(9):
                solution.append(int(store.cells[row][col].value))
        for row in range(9):
            for col in range(9):
                puzzle.append(int(sudoku.cells[row][col].value))
                if(int(sudoku.cells[row][col].value) != 0):
                    graynums.append(9*row + col)
        session["sol"] = solution
        session["graynums"] = graynums
        print(puzzle)
        session["puzzle"] = puzzle
        session["numblues"] = [82]
        session["numreds"] = [82]
        session["smalls"] = []
        session["stepsDisplayed"] = 0
        return render_template("playsudokunew.html", solution = session["sol"], nums=puzzle, lets=letters, methods = ["no"], grays=graynums, s=[], reds=session["numreds"], blues=session["numblues"], dif=session["difficulty"])
    if(request.method == "POST"):
        if not "puzzle" in session:
            return redirect(url_for("playsudoku"))
        guesses = []
        numblues = session["numblues"]
        numreds = []
        smalls = session["smalls"]
        for i in range(81):
            if('#' + letters[i//9] + str(int(i%9 + 1)) in request.form):
                print('#' + letters[i//9] + str(int(i%9 + 1)))
                if(request.form['#' + letters[i//9] + str(int(i%9 + 1))] != ""):
                    if(request.form['#' + letters[i//9] + str(int(i%9 + 1))].isnumeric()):
                        session["puzzle"][i] = int(request.form['#' + letters[i//9] + str(int(i%9 + 1))])
                        smalls.append(i)
            else:
                print(letters[i//9] + str(int(i%9 + 1)))
                if i not in session["graynums"]:
                    if(request.form[letters[i//9] + str(int(i%9 + 1))] != "" ):
                        if(request.form[letters[i//9] + str(int(i%9 + 1))].isnumeric()):
                            session["puzzle"][i] = int(request.form[letters[i//9] + str(int(i%9 + 1))])
                            guesses.append(int(i))
                    if(i in smalls):
                        smalls.remove(i)
        for n in guesses:
            if(request.form[letters[n//9] + str(int(n%9 + 1))] == str(session["sol"][n]) and n not in numblues):
                numblues.append(n)
                if n in numreds:
                    for num in numreds:
                        if(num == n):
                            numreds.remove(num)
            else:
                if(n not in numblues):
                    numreds.append(n)
        for i in smalls:
            if('#' + letters[i//9] + str(int(i%9 + 1)) in request.form):
                if(request.form['#' + letters[i//9] + str(int(i%9 + 1))] == ""):
                    smalls.remove(i)
            else:
                if(request.form[letters[i//9] + str(int(i%9 + 1))] == ""):
                    smalls.remove(i)
        session["smalls"] = smalls
        session["numblues"] = numblues
        session["numreds"] = numreds
        return render_template("playsudokunew.html", solution = session["sol"], methods = ['no'], nums=session["puzzle"], s = session["smalls"],lets=letters, grays=session["graynums"], blues=session["numblues"], dif = session["difficulty"], reds=session["numreds"])

@app.route("/numbersnake", methods=["GET", "POST"])
def numbersnake():
    numbers = [1,0,0,20,0,0,0,0,25,0,5,0,0,0,0,58,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,54,0,0,65,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,0,0,76,0,0,0,36,0,0,0,48,81,0,0,0,0,0,0,0,0,0,41,0,0,0,33]
    numbersnake = numbersnakegrid(numbers)
    for n in range(5):
        numbersnake.straightlinesolve()
        numbersnake.onedirection()
        numbersnake.pathexclusion()
        numbersnake.oneawaypathexclusion()
    numbersnake.onepathleft()
    givens = []
    for i in range(81):
        if(numbers[i] != 0):
            givens.append(i)
    solution = [3,2,23,24,29,30,31,32,33,4,1,22,25,28,37,36,35,34,5,20,21,26,27,38,39,74,75,6,19,44,43,42,41,40,73,76,7,18,45,68,69,70,71,72,77,8,17,46,67,66,65,64,81,78,9,16,47,48,61,62,63,80,79,10,15,14,49,60,59,58,57,56,11,12,13,50,51,52,53,54,55]
    return render_template("numbersnake.html", grays=givens,nums=numbers, sol=solution)
# tic tac toe easter egg
@app.route("/tictactoe", methods=["GET","POST"])
def ultimate():
    listOfCoords = []
    if(request.method == "GET"):
        session["board"] = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"
        session["boxes"] = "CCCCCCCCC"
        session["topleft"] = "CCCCCCCCC"
        session["topcenter"] = "CCCCCCCCC"
        session["topright"] = "CCCCCCCCC"
        session["middleleft"] = "CCCCCCCCC"
        session["middlecenter"] = "CCCCCCCCC"
        session["middleright"] = "CCCCCCCCC"
        session["bottomleft"] = "CCCCCCCCC"
        session["bottomcenter"] = "CCCCCCCCC"
        session["bottomright"] = "CCCCCCCCC"
        session["player"] = 1
        session["p1symbol"] = ""
        session["p2symbol"] = ""
        session["square"] = 0
        session["js"] = []
        for x in range(81):
            session["js"].append(x)
        return render_template("ultimate.html", board=session["board"], boxes=session["boxes"], player=session["player"], boxnumber = session["square"], win=False)
    else:
        letters = np.array(['A','B','C','D','E','F','G','H','I'])
        for i in range(81):
            t = letters[i//9] + str(i%9 + 1)
            listOfCoords.append(t)
            if(request.form[t] != ''):
                if(session["square"] == 0):
                    a = (i%9)//3 + 3*(i//27) + 1
                    print(a)
                    if(session["boxes"][a-1] != 'C'):
                        flash('Box already completed, try again!')
                        return render_template("ultimate.html", board=session["board"], boxes=session["boxes"], player=session["player"],coords=listOfCoords, boxnumber = session["square"], win=False)
                if(session["player"] == 1):
                    if(session["p1symbol"] == ""):
                        session["p1symbol"] = request.form[t]
                    else:
                        if(request.form[t] != session["p1symbol"]):
                            flash("incorrect character, try again")
                            return render_template("ultimate.html", board=session["board"], boxes=session["boxes"], player=session["player"],coords=listOfCoords, boxnumber = session["square"], win=False)
                else:
                    if(session["p2symbol"] == ""):
                        session["p2symbol"] = request.form[t]
                    else:
                        if(request.form[t] != session["p2symbol"]):
                            flash("wrong character, try again")
                            return render_template("ultimate.html", board=session["board"], boxes=session["boxes"], player=session["player"],coords=listOfCoords, boxnumber = session["square"], win=False)

                if(i not in session["js"] and session["square"] != 0):
                    flash("Incorrect box, try again")
                    return render_template("ultimate.html", board=session["board"], boxes=session["boxes"], player=session["player"],coords=listOfCoords, boxnumber = session["square"], win=False)
                if(session["board"][i] != 'C'):
                    flash("Cell already filled, try again")
                    return render_template("ultimate.html", board=session["board"], boxes=session["boxes"], player=session["player"],coords=listOfCoords, boxnumber = session["square"], win=False)
                session["board"] = session["board"][0:i] + request.form[t] + session["board"][i+1:81]
                session["square"] = 3*((i%27)//9) + i%3 + 1
        session["js"] = []
        for j in range(81):
            if(3*(j//27) + (j%9)//3 + 1 == session["square"]):
                session["js"].append(j)
        temp = session["board"]
        session["topleft"] = temp[0]+temp[1]+temp[2]+temp[9]+temp[10]+temp[11]+temp[18]+temp[19]+temp[20]
        session["topcenter"] = temp[3]+temp[4]+temp[5]+temp[12]+temp[13]+temp[14]+temp[21]+temp[22]+temp[23]
        session["topright"] = temp[6]+temp[7]+temp[8]+temp[15]+temp[16]+temp[17]+temp[24]+temp[25]+temp[26]
        session["middleleft"] = temp[27]+temp[28]+temp[29]+temp[36]+temp[37]+temp[38]+temp[45]+temp[46]+temp[47]
        session["middlecenter"] = temp[30]+temp[31]+temp[32]+temp[39]+temp[40]+temp[41]+temp[48]+temp[49]+temp[50]
        session["middleright"] = temp[33]+temp[34]+temp[35]+temp[42]+temp[43]+temp[44]+temp[51]+temp[52]+temp[53]
        session["bottomleft"] = temp[54]+temp[55]+temp[56]+temp[63]+temp[64]+temp[65]+temp[72]+temp[73]+temp[74]
        session["bottomcenter"] = temp[57]+temp[58]+temp[59]+temp[66]+temp[67]+temp[68]+temp[75]+temp[76]+temp[77]
        session["bottomright"] = temp[60]+temp[61]+temp[62]+temp[69]+temp[70]+temp[71]+temp[78]+temp[79]+temp[80]
        listOfLetters = [session["topleft"],session["topcenter"],session["topright"],session["middleleft"],session["middlecenter"],session["middleright"],session["bottomleft"],session["bottomcenter"],session["bottomright"]]
        listOfBoxes = []
        results = ""
        for a in range(len(listOfLetters)):
            listOfBoxes.append(Box(listOfLetters[a], a + 1))
        for box in listOfBoxes:
            a = box.value
            box.diags()
            box.rows()
            box.cols()
            results += box.value
            if("C" != box.value):
                if(int(session["square"]) == box.number):
                    session["square"] = 0
        session["boxes"] = results
        b = Box(session["boxes"], 9)
        b.diags()
        b.rows()
        b.cols()
        if(b.value != "C"):
            flash("Player " + str(session["player"]) + " is the winner!")
            return render_template("ultimate.html", board=session["board"], boxes=session["boxes"], player=session["player"],coords=listOfCoords, boxnumber = session["square"], win=True)
        session["player"] = (session["player"] % 2) + 1
    return render_template("ultimate.html", board=session["board"], boxes=session["boxes"], player=session["player"],coords=listOfCoords, boxnumber = session["square"], win=False)
@app.route("/finalproject", methods=["GET", "POST"])
def finalproject():
    return render_template("relifinalproject.html")
@app.route("/finalproject/content", methods=["GET","POST"])
def content():
    return render_template("relifinalprojectcontent.html")
@app.route("/finalproject/sources", methods=["GET","POST"])
def sources():
    return render_template("relifinalprojectsources.html")
@app.route("/finalproject/quiz", methods=["GET", "POST"])
def quiz():
    if(request.method == "GET"):
        session.pop("i", None)
        session.pop("level",None)
        session.pop("minimum",None)
        return render_template("relifinalprojectquiz.html",i=0,n='no', s=0, round = 0, m=0, x=0, y=0, mobx = 0, moby = 0, loc="none")
    if(request.method == "POST"):
        session["destinations"] = [0,5,5,5]
        session["nextround"] = ['no', 'no', 'no',  'no']
        if not "i" in session:
            session["i"] = 1
        if not "level" in session:
            session["level"] = 1
        else:
            session["i"] += 1
        session["minimum"] = int(session["level"] % 4 * 10000 + 10000)
        if(session["i"] > session["destinations"][session["level"]]):
            session["i"] = 0
            if(session["level"] == 3):
                minimum = 50000
                return render_template("relifinalprojectquiz.html",i=0,n=session["nextround"][session["level"]],s=minimum, round=99, m=minimum, x=0, y=0, mobx = 0, moby = 0, loc="none")
            session["level"] += 1
            minimum = int(session["level"] % 6 * 10000 + 10000)
            return render_template("relifinalprojectquiz.html", i=0,n=session["nextround"][session["level"]], s=minimum, round=session["level"], m=minimum, x=0, y=0, mobx = 0, moby = 0,loc="none")
        i = session["i"]
        if(session["level"] == 1):
            if(i == 1):
                mapx = 104
                mapy = 196
                place = "Los Angeles, California"
            if(i == 2):
                mapx = 235
                mapy = 195
                place = "Chaco, New Mexico"
            if(i == 3):
                mapx = 183
                mapy = 209
                place = "Phoenix, Arizona"
            if(i == 4):
                mapx = 325
                mapy = 349
                place = "Mexico City, Mexico"
            if(i == 5):
                mapx = 243
                mapy = 235
                place = "Juarez, Chihuahua, Mexico"
        if(session["level"] == 2):
            if(i == 1):
                mapx = 255
                mapy = 202
                place = "Santa Fe, New Mexico"
            if(i == 2):
                mapx = 324
                mapy = 348
                place = "Tepeyac Mountain, Mexico"
            if(i == 3):
                mapx = 335
                mapy = 260
                place = "San Antonio, Texas"
            if(i == 4):
                mapx = 120
                mapy = 214
                place = "Tijuana, Baja California, Mexico"
            if(i == 5):
                mapx = 322
                mapy = 274
                place = "Laredo, Texas"
        if(session["level"] == 3):
            if(i == 1):
                mapx = 452
                mapy = 140
                place = "Second Tepeyac, Illinois"
            if(i == 2):
                mapx = 255
                mapy = 198
                place = "Santuario de Chimayo"
            if(i == 3):
                mapx = 183
                mapy = 247
                place = "Magdalena de Kino, Mexico"
            if(i == 4):
                mapx = 187
                mapy = 235
                place = "Nogales, Mexico/Arizona"
            if(i == 5):
                mapx = 324
                mapy = 348
                place = "Basilica of our Lady of Guadalupe"
        mobilex = mapx*3/8
        mobiley = mapy*3/8
        return render_template("relifinalprojectquiz.html", i=session["i"],m=0, n=session["nextround"][session["level"]],s=session["minimum"],round=session["level"], x=mapx, y=mapy, mobx = mobilex, moby = mobiley, loc=place)
if(__name__ == "__main__"):
    app.run()
