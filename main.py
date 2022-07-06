# -*- coding: utf-8 -*-
"""
Created on Mon May 23 20:16:57 2022

@author: bendg
"""

from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import math as math
import copy as copy
import random as random
from sudokusolver import Cell, sudokuGrid
app = Flask(__name__)
app.secret_key = "sudoku"
@app.route("/")
def home():
    return redirect(url_for("solveSudoku"))
@app.route("/puzzles")
def puzzles():
    return render_template("puzzles.html")
@app.route("/puzzles/checkcells/", methods=["GET","POST"])
def checkcellspuzzles():
    c = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        a = random.randint(1,5)
        if "ccpuz" in session:
            if(a == session["ccpuz"]):
                if(a == 1):
                    a += 1
                else:
                    a -= 1
        session["ccpuz"] = a
        if(a == 1):
            numbers = np.array([1,0,2,0,4,0,0,0,0,4,3,0,5,0,9,6,0,0,0,0,7,0,0,0,8,3,4])
            c = "B3"
        if(a == 2):
            numbers = np.array([1,0,2,0,0,0,4,0,7,0,3,0,5,7,9,0,1,0,0,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,5,1,0,0,9,0,0,0,0,7,0,0,0,0,0,1,0,0,8,0,0,0,0,0,7,0,0,0,0,9,2,3,0,0,6,0,0,0,1,0,0,0,0,0,0])
            c = "H1"
        if(a == 3):
            numbers = np.array([9,0,0,5,0,2,0,0,0,0,7,4,8,0,1,3,0,0,2,0,0,6,0,0,0,4,0])
            c = "B5"
        if(a == 4):
            numbers = np.array([4,0,2,8,0,0,0,0,0,0,0,0,0,0,7,0,6,9,0,5,0,0,1,0,0,0,0,0,3,0,0,0,4,6,0,0,0,0,0,1,2,0,0,0,3,0,8,0,5,0,0,0,0,0])
            c = "B2"
        if(a == 5):
            numbers = np.array([0,0,0,4,0,0,0,0,0,0,9,0,0,7,2,0,0,4,0,0,8,0,0,1,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,0,6,0,0,0,0,0,7,0,0,0,0,9,4,5,0,1,0,0,0,0,0,0,0,0,2,0,8,0,3,0,0,0,0,0,0,7,0,0,0,0,1])
            c = "F6"
        return render_template("checkcellspuzzles.html", nums=numbers, lets=letters, result=2, puzzle=a)
    else:
        cell = request.form["cell"]
        if(session["ccpuz"] == 1):
            numbers = np.array([1,0,2,0,4,0,0,0,0,4,3,0,5,0,9,6,0,0,0,0,7,0,0,0,8,3,4])
            c = "B3"
        if(session["ccpuz"] == 2):
            numbers = np.array([1,0,2,0,0,0,4,0,7,0,3,0,5,7,9,0,1,0,0,0,0,0,4,0,0,0,0,0,0,0,1,0,0,0,0,0,5,1,0,0,9,0,0,0,0,7,0,0,0,0,0,1,0,0,8,0,0,0,0,0,7,0,0,0,0,9,2,3,0,0,6,0,0,0,1,0,0,0,0,0,0])
            c = "H1"
        if(session["ccpuz"] == 3):
            numbers = np.array([9,0,0,5,0,2,0,0,0,0,7,4,8,0,1,3,0,0,2,0,0,6,0,0,0,4,0])
            c = "B5"
        if(session["ccpuz"] == 4):
            numbers = np.array([4,0,2,8,0,0,0,0,0,0,0,0,0,0,7,0,6,9,0,5,0,0,1,0,0,0,0,0,3,0,0,0,4,6,0,0,0,0,0,1,2,0,0,0,3,0,8,0,5,0,0,0,0,0])
            c = "B2"
        if(session["ccpuz"] == 5):
            numbers = np.array([0,0,0,4,0,0,0,0,0,0,9,0,0,7,2,0,0,4,0,0,8,0,0,1,0,0,0,0,0,0,5,0,0,0,0,3,0,0,0,0,6,0,0,0,0,0,7,0,0,0,0,9,4,5,0,1,0,0,0,0,0,0,0,0,2,0,8,0,3,0,0,0,0,0,0,7,0,0,0,0,1])
            c = "F6"
        if(cell == c):
            return render_template("checkcellspuzzles.html", nums=numbers, lets=letters, result=True, answer=c, puzzle=session["puz"])
        else:
            return render_template("checkcellspuzzles.html", nums=numbers, lets=letters, result=False, answer=c, puzzle=session["puz"])
