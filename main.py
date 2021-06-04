# COMP472 - Assignment 1
# Programmed By:
# Constantine Karellas - 40109253
# Max Burah - 40077075

import math
import string
import numpy as np
import random
from queue import PriorityQueue

from numpy.core.fromnumeric import size


# class for grid element

class GridElement:
    def __init__(self, number, locationType, nodes, neighbours, neighbourLocations, cost, heuristic):
        self.number = number
        self.locationType = locationType
        self.nodes = nodes
        self.neighbours = neighbours
        self.neighbours = neighbourLocations
        self.cost = cost
        self.heuristic = heuristic

    def printElement(self):
        print("Cell Number:" + str(self.number) + "\n" +
              "Location Type:" + self.locationType + "\n" +
              "Nodes:" + str(self.nodes) + "\n" +
              "Cell Neighbours:" + str(self.neighbours) + "\n" +
              "Edge Costs:" + str(self.cost) + "\n" +
              "Heuristic Amount:" + str(self.heuristic))

    def getNumber(self):
        return str(self.number)

    def getLocationType(self):
        return self.locationType


class Node:
    def __init__(self, number, letter, neighbours, moveCost, heuristicCost, algorithmCost):
        self.number = number
        self.letter = letter
        self.neighbours = neighbours  # left,up,right,down
        self.moveCost = moveCost  # left,up,right,down
        self.heuristicCost = heuristicCost  # left,up,right,down
        self.algorithmCost = algorithmCost  # left,up,right,down

    def printElement(self):
        print("Node Number:" + str(self.number) + "\n" +
              "Node Letter:" + str(self.letter) + "\n" +
              "Neighbours:" + str(self.neighbours) + "\n" +
              "Edge Costs:" + str(self.moveCost) + "\n" +
              "Heuristic Costs:" + str(self.heuristicCost) + "\n"
              + "Algorithm Costs:" + str(self.moveCost))


def createGridElement(number):
    locationChoices = ["Q", "V", "P", "E"]
    # Q for quarantine, V for vaccine, P for playground, E for empty
    locationType = random.choice(locationChoices)  # chooses random location type
    element = GridElement(number, locationType, [], [], [], [], "0")
    return element


print("\n======================================================================")
#############   STEP 1 -- User inputs to make map
print("Program Begins:")
userRows = int(input("\nEnter amount of Rows? "))
userColumns = int(input("Enter amount of Columns? "))

# print("========================================================================")
#############   STEP 2 -- List all items in list with theyre appropriate edges
# print("Information of each cell:\n")
gridSize = userRows * userColumns
l = 0
k = 4
gridList = []
for i in range(1, gridSize + 1):  # iterate over all items in grid
    e = createGridElement(i)
    gridList.append(e)
    '''
    e.printElement()
    print("_________________________")
    '''

print("=========================================================================")
#############   STEP 3 -- Visual of map locations
print("Generated Map:\n")
genMap = []
for i in range(0, len(gridList)):
    if gridList[i].locationType == "E":
        genMap.append(gridList[i].number)
    else:
        genMap.append(gridList[i].locationType)
########### Create edges for each grid element
for i in range(0, len(gridList)):
    if gridList[i].locationType == "E":
        genMap.append(gridList[i].number)
    else:
        genMap.append(gridList[i].locationType)

letterList = (list(string.ascii_letters))  # list of alphabetical edges (lowercase then uppercase)

rc = 0
for i in range(0, len(gridList)):
    if gridList[i].number % userColumns == 1 and gridList[i].number != 1:
        gridList[i].nodes = [letterList[rc + 1], letterList[rc + 2], letterList[rc + userColumns + 3],
                             letterList[rc + userColumns + 2]]
        rc += 2
    else:
        gridList[i].nodes = [letterList[rc], letterList[rc + 1], letterList[rc + userColumns + 2],
                             letterList[rc + userColumns + 1]]
        rc += 1

counter = 0
for j in range(0, len(gridList)):
    print("| ", genMap[j], " |", end='')
    counter += 1
    if counter == userColumns:
        print(" ")
        counter = 0
