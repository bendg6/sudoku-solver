# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:56:34 2022

@author: bendg
"""
import numpy as np
import time as time
import math as math
import copy as copy
#numbers is a list of the starting cells from top left across the rows, 0 for empty cells
class Cell(object):
    def __init__(self,value):
        self.value = value
        self.order = 0
        if(self.value == 0):
            self.options = np.array([1,2,3,4,5,6,7,8,9])
            self.method = ''
        else:
            self.options = [value]
            self.method = 'given'
    def removeOption(self,number,method,grid):
        templist = np.ndarray.tolist(self.options)
        if(number in templist): 
            templist.remove(number)
            if(len(templist) == 1):
                self.method = method
                grid.cellsSolved += 1
                self.order = grid.cellsSolved
        newOptions = np.asarray(templist)
        self.options = newOptions
class sudokuGrid(object):
    def __init__(self,cells):
        self.cells = cells
        self.guessNaked = 0
        self.nakedPairs = 0
        self.cellsSolved = 0
    def checkCells(self):
        for i in range(9):
            for j in range(9):
                if(self.cells[i][j].value != 0):
                    self.cells[i][j].options = np.array([self.cells[i][j].value])
                else:
                    for y in range(9):
                        if(self.cells[i][y].value in self.cells[i][j].options):
                            self.cells[i][j].removeOption(self.cells[i][y].value,'checkCells',self)
                    for x in range(9):
                        if(self.cells[x][j].value in self.cells[i][j].options):
                            self.cells[i][j].removeOption(self.cells[x][j].value,'checkCells',self)
                    if(i < 3 and j < 3):
                        for x in range(3):
                            for y in range(3):
                                if(self.cells[x][y].value in self.cells[i][j].options):
                                    self.cells[i][j].removeOption(self.cells[x][y].value,'checkCells',self)
                    if(i > 2 and i < 6 and j < 3):
                        for x in range(3,6):
                            for y in range(3):
                                if(self.cells[x][y].value in self.cells[i][j].options):
                                    self.cells[i][j].removeOption(self.cells[x][y].value,'checkCells',self)
                    if(i > 5 and j < 3):
                        for x in range(6,9):
                            for y in range(3):
                                if(self.cells[x][y].value in self.cells[i][j].options):
                                    self.cells[i][j].removeOption(self.cells[x][y].value,'checkCells',self)
                    if(i < 3 and j > 2 and j < 6):
                        for x in range(3):
                            for y in range(3,6):
                                if(self.cells[x][y].value in self.cells[i][j].options):
                                    self.cells[i][j].removeOption(self.cells[x][y].value,'checkCells',self)
                    if(i > 2 and i < 6 and j > 2 and j < 6):
                        for x in range(3,6):
                            for y in range(3,6):
                                if(self.cells[x][y].value in self.cells[i][j].options):
                                    self.cells[i][j].removeOption(self.cells[x][y].value,'checkCells',self)
                    if(i > 5 and j > 2 and j < 6):
                        for x in range(6,9):
                            for y in range(3,6):
                                if(self.cells[x][y].value in self.cells[i][j].options):
                                    self.cells[i][j].removeOption(self.cells[x][y].value,'checkCells',self)
                    if(i < 3 and j > 5):
                        for x in range(3):
                            for y in range(6,9):
                                if(self.cells[x][y].value in self.cells[i][j].options):
                                    self.cells[i][j].removeOption(self.cells[x][y].value,'checkCells',self)
                    if(i > 2 and i < 6 and j > 5):
                        for x in range(3,6):
                            for y in range(6,9):
                                if(self.cells[x][y].value in self.cells[i][j].options):
                                    self.cells[i][j].removeOption(self.cells[x][y].value,'checkCells',self)
                    if(i > 5 and j > 5):
                        for x in range(6,9):
                            for y in range(6,9):
                                if(self.cells[x][y].value in self.cells[i][j].options):
                                    self.cells[i][j].removeOption(self.cells[x][y].value,'checkCells',self)
                    if(self.cells[i][j].options.size == 1):
                        self.cells[i][j].value = self.cells[i][j].options[0]
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'    
    def checkBoxes(self):
        unknowns = [1,2,3,4,5,6,7,8,9]
        knowns = []
        for x in range(3):
            for y in range(3):
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
            for x in range(3):
                for y in range(3):
                    if (value in self.cells[x][y].options):
                        counter += 1
                        i = x
                        j = y
            if(counter == 1):
                self.cells[i][j].value = unknownarr[u]
                self.cells[i][j].options = np.array([unknownarr[u]])
                self.cells[i][j].method = 'checkBoxes'
                self.cellsSolved += 1
                self.cells[i][j].order = self.cellsSolved
        unknowns = [1,2,3,4,5,6,7,8,9]  
        knowns = []
        for x in range(3,6):
            for y in range(3):
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
            for x in range(3,6):
                for y in range(3):
                    if (value in self.cells[x][y].options):
                        counter = counter + 1
                        i = x
                        j = y
            if(counter == 1):
                self.cells[i][j].value = unknownarr[u]
                self.cells[i][j].options = np.array([unknownarr[u]])
                self.cells[i][j].method = 'checkBoxes'
                self.cellsSolved += 1
                self.cells[i][j].order = self.cellsSolved
        unknowns = [1,2,3,4,5,6,7,8,9]
        knowns = []
        for x in range(6,9):
            for y in range(3):
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
            for x in range(6,9):
                for y in range(3):
                    if (value in self.cells[x][y].options):
                        counter = counter + 1
                        i = x
                        j = y
            if(counter == 1):
                self.cells[i][j].value = unknownarr[u]
                self.cells[i][j].options = np.array([unknownarr[u]])
                self.cells[i][j].method = 'checkBoxes'
                self.cellsSolved += 1
                self.cells[i][j].order = self.cellsSolved
        unknowns = [1,2,3,4,5,6,7,8,9]
        knowns = []
        for x in range(3):
            for y in range(3,6):
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
            for x in range(3):
                for y in range(3,6):
                    if (value in self.cells[x][y].options):
                        counter = counter + 1
                        i = x
                        j = y
            if(counter == 1):
                self.cells[i][j].value = unknownarr[u]
                self.cells[i][j].options = np.array([unknownarr[u]])
                self.cells[i][j].method = 'checkBoxes'
                self.cellsSolved += 1
                self.cells[i][j].order = self.cellsSolved
        unknowns = [1,2,3,4,5,6,7,8,9]
        knowns = []
        for x in range(3,6):
            for y in range(3,6):
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
            for x in range(3,6):
                for y in range(3,6):
                    if (value in self.cells[x][y].options):
                        counter = counter + 1
                        i = x
                        j = y
            if(counter == 1):
                self.cells[i][j].value = unknownarr[u]
                self.cells[i][j].options = np.array([unknownarr[u]])
                self.cells[i][j].method = 'checkBoxes'
                self.cellsSolved += 1
                self.cells[i][j].order = self.cellsSolved
        unknowns = [1,2,3,4,5,6,7,8,9]
        knowns = []
        for x in range(6,9):
            for y in range(3,6):
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
            for x in range(6,9):
                for y in range(3,6):
                    if (value in self.cells[x][y].options):
                        counter = counter + 1
                        i = x
                        j = y
            if(counter == 1):
                self.cells[i][j].value = unknownarr[u]
                self.cells[i][j].options = np.array([unknownarr[u]])
                self.cells[i][j].method = 'checkBoxes'
                self.cellsSolved += 1
                self.cells[i][j].order = self.cellsSolved
        unknowns = [1,2,3,4,5,6,7,8,9]
        knowns = []
        for x in range(3):
            for y in range(6,9):
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
            for x in range(3):
                for y in range(6,9):
                    if (value in self.cells[x][y].options):
                        counter = counter + 1
                        i = x
                        j = y
            if(counter == 1):
                self.cells[i][j].value = unknownarr[u]
                self.cells[i][j].options = np.array([unknownarr[u]])
                self.cells[i][j].method = 'checkBoxes'
                self.cellsSolved += 1
                self.cells[i][j].order = self.cellsSolved
        unknowns = [1,2,3,4,5,6,7,8,9]
        knowns = []
        for x in range(3,6):
            for y in range(6,9):
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
            for x in range(3,6):
                for y in range(6,9):
                    if (value in self.cells[x][y].options):
                        counter = counter + 1
                        i = x
                        j = y
            if(counter == 1):
                self.cells[i][j].value = unknownarr[u]
                self.cells[i][j].options = np.array([unknownarr[u]])
                self.cells[i][j].method = 'checkBoxes'
                self.cellsSolved += 1
                self.cells[i][j].order = self.cellsSolved
        unknowns = [1,2,3,4,5,6,7,8,9]
        knowns = []
        for x in range(6,9):
            for y in range(6,9):
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
            for x in range(6,9):
                for y in range(6,9):
                    if (value in self.cells[x][y].options):
                        counter = counter + 1
                        i = x
                        j = y
            if(counter == 1):
                self.cells[i][j].value = unknownarr[u]
                self.cells[i][j].options = np.array([unknownarr[u]])
                self.cells[i][j].method = 'checkBoxes'
                self.cellsSolved += 1
                self.cells[i][j].order = self.cellsSolved
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def checkRows(self):
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
                j = 0
                value = unknownarr[u]
                for col in range(9):
                    #tries to find an unused number with only one valid location
                    if (value in self.cells[row][col].options):
                        counter = counter + 1
                        j = col
                if(counter == 1):
                    self.cells[row][j].value = unknownarr[u]
                    self.cells[row][j].options = np.array([unknownarr[u]])
                    self.cells[row][j].method = 'checkRows'
                    self.cellsSolved += 1
                    self.cells[row][j].order = self.cellsSolved
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def checkColumns(self):
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
                i = 0
                value = unknownarr[u]
                for row in range(9):
                    #tries to find an unused number with only one valid location
                    if (value in self.cells[row][col].options):
                        counter = counter + 1
                        i = row
                if(counter == 1):
                    self.cells[i][col].value = unknownarr[u]
                    self.cells[i][col].options = np.array([unknownarr[u]])
                    self.cells[i][col].method = 'checkColumns'
                    self.cellsSolved += 1
                    self.cells[i][col].order = self.cellsSolved
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def checkNakedSets(self):
        for i in range(9):
            for j in range(9):
                p = self.cells[i][j].options
                for n in range(2,5):
                    if(p.size == n):
                        identicalBoxes = 1
                        vals = [j]
                        for col in range(9):
                            if(np.array_equal(self.cells[i][col].options,p) and col!=j):
                                identicalBoxes += 1
                                vals.append(col)
                        if(identicalBoxes == n):
                            for col in range(9):
                                if not(col in vals):
                                    for x in range(p.size):
                                        self.cells[i][col].removeOption(p[x],'checkNakedSets',self)
                                        if(self.cells[i][col].options.size == 0):
                                            return 'error'
                        identicalBoxes = 1
                        vals = [i]
                        for row in range(9):
                            if(np.array_equal(self.cells[row][j].options,p) and row!=i):
                                identicalBoxes += 1
                                vals.append(row)
                        if(identicalBoxes == n):
                            for row in range(9):
                                if not(row in vals):
                                    for x in range(p.size):
                                        self.cells[row][j].removeOption(p[x],'checkNakedSets',self)
                                        if(self.cells[row][j].options.size == 0):
                                            return 'error'
                        identicalBoxes = 1
                        vals = [self.cells[i][j]]
                        if(i < 3 and j < 3):
                            for l in range(3):
                                for m in range(3):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       vals.append(self.cells[l][m])
                            if(n == identicalBoxes):
                                for x in range(3):
                                     for y in range(3):
                                         if(not(self.cells[x][y] in vals)):
                                             for len in range(p.size):
                                                 self.cells[x][y].removeOption(p[len],'checkNakedSets',self)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
                        identicalBoxes = 1
                        vals = [self.cells[i][j]]
                        if(2 < i < 6 and j < 3):
                            for l in range(3,6):
                                for m in range(3):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       vals.append(self.cells[l][m])
                            if(n == identicalBoxes):
                                for x in range(3,6):
                                     for y in range(3):
                                         if(not(self.cells[x][y] in vals)):
                                             for len in range(p.size):
                                                 self.cells[x][y].removeOption(p[len],'checkNakedSets',self)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
                        identicalBoxes = 1
                        vals = [self.cells[i][j]]
                        if(i > 5 and j < 3):
                            for l in range(6,9):
                                for m in range(3):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       vals.append(self.cells[l][m])
                            if(n == identicalBoxes):
                                for x in range(6,9):
                                     for y in range(3):
                                         if(not(self.cells[x][y] in vals)):
                                             for len in range(p.size):
                                                 self.cells[x][y].removeOption(p[len],'checkNakedSets',self)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
                        identicalBoxes = 1
                        vals = [self.cells[i][j]]
                        if(i < 3 and 2 < j < 6):
                            for l in range(3):
                                for m in range(3,6):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       vals.append(self.cells[l][m])
                            if(n == identicalBoxes):
                                for x in range(3):
                                     for y in range(3,6):
                                         if(not(self.cells[x][y] in vals)):
                                             for len in range(p.size):
                                                 self.cells[x][y].removeOption(p[len],'checkNakedSets',self)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
                        identicalBoxes = 1
                        vals = [self.cells[i][j]]
                        if(2 < i < 6 and 2 < j < 6):
                            for l in range(3,6):
                                for m in range(3,6):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       vals.append(self.cells[l][m])
                            if(n == identicalBoxes):
                                for x in range(3,6):
                                     for y in range(3,6):
                                         if(not(self.cells[x][y] in vals)):
                                             for len in range(p.size):
                                                 self.cells[x][y].removeOption(p[len],'checkNakedSets',self)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
                        identicalBoxes = 1
                        vals = [self.cells[i][j]]
                        if(i > 5 and 2 < j < 6):
                            for l in range(6,9):
                                for m in range(3,6):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       vals.append(self.cells[l][m])
                            if(n == identicalBoxes):
                                for x in range(6,9):
                                     for y in range(3,6):
                                         if(not(self.cells[x][y] in vals)):
                                             for len in range(p.size):
                                                 self.cells[x][y].removeOption(p[len],'checkNakedSets',self)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
                        identicalBoxes = 1
                        vals = [self.cells[i][j]]
                        if(i < 3 and j > 5):
                            for l in range(3):
                                for m in range(6,9):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       vals.append(self.cells[l][m])
                            if(n == identicalBoxes):
                                for x in range(3):
                                     for y in range(6,9):
                                         if(not(self.cells[x][y] in vals)):
                                             for len in range(p.size):
                                                 self.cells[x][y].removeOption(p[len],'checkNakedSets',self)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
                        identicalBoxes = 1
                        vals = [self.cells[i][j]]
                        if(2 < i < 6 and 5 < j):
                            for l in range(3,6):
                                for m in range(6,9):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       vals.append(self.cells[l][m])
                            if(n == identicalBoxes):
                                for x in range(3,6):
                                     for y in range(6,9):
                                         if(not(self.cells[x][y] in vals)):
                                             for len in range(p.size):
                                                 self.cells[x][y].removeOption(p[len],'checkNakedSets',self)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
                        identicalBoxes = 1
                        vals = [self.cells[i][j]]
                        if(5 < i and 5 < j):
                            for l in range(6,9):
                                for m in range(6,9):
                                    if(np.array_equal(self.cells[l][m].options,p) and (l!=i or m!=j)):
                                       identicalBoxes += 1
                                       vals.append(self.cells[l][m])
                            if(n == identicalBoxes):
                                for x in range(6,9):
                                     for y in range(6,9):
                                         if(not(self.cells[x][y] in vals)):
                                             for len in range(p.size):
                                                 self.cells[x][y].removeOption(p[len],'checkNakedSets',self)
                                                 if(self.cells[x][y].options.size == 0):
                                                     return 'error'
                if(self.cells[i][j].options.size == 1):
                    self.cells[i][j].value = self.cells[i][j].options[0]
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def boxElimination(self):
        unknowns = [1,2,3,4,5,6,7,8,9]
        for x in range(3):
            for y in range(3):
                if(self.cells[x][y].value in unknowns):
                    unknowns.remove(self.cells[x][y].value)
        unknownarr = np.asarray(unknowns)
        for u in range(unknownarr.size):
            rows = np.array([])
            cols = np.array([])
            for x in range(3):
                for y in range(3):
                    if(unknownarr[u] in self.cells[x][y].options):
                        rows = np.append(rows,x)
                        cols = np.append(cols,y)
            if(rows.size != 0):
                if(np.all(rows == rows[0]) and rows.size > 1):
                    for col in range(3,9):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                if(np.all(cols == cols[0])and cols.size > 1):
                    for row in range(3,9):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
        unknowns = [1,2,3,4,5,6,7,8,9]
        for x in range(3,6):
            for y in range(3):
                if(self.cells[x][y].value in unknowns):
                    unknowns.remove(self.cells[x][y].value)
        unknownarr = np.asarray(unknowns)
        for u in range(unknownarr.size):
            rows = np.array([])
            cols = np.array([])
            for x in range(3,6):
                for y in range(3):
                    if(unknownarr[u] in self.cells[x][y].options):
                        rows = np.append(rows,x)
                        cols = np.append(cols,y)
            if(rows.size != 0):
                if(np.all(rows == rows[0])and rows.size > 1):
                    for col in range(3,9):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                if(np.all(cols == cols[0])and cols.size > 1):
                    for row in range(0,3):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
                    for row in range(6,9):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self) 
        unknowns = [1,2,3,4,5,6,7,8,9]
        for x in range(6,9):
            for y in range(3):
                if(self.cells[x][y].value in unknowns):
                    unknowns.remove(self.cells[x][y].value)
        unknownarr = np.asarray(unknowns)
        for u in range(unknownarr.size):
            rows = np.array([])
            cols = np.array([])
            for x in range(6,9):
                for y in range(3):
                    if(unknownarr[u] in self.cells[x][y].options):
                        rows = np.append(rows,x)
                        cols = np.append(cols,y)
            if(rows.size != 0):
                if(np.all(rows == rows[0])and rows.size > 1):
                    for col in range(3,9):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                if(np.all(cols == cols[0])and cols.size > 1):
                    for row in range(6):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
        unknowns = [1,2,3,4,5,6,7,8,9]
        for x in range(3):
            for y in range(3,6):
                if(self.cells[x][y].value in unknowns):
                    unknowns.remove(self.cells[x][y].value)
        unknownarr = np.asarray(unknowns)
        for u in range(unknownarr.size):
            rows = np.array([])
            cols = np.array([])
            for x in range(3):
                for y in range(3,6):
                    if(unknownarr[u] in self.cells[x][y].options):
                        rows = np.append(rows,x)
                        cols = np.append(cols,y)
            if(rows.size != 0):
                if(np.all(rows == rows[0])and rows.size > 1):
                    for col in range(0,3):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                    for col in range(6,9):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                if(np.all(cols == cols[0])and cols.size > 1):
                    for row in range(3,9):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
        unknowns = [1,2,3,4,5,6,7,8,9]
        for x in range(3,6):
            for y in range(3,6):
                if(self.cells[x][y].value in unknowns):
                    unknowns.remove(self.cells[x][y].value)
        unknownarr = np.asarray(unknowns)
        for u in range(unknownarr.size):
            rows = np.array([])
            cols = np.array([])
            for x in range(3,6):
                for y in range(3,6):
                    if(unknownarr[u] in self.cells[x][y].options):
                        rows = np.append(rows,x)
                        cols = np.append(cols,y)
            if(rows.size != 0):
                if(np.all(rows == rows[0])and rows.size > 1):
                    for col in range(0,3):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                    for col in range(6,9):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                if(np.all(cols == cols[0])and cols.size > 1):
                    for row in range(0,3):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
                    for row in range(6,9):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
        unknowns = [1,2,3,4,5,6,7,8,9]
        for x in range(6,9):
            for y in range(3,6):
                if(self.cells[x][y].value in unknowns):
                    unknowns.remove(self.cells[x][y].value)
        unknownarr = np.asarray(unknowns)
        for u in range(unknownarr.size):
            rows = np.array([])
            cols = np.array([])
            for x in range(6,9):
                for y in range(3,6):
                    if(unknownarr[u] in self.cells[x][y].options):
                        rows = np.append(rows,x)
                        cols = np.append(cols,y)
            if(rows.size != 0):
                if(np.all(rows == rows[0])and rows.size > 1):
                    for col in range(0,3):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                    for col in range(6,9):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                if(np.all(cols == cols[0])and cols.size > 1):
                    for row in range(6):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
        unknowns = [1,2,3,4,5,6,7,8,9]
        for x in range(3):
            for y in range(6,9):
                if(self.cells[x][y].value in unknowns):
                    unknowns.remove(self.cells[x][y].value)
        unknownarr = np.asarray(unknowns)
        for u in range(unknownarr.size):
            rows = np.array([])
            cols = np.array([])
            for x in range(3):
                for y in range(6,9):
                    if(unknownarr[u] in self.cells[x][y].options):
                        rows = np.append(rows,x)
                        cols = np.append(cols,y)
            if(rows.size != 0):
                if(np.all(rows == rows[0])and rows.size > 1):
                    for col in range(6):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                if(np.all(cols == cols[0])and cols.size > 1):
                    for row in range(3,9):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
        unknowns = [1,2,3,4,5,6,7,8,9]
        for x in range(3,6):
            for y in range(6,9):
                if(self.cells[x][y].value in unknowns):
                    unknowns.remove(self.cells[x][y].value)
        unknownarr = np.asarray(unknowns)
        for u in range(unknownarr.size):
            rows = np.array([])
            cols = np.array([])
            for x in range(3,6):
                for y in range(6,9):
                    if(unknownarr[u] in self.cells[x][y].options):
                        rows = np.append(rows,x)
                        cols = np.append(cols,y)
            if(rows.size != 0):
                if(np.all(rows == rows[0])and rows.size > 1):
                    for col in range(6):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                if(np.all(cols == cols[0])and cols.size > 1):
                    for row in range(0,3):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
                    for row in range(6,9):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
        unknowns = [1,2,3,4,5,6,7,8,9]
        for x in range(6,9):
            for y in range(6,9):
                if(self.cells[x][y].value in unknowns):
                    unknowns.remove(self.cells[x][y].value)
        unknownarr = np.asarray(unknowns)
        for u in range(unknownarr.size):
            rows = np.array([])
            cols = np.array([])
            for x in range(6,9):
                for y in range(6,9):
                    if(unknownarr[u] in self.cells[x][y].options):
                        rows = np.append(rows,x)
                        cols = np.append(cols,y)
            if(rows.size != 0):
                if(np.all(rows == rows[0])and rows.size > 1):
                    for col in range(6):
                        self.cells[int(rows[0])][col].removeOption(unknownarr[u],'boxElimination',self)
                if(np.all(cols == cols[0])and cols.size > 1):
                    for row in range(6):
                        self.cells[row][int(cols[0])].removeOption(unknownarr[u],'boxElimination',self)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def rowElimination(self):
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
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                        for x in range(row + 1,3):
                            for y in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                    if(2 < row < 6):
                        for x in range(3,row): 
                            for y in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                        for x in range(row+1,6):
                            for y in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                    if(5 < row):
                        for x in range(6,row): 
                            for y in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                        for x in range((row + 1),9):
                            for y in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                if(np.all(2 < cols) and np.all(cols < 6) and cols.size > 1):
                    if(row < 3):
                        for x in range(row):
                            for y in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                        for x in range(row + 1,3):
                            for y in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                    if(2 < row < 6):
                        for x in range(3,row): 
                            for y in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                        for x in range(row+1,6):
                            for y in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                    if(5 < row):
                        for x in range(6,row): 
                            for y in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                        for x in range((row + 1),9):
                            for y in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                if(np.all(cols > 5)and cols.size > 1):
                    if(row < 3):
                        for x in range(row):
                            for y in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                        for x in range(row + 1,3):
                            for y in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                    if(2 < row < 6):
                        for x in range(3,row): 
                            for y in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                        for x in range(row+1,6):
                            for y in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                    if(5 < row):
                        for x in range(6,row): 
                            for y in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
                        for x in range((row + 1),9):
                            for y in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'rowElimination',self)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def colElimination(self):
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
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                        for y in range((col + 1),3):
                            for x in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                    if(2 < col < 6):
                        for y in range(3,col): 
                            for x in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                        for y in range((col + 1),6):
                            for x in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                    if(5 < col):
                        for y in range(6,col):
                            for x in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                        for y in range((col + 1),9):
                            for x in range(3):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                if(np.all(2 < rows) and np.all(rows < 6) and rows.size > 1):
                    if(col < 3):
                        for y in range(0,col): 
                            for x in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                        for y in range((col + 1),3):
                            for x in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                    if(2 < col < 6):
                        for y in range(3,col): 
                            for x in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                        for y in range((col + 1),6):
                            for x in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                    if(5 < col):
                        for y in range(6,col):
                            for x in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                        for y in range((col + 1),9):
                            for x in range(3,6):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                if(np.all(rows > 5)and rows.size > 1):
                    if(col < 3):
                        for y in range(0,col): 
                            for x in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                        for y in range((col + 1),3):
                            for x in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                    if(2 < col < 6):
                        for y in range(3,col): 
                            for x in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                        for y in range((col + 1),6):
                            for x in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                    if(5 < col):
                        for y in range(6,col):
                            for x in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
                        for y in range((col + 1),9):
                            for x in range(6,9):
                                self.cells[x][y].removeOption(unknownarr[u],'colElimination',self)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
        return 'ok'
    def nakedTriple(self):
        for row in range(9):
            cols = []
            counter = 0
            for col in range(9):
                if(self.cells[row][col].options.size == 2):
                    counter += 1
                    cols.append(col)
            colsarr = np.asarray(cols)
            if(counter >= 3):
                for a in range(3,10):
                    for b in range(2,a):
                        for c in range(1,b):
                            abc = np.array([a,b,c])
                            winners = []
                            for i in range(len(colsarr)):
                                if(self.cells[row][colsarr[i]].options.size == 2):
                                    if(self.cells[row][colsarr[i]].options[0] in abc and self.cells[row][colsarr[i]].options[1] in abc):
                                        winners.append(colsarr[i])
                            winarr = np.asarray(winners)
                            if(len(winarr) == 3):
                                for col in range(9):
                                    if(col not in winarr):
                                        self.cells[row][col].removeOption(a,'nakedTriple',self)
                                        self.cells[row][col].removeOption(b,'nakedTriple',self)
                                        self.cells[row][col].removeOption(c,'nakedTriple',self)
        for col in range(9):
            rows = []
            counter = 0
            for row in range(9):
                if(self.cells[row][col].options.size == 2):
                    counter += 1
                    rows.append(row)
            rowsarr = np.asarray(rows)
            if(counter >= 3):
                for a in range(3,10):
                    for b in range(2,a):
                        for c in range(1,b):
                            abc = np.array([a,b,c])
                            winners = []
                            for i in range(len(rowsarr)):
                                if(self.cells[rowsarr[i]][col].options.size == 2):
                                    if(self.cells[rowsarr[i]][col].options[0] in abc and self.cells[rowsarr[i]][col].options[1] in abc):
                                        winners.append(rowsarr[i])
                            winarr = np.asarray(winners)
                            if(len(winarr) == 3):
                                for row in range(9):
                                    if(row not in winarr):
                                        self.cells[row][col].removeOption(a,'nakedTriple',self)
                                        self.cells[row][col].removeOption(b,'nakedTriple',self)
                                        self.cells[row][col].removeOption(c,'nakedTriple',self)
        for x in range(9):                                
            rows = []
            cols = []
            counter = 0
            for col in range(3*(x%3),3*(x%3) + 3):
                for row in range(3*math.floor(x/3),3*math.floor(x/3) + 3):
                    if(self.cells[row][col].options.size == 2):
                        counter += 1
                        rows.append(row)
                        cols.append(col)
            rowsarr = np.asarray(rows)
            colsarr = np.asarray(cols)
            if(counter >= 3):
                for a in range(3,10):
                    for b in range(2,a):
                        for c in range(1,b):
                            abc = np.array([a,b,c])
                            winners = []
                            for i in range(len(rowsarr)):
                                if(self.cells[rowsarr[i]][colsarr[i]].options.size == 2):
                                    if(self.cells[rowsarr[i]][colsarr[i]].options[0] in abc and self.cells[rowsarr[i]][colsarr[i]].options[1] in abc):
                                        winners.append(self.cells[rowsarr[i]][colsarr[i]])
                            winnersarr = np.asarray(winners)
                            if(len(winnersarr) == 3):
                                for col in range(3*(x%3),3*(x%3) + 3):
                                    for row in range(3*math.floor(x/3),3*math.floor(x/3) + 3):
                                        if(self.cells[row][col] not in winnersarr):
                                            self.cells[row][col].removeOption(a,'nakedTriple',self)
                                            self.cells[row][col].removeOption(b,'nakedTriple',self)
                                            self.cells[row][col].removeOption(c,'nakedTriple',self)
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
                    for column in range(col + 1, 9):
                        rowstemp = []
                        for r in range(9):
                            if (value in self.cells[r][column].options):
                                counter = counter + 1
                                rowstemp.append(r)
                        if(rowstemp == rows):
                            for c in range(9):
                                if(c != col and c != column):
                                    self.cells[rowsarr[0]][c].removeOption(unknownarr[u],'x-wing',self)
                                    self.cells[rowsarr[1]][c].removeOption(unknownarr[u],'x-wing',self)
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
                colsarr = np.asarray(cols)
                if(counter == 2):
                    for rowt in range(row + 1, 9):
                        colstemp = []
                        for c in range(9):
                            if (value in self.cells[rowt][c].options):
                                counter = counter + 1
                                colstemp.append(c)
                        if(colstemp == cols):
                            for r in range(9):
                                if(r != row and r != rowt):
                                    self.cells[r][colsarr[0]].removeOption(unknownarr[u],'x-wing',self)
                                    self.cells[r][colsarr[1]].removeOption(unknownarr[u],'x-wing',self)
        for row in range(9):
            for col in range(9):
                if(self.cells[row][col].options.size == 0):
                    return 'error'
    def xywing(self):
        for row in range(9):
            for col in range(9):
                winners = []
                v = 0
                if(self.cells[row][col].options.size == 2):
                    b = self.cells[row][col].options
                    winners.append(b[0])
                    winners.append(b[1])
                    for y in range(9):
                        if(self.cells[row][y].options.size == 2 and y != col):
                            if(b[0] in self.cells[row][y].options or b[1] in self.cells[row][y].options):
                                g = self.cells[row][y].options
                                if(g[0] not in winners):
                                    winners.append(g[0])
                                    v = g[0]
                                if(g[1] not in winners):
                                    winners.append(g[1])
                                    v = g[1]
                            
                                for x in range(9):
                                    if(self.cells[x][col].options.size == 2 and x != row and self.cells[x][col].options[0] in winners and self.cells[x][col].options[1] in winners):
                                        self.cells[x][y].removeOption(v,'xy-wing',self)
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
                self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                error = 0
                k = 0
                while(k < 5):
                    if (self.checkCells() == 'error'):
                        error+=1
                        self.cellsSolved = solved
                        self.cells = copy.deepcopy(cellstor)
                        self.cells[i][j].value = self.cells[i][j].options[1]
                        self.cells[i][j].removeOption(self.cells[i][j].options[0],'guessAndCheck',self)
                        solved += 1
                        k = 20
                    if(error == 0):
                        if (self.checkBoxes() == 'error'):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'guessAndCheck',self)
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.checkColumns() == 'error' and error == 0):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'guessAndCheck',self)
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.checkRows() == 'error' and error == 0):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'guessAndCheck',self)
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.boxElimination() == 'error' and error == 0):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'guessAndCheck',self)
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.colElimination() == 'error' and error == 0):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'guessAndCheck',self)
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.rowElimination() == 'error' and error == 0):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'guessAndCheck',self)
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.checkNakedSets() == 'error' and error == 0):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'guessAndCheck',self)
                            solved += 1
                            k = 20
                    if(error == 0):
                        if (self.nakedTriple() == 'error' and error == 0):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[1]
                            self.cells[i][j].removeOption(self.cells[i][j].options[0],'guessAndCheck',self)
                            solved += 1
                            k = 20
                    k += 1
                if(error > 0):
                    cellstor = copy.deepcopy(self.cells)
                    self.cells[i][j].option = 'guessAndCheck'
                else:
                    self.cells = copy.deepcopy(cellstor)
                    self.cells[i][j].value = self.cells[i][j].options[1]
                    self.cells[i][j].removeOption(self.cells[i][j].options[0], 'guessAndCheck',self)
                    self.cellsSolved = solved
                    k = 0
                    while(k < 5):
                        if (self.checkCells() == 'error'):
                            error+=1
                            self.cellsSolved = solved
                            self.cells = copy.deepcopy(cellstor)
                            self.cells[i][j].value = self.cells[i][j].options[0]
                            self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                            solved += 1
                            k = 20
                        if(error == 0):    
                            if (self.checkBoxes() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.checkColumns() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.checkRows() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.boxElimination() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.colElimination() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.rowElimination() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.checkNakedSets() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                                solved += 1
                                k = 20
                        if(error == 0):
                            if (self.nakedTriple() == 'error' and error == 0):
                                error+=1
                                self.cellsSolved = solved
                                self.cells = copy.deepcopy(cellstor)
                                self.cells[i][j].value = self.cells[i][j].options[0]
                                self.cells[i][j].removeOption(self.cells[i][j].options[1],'guessAndCheck',self)
                                solved += 1
                                k = 20
                        k += 1
                    if(error > 0):
                        cellstor = copy.deepcopy(self.cells)
                        self.cells[i][j].option = 'guessAndCheck'
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
                            if (self.boxElimination() == 'error' and error == 0):
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
                            if (self.colElimination() == 'error' and error == 0):
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
                            if (self.rowElimination() == 'error' and error == 0):
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
                            if (self.checkNakedSets() == 'error' and error == 0):
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
                                if (self.boxElimination() == 'error' and error == 0):
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
                                if (self.colElimination() == 'error' and error == 0):
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
                                if (self.rowElimination() == 'error' and error == 0):
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
                                if (self.checkNakedSets() == 'error' and error == 0):
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
                                            if (self.boxElimination() == 'error' and error == 0):
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
                                            if (self.colElimination() == 'error' and error == 0):
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
                                            if (self.rowElimination() == 'error' and error == 0):
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
                                            if (self.checkNakedSets() == 'error' and error == 0):
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
                                                if (self.boxElimination() == 'error' and error == 0):
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
                                                if (self.colElimination() == 'error' and error == 0):
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
                                                if (self.rowElimination() == 'error' and error == 0):
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
                                                if (self.checkNakedSets() == 'error' and error == 0):
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
def solveSudoku(rows):
    done = 0
    iter = 0
    if (rows[0].size != 9):
        print('error')
        return
    if (rows[:,0].size != 9):
        print('error')
        return
    cells = np.empty((9,9),dtype=object)
    #initialize the grid
    for i in range(9):
        for j in range(9):
            cells[i][j] = Cell(rows[i][j])
    sudoku = sudokuGrid(cells)
    #cycle through sudoku operations
    temp = copy.deepcopy(sudoku)
    i = 0
    while(done == 0 and i < 50):
        sudoku.checkCells()
        sudoku.checkBoxes()
        sudoku.checkColumns()
        sudoku.checkRows()
        sudoku.boxElimination()
        sudoku.colElimination()
        sudoku.rowElimination()
        sudoku.checkNakedSets()
        sudoku.nakedTriple()
        sudoku.xwing()
        sudoku.xywing()
        i+=1
        iter+=1
        #check if all values are filled in
        if (sudoku.checkDone() == True):
            done = 1
        changes = 0
        for col in range(9):
            for row in range(9):
                if(temp.cells[row][col].value != sudoku.cells[row][col].value):
                    changes += 1
        if(changes == 0):
            i = 50
        changes = 0
        temp = copy.deepcopy(sudoku)
    if(done == 0):
        sudoku.guessAndCheck()
        sudoku.guessNakedPairs()
        iter += 10
    if (sudoku.checkDone() == True):
        done = 1
    iteragain = 0
    while(done == 0 and iteragain < 20):
        sudoku.checkCells()
        sudoku.checkBoxes()
        sudoku.checkColumns()
        sudoku.checkRows()
        sudoku.boxElimination()
        sudoku.colElimination()
        sudoku.rowElimination()
        sudoku.checkNakedSets()
        sudoku.nakedTriple()
        sudoku.xwing()
        sudoku.xywing()
        #check if all values are filled in
        if (sudoku.checkDone() == True):
            done = 1
        iteragain+=1
    numbers = np.empty((9,9))
    letters = np.array(['A','B','C', 'D', 'E','F','G','H','I'])
    #prints completed sudoku
    for i in range(9):
        for j in range(9):
            numbers[i][j] = sudoku.cells[i][j].value
            if(sudoku.cells[i][j].method == 'given'):
                print('cell ' + str(letters[i]) + str(j+1) + ' was given')
            else:
                print('cell ' + str(letters[i]) + str(j+1) + ' was solved by ' + sudoku.cells[i][j].method)
    print(numbers)
    if(done == 0):
        print('incomplete')
    else:
        print('Iterations required:')
        print(iter + iteragain)
    return 
# a = input("Enter the sudoku starting with the first row with zeroes for blank spots:")
# rows = np.empty((9,9))
# for i in range(9):
#     for j in range(9):
#         rows[i][j] = a[9*i + j]
# solveSudoku(rows)
    
            
        
        