@app.route("/puzzles/checkboxes/", methods=["GET","POST"])
def checkboxespuzzles():
    c = ""
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(request.method == "GET"):
        a = random.randint(1,3)
        if "cbpuz" in session:
            if(a == session["cbpuz"]):
                if(a == 1):
                    a += 1
                else:
                    a -= 1
        session["cbpuz"] = a
        if(a == 1):
            numbers = np.array([7,0,0,0,0,0,1,0,0,2,0,5,0,6,7,0,0,3,0,4,0,1,0,0,0,8,0])
            c = "B2"
        if(a == 2):
            numbers = np.array([0,0,0,0,0,0,2,0,0,5,4,0,0,6,0,0,9,0,0,0,0,7,0,3,0,0,0,0,9,3,0,0,0,0,0,0,0,1,0,6,0,7,0,0,0,0,2,0,0,0,0,0,0,3,0,0,0,0,2,0,0,5,0,9,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,1])
            c = "E5"
        if(a == 3):
            numbers = np.array([0,0,0,6,7,2,0,1,0,7,0,2,0,0,9,0,0,0,0,5,0,0,1,0,4,7,0])
            c = "B2"
        return render_template("checkboxespuzzles.html", nums=numbers, lets=letters, result=2, puzzle=a)
    else:
        cell = request.form["cell"]
        if(session["cbpuz"] == 1):
            numbers = np.array([7,0,0,0,0,0,1,0,0,2,0,5,0,6,7,0,0,3,0,4,0,1,0,0,0,8,0])
            c = "B2"
        if(session["cbpuz"] == 2):
            numbers = np.array([0,0,0,0,0,0,2,0,0,5,4,0,0,6,0,0,9,0,0,0,0,7,0,3,0,0,0,0,9,3,0,0,0,0,0,0,0,1,0,6,0,7,0,0,0,0,2,0,0,0,0,0,0,3,0,0,0,0,2,0,0,5,0,9,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,1])
            c = "E5"
        if(session["cbpuz"] == 3):
            numbers = np.array([0,0,0,6,7,2,0,1,0,7,0,2,0,0,9,0,0,0,0,5,0,0,1,0,4,7,0])
            c = "B2"
        if(cell == c):
            return render_template("checkboxespuzzles.html", nums=numbers, lets=letters, result=True, answer=c, puzzle=session["cbpuz"])
        else:
            return render_template("checkboxespuzzles.html", nums=numbers, lets=letters, result=False, answer=c, puzzle=session["cbpuz"])
@app.route("/puzzles/checkrows/")
def checkrowspuzzles():
    return render_template("puzzles.html")
@app.route("/puzzles/checkcols/")
def checkcolumnspuzzles():
    return render_template("puzzles.html")
@app.route("/puzzles/nakedsets")
def nakedsetspuzzles():
    return render_template("puzzles.html")
@app.route("/puzzles/boxelimination")
def boxeliminationpuzzles():
    return render_template("puzzles.html")
@app.route("/puzzles/colelimination")
def coleliminationpuzzles():
    return render_template("puzzles.html")
@app.route("/puzzles/rowelimination")
def roweliminationpuzzles():
    return render_template("puzzles.html")
@app.route("/puzzles/nakedtriples")
def nakedtriplepuzzles():
    return render_template("puzzles.html")
@app.route("/puzzles/xwing")
def xwingpuzzles():
    return render_template("puzzles.html")
@app.route("/puzzles/xywing")
def xywingpuzzles():
    return render_template("puzzles.html")
@app.route("/methods")
def methods():
    return render_template("methods.html")
@app.route("/methods/checkcells")
def methodscheckcells():
    return render_template("methods.html")