'''
nodeAmount = (userColumns * userRows) + (userColumns + userRows + 1)

def createNodeElement(number):
    nodeElement = Node(number, letterList[number], [], [], [], [])
    return nodeElement


nodeList = []
for m in range(0, nodeAmount):
    n = createNodeElement(m)
    nodeList.append(n)

# find neighboring nodes
for i in range(len(nodeList)):
    nodeList[i].moveCost = [0, 0, 0, 0]
    nodeList[i].heuristicCost = [0, 0, 0, 0]
    nodeList[i].algorithmCost = [0, 0, 0, 0]
    if nodeList[i].number == 0:
        nodeList[i].neighbours = [-1, -1, letterList[i + 1], letterList[i + userColumns + 1]]
    elif nodeList[i].number == nodeAmount - 1:
        nodeList[i].neighbours = [letterList[i - 1], letterList[i - userColumns - 1],
                                  -1, -1]
    elif nodeList[i].number > nodeAmount - userColumns:
        nodeList[i].neighbours = [letterList[i - 1], letterList[i - userColumns - 1],
                                  letterList[i + 1], -1]
    else:
        nodeList[i].neighbours = [letterList[i - 1], letterList[i - userColumns - 1],
                                  letterList[i + 1], letterList[i + userColumns + 1]]
for i in range(0, len(nodeList)):
    # check if there are no left neighbours
    if nodeList[i].number % (userColumns + 1) == 0:
        nodeList[i].neighbours[0] = -1
        nodeList[i].moveCost[0] = -1
        nodeList[i].heuristicCost[0] = -1
        nodeList[i].algorithmCost[0] = -1
    # check if there are no upper neighbours
    if nodeList[i].number <= userColumns:
        nodeList[i].neighbours[1] = -1
        nodeList[i].moveCost[1] = -1
        nodeList[i].heuristicCost[1] = -1
        nodeList[i].algorithmCost[1] = -1
    # check if there are no right neighbours
    if nodeList[i].number % (userColumns + 1) == 4:
        nodeList[i].neighbours[2] = -1
        nodeList[i].moveCost[2] = -1
        nodeList[i].heuristicCost[2] = -1
        nodeList[i].algorithmCost[2] = -1
    # check if there are no bottom neighbours
    if nodeList[i].number >= nodeAmount - userColumns - 1:
        nodeList[i].neighbours[3] = -1
        nodeList[i].moveCost[3] = -1
        nodeList[i].heuristicCost[3] = -1
        nodeList[i].algorithmCost[3] = -1
'''

print("\n=======================================================================")
#############   STEP 4 --  User choosing the Role C or Role V and inputs start state
print("Role C (Covid Patients)\nRole P (Children Getting Vaccinated)\n")
role = (input("Choose the Role C or the Role P by entering C or P: "))

cellWidth = 0.1
cellLength = 0.2

gridWidth = cellWidth * userColumns
gridLength = cellLength * userRows

# For role C
if role == 'c' or role == 'C':
    exists = 'Q' in genMap
    if(exists ==  False):
        print("\nNo path found because there in so Q in map.\nRun program again.\n")
        exit()
    # user input for x and y
    startCellxInput = float(input("\nEnter an x coordinate as the starting point/state (Choose between 0 and " + str(
        round(gridWidth, 2)) + "): "))
    if startCellxInput > userColumns*0.1 or startCellxInput < 0:
        startCellxInput = float(input("Out of Range - Enter a number between 0 and " + str(round(gridWidth, 2)) + ": "))
            
    startCellyInput = float(input("Enter a y coordinate as the starting point/state (Choose between 0 and " + str(round(gridLength, 2)) + "): "))
    if startCellyInput > userRows*0.2 or startCellyInput < 0:
        startCellyInput = float(input("Out of Range - Enter a number between 0 and " + str(round(gridWidth, 2)) + ": "))
   
    # finding the row and column obased on the user input
    startRow = (math.floor(startCellyInput / cellLength)) + 1
    print("Start state is in row: " + str(startRow))
    startColumn = (math.floor(startCellxInput / cellWidth)) + 1
    print("Start state is in column: " + str(startColumn))

    # finding the start cell number based on the row and column
    startCell = ((startRow - 1) * userColumns) + startColumn
    print("Start State Cell Number: " + str(startCell))

    startX = round((startColumn * 0.1), 2)
    startY = round(((startRow - 1) * 0.2), 2)

    print("Start Cell Coordinates: " + str(startX) + "," + str(startY))

    goalStateList = []
    goalXList = []
    goalYList = []
    distanceList = []
    for j in range(0, len(gridList)):
        if "Q" in gridList[j].locationType:
            goalStateList.append(gridList[j].number)

    for i in range(0, len(goalStateList)):
        goalStateRow = math.ceil(goalStateList[i] / userRows)
        goalStateColumn = goalStateList[i] % userColumns
        if goalStateColumn == 0:
            goalStateColumn = userColumns
        goalYList.append((goalStateRow - 1) * 0.2)
        goalXList.append(goalStateColumn * 0.1)

    for i in range(0, len(goalStateList)):
        distanceList.append(
            math.sqrt((abs((goalXList[i] - startX)) ** 2) + (abs((goalYList[i] - startY)) ** 2)))

    for p in range(0, len(distanceList)):
        goalDistanceIndex = distanceList.index(min(distanceList))

    goalState = goalStateList[goalDistanceIndex]
    print("Goal State Cell Number: " + str(goalState))
    goalStateX = goalXList[goalDistanceIndex]
    goalStateY = goalYList[goalDistanceIndex]

    print("Goal Cell Coordinates: " + str(goalStateX) + "," + str(goalStateY))

    print("\nStarting State: ", genMap[startCell - 1], "(Cell: ", startCell, ")   ------->  Goal State: Q ", "(Cell: ",
          goalState, ")")

