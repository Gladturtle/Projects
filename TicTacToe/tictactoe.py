
import os
import random

def display_board(board):
    os.system('cls')
    pos = board
    print("   {}  |  {}  |  {} ".format(pos[0],pos[1],pos[2]))
    print("_ _ _ _ _ _ _ _ _ _")
    print("   {}  |  {}  |  {} ".format(pos[3],pos[4],pos[5]))
    print("_ _ _ _ _ _ _ _ _ _")
    print("   {}  |  {}  |  {} ".format(pos[6],pos[7],pos[8]))



def player_input(lastchoice):
    mydict = {"X":"O","O":"X"}
    thedict = {"X":"1","O":"2"}
    choice = mydict[lastchoice]
    print("It is Player {} chance".format(thedict[choice]))
    return choice

def place_marker(board, marker, position):
    board[position-1] = marker


def win_check(board):
    if board[0]==board[3]==board[6]!=' ' or board[1]==board[4]==board[7]!=' ' or board[2]==board[5]==board[8]!=' ' or board[0]==board[1]==board[2]!=' ' or board[3]==board[4]==board[5]!=' ' or board[6]==board[7]==board[8]!=' ' or board[0]==board[4]==board[8]!=' ' or board[2]==board[4]==board[6]!=' ':
      return True
    return False


def choose_first():
     return random.randint(1,2)
 
def space_check(board, position):
    if position>9:
        return True
    if board[position-1]==" ":
        return False
    else:
        return True

def full_board_check(board):
    count = 0
    for char in board:
        if char == " ":
            count +=1
    return count==0

def player_choice(board):
    choice = "D"
    space = True
    while choice.isdigit()==False or space :
        choice = input("Please enter position of character from 1-9")
        if choice.isdigit():
            space = space_check(board,int(choice))
    return int(choice)

def replay():
    choice = "1"
    while choice not in ["Y","N"]:
        choice = input("Do you want to play again(Y or N)?")
    return choice=="Y"

print('Welcome to Tic Tac Toe!')
playagain = True
tiecheck = False
choice = ""
position = 10
wincheck = False
lastchoice = 0
mydict = {"X":"1","O":"2"}
thedict = {1:"X",2:"O"}
while playagain:#while True:
    board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
    display_board(board) # Set the game up here
    lastchoice = choose_first()
    lastchoice = thedict[lastchoice]
    wincheck = False
    while wincheck == False:
        choice = player_input(lastchoice)
        lastchoice = choice
        position = player_choice(board)
        place_marker(board,choice,position)
        display_board(board)
        wincheck = win_check(board)
        if wincheck == False:
            tiecheck = full_board_check(board)
            if tiecheck == True:
                print("The game has tied")
                break
        else:
            print("Player {} has won!!!".format(mydict[choice])) 
            
    playagain = replay()