@app.route("/sudoku", methods=["GET","POST"])
def buildSudoku():
    if request.method == "GET":
        return render_template("sudokuform.html")
    else:
        if("sudoku" in session):
            session.pop("sudoku",None)
            session.pop("solution",None)
            session.pop("methods",None)
            session.pop("numberOfSteps",None)
            session.pop("stepsDisplayed",None)
            session.pop("givens", None)
            session.pop("bluenums", None)
        row1 = request.form["row1"]
        row2 = request.form["row2"]
        row3 = request.form["row3"]
        row4 = request.form["row4"]
        row5 = request.form["row5"]
        row6 = request.form["row6"]
        row7 = request.form["row7"]
        row8 = request.form["row8"]
        row9 = request.form["row9"]
        if (len(row1) != 9):
            return 'Row 1 has an error. Press the back button to correct it.'
        if (len(row2) != 9):
            return 'Row 2 has an error. Press the back button to correct it.'
        if (len(row3) != 9):
            return 'Row 3 has an error. Press the back button to correct it.'
        if (len(row4) != 9):
            return 'Row 4 has an error. Press the back button to correct it.'
        if (len(row5) != 9):
            return 'Row 5 has an error. Press the back button to correct it.'
        if (len(row6) != 9):
            return 'Row 6 has an error. Press the back button to correct it.'
        if (len(row7) != 9):
            return 'Row 7 has an error. Press the back button to correct it.'
        if (len(row8) != 9):
            return 'Row 8 has an error. Press the back button to correct it.'
        if (len(row9) != 9):
            return 'Row 9 has an error. Press the back button to correct it.'
        rows = np.empty((9,9))
        for j in range(9):
            rows[0][j] = row1[j]
            rows[1][j] = row2[j]
            rows[2][j] = row3[j]
            rows[3][j] = row4[j]
            rows[4][j] = row5[j]
            rows[5][j] = row6[j]
            rows[6][j] = row7[j]
            rows[7][j] = row8[j]
            rows[8][j] = row9[j]
        letters = np.array(['A','B','C','D','E','F','G','H','I'])
        #initialize the grid
        done = 0
        iter = 0
        session["givens"] = 0
        session["bluenums"] = ""
        init = ""
        cells = np.empty((9,9),dtype=object)
        for i in range(9):
            for j in range(9):
                if(rows[i][j] != 0):
                    session["givens"] += 1
                cells[i][j] = Cell(rows[i][j])
                init = init + str(int(rows[i][j]))
        session["sudoku"] = init
        sudoku = sudokuGrid(cells)      
        temp = copy.deepcopy(sudoku)
        #cycle through sudoku operations
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
            iter += 2
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
        totaliter = iter + iteragain
        answer = ""
        listOfMethods = ""
        listOfOrders = ""
        #prints completed sudoku
        k = 0
        for i in range(9):
                for j in range(9):
                    answer = answer + str(int(sudoku.cells[i][j].value))
                    listOfOrders = listOfOrders + str(int(sudoku.cells[i][j].order)) + ","
        while(k <= sudoku.cellsSolved):
            for i in range(9):
                for j in range(9):
                    if(sudoku.cells[i][j].order == k):
                        if(sudoku.cells[i][j].method == 'given'):
                            listOfMethods = listOfMethods + 'cell ' + str(letters[i]) + str(j+1) + ' was given,'
                        else:
                            listOfMethods = listOfMethods + 'cell ' + str(letters[i]) + str(j+1) + ' was solved by ' + sudoku.cells[i][j].method + ","
            k += 1
        session["solution"] = answer
        session["methods"] = listOfMethods
        session["orders"] = listOfOrders
        session["numOfSteps"] = sudoku.cellsSolved
        session["stepsDisplayed"] = 0
        if(done == 0):
            return render_template("incomplete.html")
        else:
            return render_template("sudoku formatting.html", nums=init, methods=[], lets=letters, steps=0, blue = [])
@app.route("/sudoku/solve", methods=["GET","POST"])
def solveSudoku():
    if not "sudoku" in session:
        return redirect(url_for("buildSudoku"))
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    m = session["methods"]
    b = session["orders"]
    listOfOrders = []
    listOfMethods = []
    listOfBluenums = []
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
    for x in range(len(session["bluenums"])):
        if(session["bluenums"][x] == ","):
            listOfBluenums.append(int(session["bluenums"][a:x]))
            a = x+1
    return render_template("sudoku formatting.html", nums=session["solution"], methods=listOfMethods,lets=letters,steps=81,blue=listOfBluenums)
@app.route("/sudoku/onestep", methods=["GET","POST"])
def onestep():
    if not "sudoku" in session:
        return redirect(url_for("buildSudoku"))
    letters = np.array(['A','B','C','D','E','F','G','H','I'])
    if(session["stepsDisplayed"] < session["numOfSteps"]):
        session["stepsDisplayed"] += 1
    b = session["orders"]
    m = session["methods"]
    listOfMethods = []
    listOfOrders = []
    listOfBluenums = []
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
        if(int(listOfOrders[p]) == session["stepsDisplayed"]):
            session["sudoku"] = session["sudoku"][0:p] + session["solution"][p] + session["sudoku"][p+1:81]
            session["bluenums"] = session["bluenums"] + str(p) + ","
            num = p
    a = 0
    for x in range(len(session["bluenums"])):
        if(session["bluenums"][x] == ","):
            listOfBluenums.append(int(session["bluenums"][a:x]))
            a = x+1
    return render_template("sudoku formatting.html", nums=session["sudoku"], lets=letters, methods=np.array([listOfMethods[session["givens"] - 1 + session["stepsDisplayed"]]]), steps=1, blue=listOfBluenums)
@app.route("/sudoku/clear", methods=["GET", "POST"])
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
    for x in range(len(session["sudoku"])):
        if x in listOfBluenums:
            session["sudoku"] = session["sudoku"][0:x] + "0" + session["sudoku"][x+1:81]
    session["bluenums"] = ""
    session["stepsDisplayed"] = 0
    return render_template("sudoku formatting.html",nums=session["sudoku"], methods = [], lets=letters, steps=0, blue=[])
if(__name__ == "__main__"):
    app.run()