# For role P
if role == 'p' or role == 'P':
    exists = 'P' in genMap
    if(exists ==  False):
        print("\nNo path found because there in so P in map.\nRun program again.\n")
        exit()
    # user input for x and y
    startCellxInput = float(input("\nEnter an x coordinate as the starting point/state (Choose between 0 and " + str(
        round(gridWidth, 2)) + "): "))
    if startCellxInput > userColumns*0.1:
        startCellxInput = float(input("Out of Range - Enter a number between 0 and " + str(round(gridWidth, 2)) + ": "))
    startCellyInput = float(input(
        "Enter a y coordinate as the starting point/state (Choose between 0 and " + str(round(gridLength, 2)) + "): "))
    if startCellyInput > userRows*0.2:
        startCellyInput = float(input("Out of Range - Enter a number between 0 and " + str(round(gridWidth, 2)) + ": "))

    # finding the row and column obased on the user input
    startRow = (math.floor(startCellyInput / cellLength)) + 1
    print("Start state is in row: " + str(startRow))
    startColumn = (math.floor(startCellxInput / cellWidth)) + 1
    print("Start state is in column: " + str(startColumn))

    # finding the start cell number based on the row and column
    startCell = ((startRow - 1) * userColumns) + startColumn
    print("Start State Cell Number: " + str(startCell))

    startX = startCellxInput
    startY = startCellyInput

    print("Start Cell Coordinates: " + str(startX) + "," + str(startY))

    goalStateList = []
    goalXList = []
    goalYList = []
    distanceList = []
    for j in range(0, len(gridList)):
        if "P" in gridList[j].locationType:
            goalStateList.append(gridList[j].number)

    for i in range(0, len(goalStateList)):
        goalStateRow = math.ceil(goalStateList[i] / userRows)
        goalStateColumn = goalStateList[i] % userColumns
        if goalStateColumn == 0:
            goalStateColumn = userColumns
        goalYList.append((goalStateRow * 0.2))
        goalXList.append(((goalStateColumn - 1) * 0.1))

    for i in range(0, len(goalStateList)):
        distanceList.append(
            math.sqrt((abs((goalXList[i] - startX)) ** 2) + (abs((goalYList[i] - startY)) ** 2)))

    for p in range(0, len(distanceList)):
        goalDistanceIndex = distanceList.index(min(distanceList))

    goalState = goalStateList[goalDistanceIndex]
    print("Goal State Cell Number: " + str(goalState))
    goalStateX = goalXList[goalDistanceIndex]
    goalStateY = goalYList[goalDistanceIndex]

    print("\nStarting State: ", genMap[startCell - 1], "(Cell: ", startCell, ")   ------->  Goal State: P ", "(Cell: ",
          goalState, ")")

#############   STEP 5 -- Cost

# find neighbours numbers for each gridElement
for i in range(0, len(gridList)):
    try:
        if gridList[i].number == gridSize:
            gridList[i].neighbours = [gridList[i - 1].number, gridList[i - userColumns].number,
                                      "0", "0"]
        elif gridList[i].number > gridSize - userColumns:
            gridList[i].neighbours = [gridList[i - 1].number, gridList[i - userColumns].number,
                                      gridList[i + 1].number, "0"]
        else:
            gridList[i].neighbours = [gridList[i - 1].number, gridList[i - userColumns].number,
                                      gridList[i + 1].number, gridList[i + userColumns].number]
    except IndexError:
        print("No neighbour for element: " + str(gridList[i].number))

for i in range(0, len(gridList)):
    # check if there are no left neighbours
    if gridList[i].number % userColumns == 1:
        gridList[i].neighbours[0] = -1
    # check if there are no upper neighbours
    if gridList[i].number <= userColumns:
        gridList[i].neighbours[1] = -1
    # check if there are no right neighbours
    if gridList[i].number % userColumns == 0:
        gridList[i].neighbours[2] = -1
    # check if there are no bottom neighbours
    if gridList[i].number > gridSize - userColumns:
        gridList[i].neighbours[3] = -1

    # gridList[i].printElement()

