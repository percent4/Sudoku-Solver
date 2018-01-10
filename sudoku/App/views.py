import json
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html')

#Read a Sudoku puzzle from index.html page
def readAPuzzle(lst):
    grid=[]
    for i in range(9):
        grid.append(lst[9*i:9*(i+1)])
 
    return grid
 
#Obtain a list of free cells from the puzzle
def getFreeCellList(grid):
    freeCellList=[]
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                freeCellList.append([i,j])
 
    return freeCellList

#Search for a solution
def search(grid):
    freeCellList=getFreeCellList(grid)
    numberOfFreeCells=len(freeCellList)
    if numberOfFreeCells == 0:
        return True
     
    k=0  #Start from the first free cell
 
    while True:
        i=freeCellList[k][0]
        j=freeCellList[k][1]
        if grid[i][j] == 0:
            grid[i][j]=1
 
        if isValid(i,j,grid):
            if k+1 == numberOfFreeCells:
                #no more free cells
                return True  #A solution is found
            else:
                #Move to the next free cell
                k += 1
        elif grid[i][j] < 9:
            #Fill the free cell with the next possible value
            grid[i][j] += 1
        else:
            #grid[i][j] is 9,backtrack
            while grid[i][j] == 9:
                if k == 0:
                    return False  #No possible value
                grid[i][j]=0  #Reset to free cell
                k -= 1  #Backtrack to the preceding free cell
                i=freeCellList[k][0]
                j=freeCellList[k][1]
 
 
            #Fill the free cell with the next possible value
            #search continues from this free cell at k
            grid[i][j] += 1
 
    return True  #A solution is found
 
#Check whether grid[i][j] is valid in the grid
def isValid(i,j,grid):
    #Check whether grid[i][j] is valid at the i's row
    for column in range(9):
        if column != j and grid[i][column] == grid[i][j]:
            return False
         
    #Check whether grid[i][j] is valid at the j's column
    for row in range(9):
        if row != i and grid[row][j] == grid[i][j]:
            return False
 
    #Check whether grid[i][j] is valid at the 3-by-3 box
    for row in range((i//3)*3,(i//3)*3+3):
        for col in range((j//3)*3,(j//3)*3+3):
            if row != i and col != j and grid[row][col] == grid[i][j]:
                return False
             
    return True #The current value at grid[i][j] is valid
 
#Check whether the fixed cells are valid in the grid
def isValidGrid(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] not in range(10) or (grid[i][j] in range(1,10) and not isValid(i,j,grid)):
                return False
    return True

def answer(request):
    #Get input from the index.html page
    get_lst = request.REQUEST.getlist("grid")
	#original grid to store the input numbers, replace empty string with 0
    grid_orig = readAPuzzle(lst = [int(_) if _ else 0 for _ in get_lst])
	#the grid that store a answer with latter processing
    grid = readAPuzzle(lst = [int(_) if _ else 0 for _ in get_lst])
	
	#information to output
    info = ""
    if not isValidGrid(grid):
        info = "Invalid input"
    elif search(grid):
        info = "The solution is found:"
    else:
        info = "No solution!"
    return render_to_response('answer.html',{'grid_orig':json.dumps(grid_orig),'grid':json.dumps(grid),'info':info})