# find neighbour locations for each gridElement
for i in range(0, len(gridList)):
    try:
        if gridList[i].number == gridSize:
            gridList[i].neighbourLocations = [gridList[i - 1].locationType, gridList[i - userColumns].locationType,
                                              "0", "0"]
        elif gridList[i].number > gridSize - userColumns:
            gridList[i].neighbourLocations = [gridList[i - 1].locationType, gridList[i - userColumns].locationType,
                                              gridList[i + 1].locationType, "0"]
        else:
            gridList[i].neighbourLocations = [gridList[i - 1].locationType, gridList[i - userColumns].locationType,
                                              gridList[i + 1].locationType, gridList[i + userColumns].locationType]
    except IndexError:
        print("No neighbour for element: " + str(gridList[i].number))

for i in range(0, len(gridList)):
    # check if there are no left neighbours
    if gridList[i].number % userColumns == 1:
        gridList[i].neighbourLocations[0] = "0"
    # check if there are no upper neighbours
    if gridList[i].number <= userColumns:
        gridList[i].neighbourLocations[1] = "0"
    # check if there are no right neighbours
    if gridList[i].number % userColumns == 0:
        gridList[i].neighbourLocations[2] = "0"
    # check if there are no bottom neighbours
    if gridList[i].number > gridSize - userColumns:
        gridList[i].neighbourLocations[3] = "0"

# find cost for each grid Element dependent on what role is chosen
# fill cost list with -1s as default
for i in range(0, len(gridList)):
    gridList[i].cost = [-1, -1, -1, -1]
# for role c: cost = (left,top,right,bottom)
for i in range(0, len(gridList)):
    # if there are no neighbours on the left
    if gridList[i].neighbourLocations[0] == "0":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = 0
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = 3
    # if there are no neighbours on the top
    if gridList[i].neighbourLocations[1] == "0":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = 0
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = 3
    # if there are no neighbours on the right
    if gridList[i].neighbourLocations[2] == "0":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = 0
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = 3
    # if there are no neighbours on the bottom
    if gridList[i].neighbourLocations[3] == "0":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = 0
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = 3
    # if there is a neighbour that is a quarantine place
    if gridList[i].neighbourLocations[0] == "Q":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = 0
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = 0.5
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = 1
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = 1.5
    if gridList[i].neighbourLocations[1] == "Q":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = 0
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = 0.5
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = 1
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = 1.5
    if gridList[i].neighbourLocations[2] == "Q":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = 0
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = 0.5
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = 1
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = 1.5
    if gridList[i].neighbourLocations[3] == "Q":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = 0
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = 0.5
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = 1
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = 1.5

    ############## if there is a neighbour that is a vaccine place
    if gridList[i].neighbourLocations[0] == "V":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = 1
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = 1.5
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = 2.5
    if gridList[i].neighbourLocations[1] == "V":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = 1
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = 1.5
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = 2.5
    if gridList[i].neighbourLocations[2] == "V":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = 1
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = 1.5
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = 2.5
    if gridList[i].neighbourLocations[3] == "V":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = 1
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = 1.5
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = 2.5

    ############## if there is a neighbour that is a playground
    if gridList[i].neighbourLocations[0] == "P":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = 1.5
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = 2
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = 2.5
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = 3
    if gridList[i].neighbourLocations[1] == "P":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = 1.5
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = 2
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = 2.5
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = 3
    if gridList[i].neighbourLocations[2] == "P":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = 1.5
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = 2
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = 2.5
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = 3
    if gridList[i].neighbourLocations[3] == "P":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = 1.5
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = 2
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = 2.5
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = 3

        ############## if there is a neighbour that is EMPTY
    if gridList[i].neighbourLocations[0] == "E":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = 0.5
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = 1.5
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = 2
    if gridList[i].neighbourLocations[1] == "E":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = 0.5
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = 1.5
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = 2
    if gridList[i].neighbourLocations[2] == "E":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = 0.5
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = 1.5
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = 2
    if gridList[i].neighbourLocations[3] == "E":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = 0.5
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = 1.5
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = 2

'''
for i in range(len(nodeList)):
    if i <= userColumns:
        nodeList[i].moveCost = [gridList[i-1].cost[1], gridList[i - 1].cost[2], gridList[i].cost[1], gridList[i].cost[0]]
    if userColumns < i <= userColumns*2:
        nodeList[i].moveCost = [gridList[i - 2].cost[1], gridList[i - 2].cost[2], gridList[i-1].cost[1],
                                gridList[i-1].cost[0]]
    if userColumns*2 < i <= userColumns*3:
        nodeList[i].moveCost = [gridList[i - 3].cost[1], gridList[i - 3].cost[2], gridList[i-2].cost[1],
                                gridList[i-2].cost[0]]
'''

print("\n=========================================================================")

#############   STEP 6 -- Heuristic and A* Algorithms for Optimal Path
for l in range(0, len(gridList)):
    gridList[l].heuristic = [-1, -1, -1, -1]  # left,top,right,bottom
for i in range(0, len(gridList)):
    # get row and column for current gridList element
    currentRow = math.ceil(gridList[i].number / userRows)
    currentColumn = gridList[i].number % userColumns
    if currentColumn == 0:
        currentColumn = userColumns
    # get x and y coordinate for current element
    topRightX = round((currentColumn * 0.1), 2)
    topRightY = round(((currentRow - 1) * 0.2), 2)

    topLeftX = round(((currentColumn - 1) * 0.1), 2)
    topLeftY = topRightY

    bottomRightX = topRightX
    bottomRightY = round((currentRow * 0.2), 2)

    bottomLeftX = topLeftX
    bottomLeftY = bottomRightY

    # get distance to goal state
    topRightDistance = math.sqrt((abs((goalStateX - topRightX)) ** 2) + (abs((goalStateY - topRightY)) ** 2))
    topLeftDistance = math.sqrt((abs((goalStateX - topLeftX)) ** 2) + (abs((goalStateY - topLeftY)) ** 2))
    bottomRightDistance = math.sqrt((abs((goalStateX - bottomRightX)) ** 2) + (abs((goalStateY - bottomRightY)) ** 2))
    bottomLeftDistance = math.sqrt((abs((goalStateX - bottomLeftX)) ** 2) + (abs((goalStateY - bottomLeftY)) ** 2))
    '''
    print("TopLeft: " + str(topLeftDistance) +"TopRight: " + str(topRightDistance) + ",BottomRight: " + str(
        bottomRightDistance) + ",BottomLeft: " + str(bottomLeftDistance) + " for number: " + str(gridList[i].number))
    '''
    # rate Distances for heuristic
    heuristicDistanceList = [topLeftDistance, topRightDistance, bottomRightDistance,
                             bottomLeftDistance]  # topleft,topright,bottomright,bottomleft
    hAmount = 0
    for p in range(0, len(heuristicDistanceList)):
        heuristicIndex = heuristicDistanceList.index(min(heuristicDistanceList))
        heuristicDistanceList[heuristicIndex] = 100
        gridList[i].heuristic[heuristicIndex] = hAmount
        hAmount += 1

    # gridList[i].printElement()

openList = []
closedList = []
visitedState = []

optimalPath = []

startingNode = gridList[startCell - 1].nodes[1]
currentNumber = startCell - 1
currentNode = startingNode

for i in range(len(gridList)):
    gridList[i].printElement()


def traverseGrid(currentGridNumber, nextNode):
    visitedState.append(nextNode)
    currentNodeList = []
    for k in range(0, 4):
        currentNodeList.append(gridList[currentGridNumber].nodes[k])
    print("current node list: " + str(currentNodeList))
    currentNodeIndex = currentNodeList.index(nextNode)
    print("CurrentNodeIndex: " + str(currentNodeIndex))
    nodeListIndex = letterList.index(nextNode)

    # if the current node is on the top left, takes from left and top neighbour
    # left movement cost comes from left neighbour, top movement cost comes from top neighbour
    if currentNodeIndex == 0:
        if gridList[currentGridNumber].neighbours[0] == -1:
            leftCost = 10
            leftHeuristic = 10
            nodeLeft = ""
            nodeLeftElement = ""
        else:
            leftCost = gridList[(gridList[currentGridNumber].neighbours[0]) - 1].cost[1]
            leftHeuristic = gridList[(gridList[currentGridNumber].neighbours[0]) - 1].heuristic[0]
            nodeLeft = letterList[nodeListIndex - 1]
            nodeLeftElement = gridList[(gridList[currentGridNumber].neighbours[0]) - 1].number
        if gridList[currentGridNumber].neighbours[1] == -1:
            upCost = 10
            upHeuristic = 10
            nodeUp = ""
            nodeUpElement = ""
        else:
            upCost = gridList[(gridList[currentGridNumber].neighbours[1]) - 1].cost[0]
            upHeuristic = gridList[(gridList[currentGridNumber].neighbours[1]) - 1].heuristic[0]
            nodeUp = letterList[nodeListIndex - (userColumns + 1)]
            nodeUpElement = gridList[(gridList[currentGridNumber].neighbours[1]) - 1].number
        rightCost = gridList[currentGridNumber].cost[1]
        rightHeuristic = gridList[currentGridNumber].heuristic[1]
        nodeRight = letterList[nodeListIndex + 1]
        nodeRightElement = gridList[currentGridNumber].number
        downCost = gridList[currentGridNumber].cost[0]
        downHeuristic = gridList[currentGridNumber].heuristic[3]
        nodeDown = letterList[nodeListIndex + (userColumns + 1)]
        nodeDownElement = gridList[currentGridNumber].number
        moveCost = [leftCost, upCost, rightCost, downCost]  # to move left,up,right,down
        heuristicCost = [leftHeuristic, upHeuristic, rightHeuristic, downHeuristic]

        algorithmCost = [leftCost + leftHeuristic, upCost + upHeuristic, rightCost + rightHeuristic,
                         downCost + downHeuristic]
        nextElement = [nodeLeftElement, nodeUpElement, nodeRightElement, nodeDownElement]

    ##if current node is at top right
    if currentNodeIndex == 1:
        ##no right neighboour,set cost very high
        if gridList[currentGridNumber].neighbours[2] == -1:
            rightCost = 10
            rightHeuristic = 10
            nodeRight = ""
            nodeRightElement = ""
        else:
            rightCost = gridList[(gridList[currentGridNumber].neighbours[2]) - 1].cost[1]
            rightHeuristic = gridList[(gridList[currentGridNumber].neighbours[2]) - 1].heuristic[1]
            nodeRight = letterList[nodeListIndex + 1]
            nodeRightElement = gridList[(gridList[currentGridNumber].neighbours[2]) - 1].number
        if gridList[currentGridNumber].neighbours[1] == -1:
            upCost = 10
            upHeuristic = 10
            nodeUp = ""
            nodeUpElement = ''
        else:
            upCost = gridList[(gridList[currentGridNumber].neighbours[1]) - 1].cost[2]
            upHeuristic = gridList[(gridList[currentGridNumber].neighbours[1]) - 1].heuristic[1]
            nodeUp = letterList[nodeListIndex - (userColumns + 1)]
            nodeUpElement = gridList[(gridList[currentGridNumber].neighbours[1]) - 1].number
        leftCost = gridList[currentGridNumber].cost[1]
        leftHeuristic = gridList[currentGridNumber].heuristic[0]
        nodeLeft = letterList[nodeListIndex - 1]
        nodeLeftElement = gridList[currentGridNumber].number
        downCost = gridList[currentGridNumber].cost[2]
        downHeuristic = gridList[currentGridNumber].heuristic[2]
        nodeDown = letterList[nodeListIndex + (userColumns + 1)]
        nodeDownElement = gridList[currentGridNumber].number
        moveCost = [leftCost, upCost, rightCost, downCost]  # to move left,up,right,down
        heuristicCost = [leftHeuristic, upHeuristic, rightHeuristic, downHeuristic]

        algorithmCost = [leftCost + leftHeuristic, upCost + upHeuristic, rightCost + rightHeuristic,
                         downCost + downHeuristic]
        nextElement = [nodeLeftElement, nodeUpElement, nodeRightElement, nodeDownElement]

    ##if current node is at bottom right
    if currentNodeIndex == 2:
        if gridList[currentGridNumber].neighbours[2] == -1:
            rightCost = 10
            rightHeuristic = 10
            nodeRight = ""
            nodeRightElement = ''
        else:
            rightCost = gridList[(gridList[currentGridNumber].neighbours[2]) - 1].cost[3]
            rightHeuristic = gridList[(gridList[currentGridNumber].neighbours[2]) - 1].heuristic[2]
            nodeRight = letterList[nodeListIndex + 1]
            nodeRightElement = gridList[(gridList[currentGridNumber].neighbours[2]) - 1].number
        if gridList[currentGridNumber].neighbours[3] == -1:
            downCost = 10
            downHeuristic = 10
            nodeDown = ""
            nodeDownElement = ""
        else:
            downCost = gridList[(gridList[currentGridNumber].neighbours[3]) - 1].cost[2]
            downHeuristic = gridList[(gridList[currentGridNumber].neighbours[3]) - 1].heuristic[2]
            nodeDown = letterList[nodeListIndex + (userColumns + 1)]
            nodeDownElement = gridList[(gridList[currentGridNumber].neighbours[3]) - 1].number
        leftCost = gridList[currentGridNumber].cost[3]
        leftHeuristic = gridList[currentGridNumber].heuristic[3]
        nodeLeft = letterList[nodeListIndex - 1]
        nodeLeftElement = gridList[currentGridNumber].number
        upCost = gridList[currentGridNumber].cost[2]
        upHeuristic = gridList[currentGridNumber].heuristic[1]
        nodeUp = letterList[nodeListIndex - (userColumns + 1)]
        nodeUpElement = gridList[currentGridNumber].number
        moveCost = [leftCost, upCost, rightCost, downCost]
        heuristicCost = [leftHeuristic, upHeuristic, rightHeuristic, downHeuristic]

        algorithmCost = [leftCost + leftHeuristic, upCost + upHeuristic, rightCost + rightHeuristic,
                         downCost + downHeuristic]
        nextElement = [nodeLeftElement, nodeUpElement, nodeRightElement, nodeDownElement]

    ##if current node is at bottom left
    if currentNodeIndex == 3:
        if gridList[currentGridNumber].neighbours[0] == -1:
            leftCost = 10
            leftHeuristic = 10
            nodeLeft = ""
            nodeLeftElement = ''
        else:
            leftCost = gridList[(gridList[currentGridNumber].neighbours[0]) - 1].cost[1]
            leftHeuristic = gridList[(gridList[currentGridNumber].neighbours[0]) - 1].heuristic[3]
            nodeLeft = letterList[nodeListIndex - 1]
            nodeLeftElement = gridList[(gridList[currentGridNumber].neighbours[0]) - 1].number
        if gridList[currentGridNumber].neighbours[3] == -1:
            downCost = 10
            downHeuristic = 10
            nodeDown = ""
            nodeDownElement = ''
        else:
            downCost = gridList[(gridList[currentGridNumber].neighbours[3]) - 1].cost[0]
            downHeuristic = gridList[(gridList[currentGridNumber].neighbours[0]) - 1].heuristic[3]
            nodeDown = letterList[nodeListIndex + (userColumns + 1)]
            nodeDownElement = gridList[(gridList[currentGridNumber].neighbours[0]) - 1].number
        rightCost = gridList[currentGridNumber].cost[3]
        rightHeuristic = gridList[currentGridNumber].heuristic[2]
        nodeRight = letterList[nodeListIndex + 1]
        nodeRightElement = gridList[currentGridNumber].number
        upCost = gridList[currentGridNumber].cost[0]
        upHeuristic = gridList[currentGridNumber].heuristic[0]
        nodeUp = letterList[nodeListIndex - (userColumns + 1)]
        nodeUpElement = gridList[currentGridNumber].number
        moveCost = [leftCost, upCost, rightCost, downCost]
        heuristicCost = [leftHeuristic, upHeuristic, rightHeuristic, downHeuristic]

        algorithmCost = [leftCost + leftHeuristic, upCost + upHeuristic, rightCost + rightHeuristic,
                         downCost + downHeuristic]
        nextElement = [nodeLeftElement, nodeUpElement, nodeRightElement, nodeDownElement]

    print("Move cost: " + str(moveCost))
    print("Heuristic cost: " + str(heuristicCost))
    print("Algo cost: " + str(algorithmCost))
    print("Directions: " + str(nextElement))

    # algorithmCost #leftMove,upMove,rightMove,bottomMove costs
    # move direction: 0:left, 1:up, 2:right, 3:down
    openList.append(nodeLeft + "," + nodeUp + "," + nodeRight + "," + nodeDown)
    moveDirection = algorithmCost.index(min(algorithmCost))
    goalStateNode = gridList[goalState - 1].nodes[1]
    print("Goal State Node: " + goalStateNode)
    print("Visited state: " + str(visitedState))
    # if 0 left

    if len(visitedState) == 10:
        print("No path found, too many playgrounds")
        return

    if moveDirection == 0:
        print("Open List: " + str(openList))
        nextCellNumber = nextElement[moveDirection]
        if nodeLeft == goalStateNode:
            visitedState.append(goalStateNode)
            print("Visited state: " + str(visitedState))
            print("Goal state reached")
            return
        else:
            print("nextCellNumber: " + str(nextCellNumber))
            print("nextNodeLeft: " + nodeLeft)
            print("___________________")
            return traverseGrid(nextCellNumber - 1, nodeLeft)

    if moveDirection == 1:
        print("Open List: " + str(openList))
        nextCellNumber = nextElement[moveDirection]
        if nodeRight == goalStateNode:
            visitedState.append(goalStateNode)
            print("Visited state: " + str(visitedState))
            print("Goal state reached")
            return
        else:
            print("nextCellNumber: " + str(nextCellNumber))
            print("nextNodeUp: " + nodeUp)
            print("___________________")
            return traverseGrid(nextCellNumber - 1, nodeUp)

    if moveDirection == 2:
        print("Open List: " + str(openList))
        nextCellNumber = nextElement[moveDirection]
        if nodeRight == goalStateNode:
            visitedState.append(goalStateNode)
            print("Visited state: " + str(visitedState))
            print("Goal state reached")
            return
        else:
            print("nextCellNumber: " + str(nextCellNumber))
            print("nextNodeRight: " + nodeRight)
            print("___________________")
            return traverseGrid(nextCellNumber - 1, nodeRight)

    if moveDirection == 3:
        print("Open List: " + str(openList))
        nextCellNumber = nextElement[moveDirection]
        if nodeDown == goalStateNode:
            visitedState.append(goalStateNode)
            print("Visited state: " + str(visitedState))
            print("Goal state reached")
            return
        else:
            print("nextCellNumber: " + str(nextCellNumber))
            print("nextNodeDown: " + nodeDown)
            print("___________________")
            return traverseGrid(nextCellNumber - 1, nodeDown)


# while goalStateNode != gridList[nextCell].nodes[1]:

traverseGrid(currentNumber, startingNode)


def aAlgorithm(element):
    print("Optimal Path:")
    optimalPath = PriorityQueue()



# for role P: cost = (left,top,right,bottom)
infinity = np.inf
for i in range(0, len(gridList)):
    # if there are no neighbours on the left
    if gridList[i].neighbourLocations[0] == "0":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = 0
    # if there are no neighbours on the top
    if gridList[i].neighbourLocations[1] == "0":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = 0
    # if there are no neighbours on the right
    if gridList[i].neighbourLocations[2] == "0":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = 0
    # if there are no neighbours on the bottom
    if gridList[i].neighbourLocations[3] == "0":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = 0
    ######### if there is a neighbour that is a quarantine place
    if gridList[i].neighbourLocations[0] == "Q":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = infinity
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = infinity
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = infinity
    if gridList[i].neighbourLocations[1] == "Q":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = infinity
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = infinity
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = infinity
    if gridList[i].neighbourLocations[2] == "Q":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = infinity
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = infinity
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = infinity
    if gridList[i].neighbourLocations[3] == "Q":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = infinity
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = infinity
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = infinity

    ############## if there is a neighbour that is a vaccine place
    if gridList[i].neighbourLocations[0] == "V":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = 1.5
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = 1
    if gridList[i].neighbourLocations[1] == "V":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = 1.5
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = 1
    if gridList[i].neighbourLocations[2] == "V":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = 1.5
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = 1
    if gridList[i].neighbourLocations[3] == "V":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = 1.5
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = 2
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = 1

    ############## if there is a neighbour that is a playground
    if gridList[i].neighbourLocations[0] == "P":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = 0.5
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = 1
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = 0
    if gridList[i].neighbourLocations[1] == "P":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = 0.5
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = 1
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = 0
    if gridList[i].neighbourLocations[2] == "P":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = 0.5
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = 1
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = 0
    if gridList[i].neighbourLocations[3] == "P":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = 0.5
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = 1
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = 0

        ############## if there is a neighbour that is EMPTY
    if gridList[i].neighbourLocations[0] == "E":
        if gridList[i].locationType == "Q":
            gridList[i].cost[0] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[0] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[0] = 1.5
        if gridList[i].locationType == "P":
            gridList[i].cost[0] = 0.5
    if gridList[i].neighbourLocations[1] == "E":
        if gridList[i].locationType == "Q":
            gridList[i].cost[1] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[1] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[1] = 1.5
        if gridList[i].locationType == "P":
            gridList[i].cost[1] = 0.5
    if gridList[i].neighbourLocations[2] == "E":
        if gridList[i].locationType == "Q":
            gridList[i].cost[2] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[2] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[2] = 1.5
        if gridList[i].locationType == "P":
            gridList[i].cost[2] = 0.5
    if gridList[i].neighbourLocations[3] == "E":
        if gridList[i].locationType == "Q":
            gridList[i].cost[3] = infinity
        if gridList[i].locationType == "E":
            gridList[i].cost[3] = 1
        if gridList[i].locationType == "V":
            gridList[i].cost[3] = 1.5
        if gridList[i].locationType == "P":
            gridList[i].cost[3] = 0.5