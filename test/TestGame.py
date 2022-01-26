#import req libs
import random
import os
import pandas as pd

#first we have menu driven part
def main_menu():
    print()
    print("Welcome to Tic-Tac-Toe!")
    print("1. Play")
    print("2. Records")
    print("3. Exit")
    try:
        option=int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input, please enter a number")
        main_menu()
    if(option==1):
        game_main()
    elif(option==2):
        records()
    elif(option==3):
        print("Goodbye!\n")
        exit()
    else:
        print("Invalid option, please try again")
        main_menu()

#game menu
def game_main():
    print()
    print("Select mode:")
    print("1. vs Computer")
    print("2. vs Human")
    print("3. Go back")
    try:
        pOption=int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input, please enter a number")
        game_main()
    if(pOption==1):
        play("AI")
    elif(pOption==2):
        play("PvP")
    elif(pOption==3):
        print()
        main_menu()
    else:
        print("Invalid option, please try again")
        game_main()

#records menu
def records():
    print()
    print("What do you want to do?")
    print("1. View all records")
    print("2. View my record")
    print("3. Delete my record")
    print("4. Change name")
    print("5. Go back")
    print("6. Exit")
    try:
        rOption=int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input, please enter a number")
        records()
    if(rOption==1):
        view_all()
    elif(rOption==2):
        view_single()
    elif(rOption==3):
        delete()
    elif(rOption==4):
        change_name()
    elif(rOption==5):
        print()
        main_menu()
    elif(rOption==6):
        print("Goodbye!\n")
        exit()
    else:
        print("Invalid option, please try again.")
        records()

def play(choice):
    df=pd.read_csv("records.csv")
    
    #print(df.isin(['ta']).any().any())
    
    print()
    p1_name=input("Player 1, enter your name: ")
    p1_name=p1_name.strip().lower()

    #if(df.isin([p1_name]).any().any()):
    #    print("Name found!\n")

    if(not df.isin([p1_name]).any().any()):
        p1attrDict = {
                        'Name'                          :   [p1_name],
                        'AI matches played'             :   [0],
                        'AI wins'                       :   [0],
                        'AI losses'                     :   [0],
                        'AI ties'                       :   [0],
                        'PvP matches played'            :   [0],
                        'PvP wins'                      :   [0],
                        'PvP losses'                    :   [0],
                        'PvP ties'                      :   [0]}
        p1_data=pd.DataFrame(p1attrDict)
        p1_data.to_csv('records.csv', mode='a', index=False, header=False)
        #df.append(p1attrDict, ignore_index=True)

    if(choice=="PvP"):
        p2_name=input("Player 2, enter your name: ")
        p2_name=p2_name.strip().lower()

        #if(df.isin([p2_name]).any().any()):
        #    print("Name found!\n")
        if(not df.isin([p2_name]).any().any()):
            p2attrDict = {
                        'Name'                          :   [p2_name],
                        'AI matches played'             :   [0],
                        'AI wins'                       :   [0],
                        'AI losses'                     :   [0],
                        'AI ties'                       :   [0],
                        'PvP matches played'            :   [0],
                        'PvP wins'                      :   [0],
                        'PvP losses'                    :   [0],
                        'PvP ties'                      :   [0]}
            p2_data=pd.DataFrame(p2attrDict)
            p2_data.to_csv('records.csv', mode='a', index=False, header=False)
            #df.append(p2attrDict, ignore_index=True)
    #from this point no changes in the overall dataframe is gonna take place so we can drop the unnamed col right here
    #df.drop(columns=['Unnamed: 0'], inplace=True)

    #we read again bc new names could have been added and we want to change their values acc to the results
    df=pd.read_csv("records.csv")
    if(choice=="PvP"):
        df.loc[df.Name==p2_name,['PvP matches played']]+=1
        df.loc[df.Name==p1_name,['PvP matches played']]+=1
    else:
        df.loc[df.Name==p1_name,['AI matches played']]+=1
    #extra print for cleaner ui
    print()
    
    board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    end = False
    win_commbinations = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

    def draw():
        print(board[0],'|',board[1],'|',board[2])
        print('----------')
        print(board[3],'|',board[4],'|', board[5])
        print('----------')
        print(board[6],'|', board[7],'|', board[8])
        print()

    def choose_number():
        while True:
            a = input()
            try:
                a  = int(a)
                a -= 1
                if a in range(0, 9):
                    return a
                else:
                    print("\nThat's not on the board. Try again")
                    continue
            except ValueError:
                print("\nThat's not a number. Try again")
                continue
    def p1():
        n = choose_number()
        if board[n] == "X" or board[n] == "O":
            print("\nYou can't go there. Try again")
            p1()
        else:
            board[n] = "X"

    def p2():
        if(choice=="PvP"):
            n = choose_number()
            if board[n] == "X" or board[n] == "O":
                print("\nYou can't go there. Try again")
                p2()
            else:
                board[n] = "O"
        else:
            AI_turn()
    
    def make_copy():
        board_copy=[]
        for i in range(0,9):
            board_copy.append(board[i])
        return board_copy

    def AI_turn():
        #Note: the only way to trick the ai in this strategy is to pick any 3 corners as first 3 moves
        #check if there is a winning move for AI
        print("The computer made a move!")
        copy=make_copy()
        for i in range(0,9):
            if(copy[i]!='X' and copy[i]!='O'):
                copy[i]='O'
                for a in win_commbinations:
                    #if this move wins, we set that board position to that value and break
                    if copy[a[0]] == copy[a[1]] == copy[a[2]] == "O":
                        board[i]='O'
                        return
                #if we can't find a winning move, we reset the board position
                copy[i]=i

        #check if there is a winning move for the player, if yes then block it
        copy=make_copy()
        for i in range(0,9):
            if(copy[i]!='X' and copy[i]!='O'):
                copy[i]='X'
                for a in win_commbinations:
                    #if this move wins, we set block that pos with our letter O
                    if copy[a[0]] == copy[a[1]] == copy[a[2]] == "X":
                        board[i]='O'
                        return
                #if there is no need to block after this hypothetical move, we reset the board 
                copy[i]=i 

        #if there is no winning/losing combo, we choose a pos acc to an order:
        #first we check for the center, because it is a part of 4 winning combos
        if(board[4]!='X' and board[4]!='O'):
            board[4]='O'
            return

        #next we check for the corners, because each of them is a part of 3 winning combos
        random_corner=[]
        #we add corner indices of unfilled cells, can't run loop bc of irregular increment
        if(board[0]!='X' and board[0]!='O'):
            random_corner.append(0)

        if(board[2]!='X' and board[2]!='O'):
            random_corner.append(2)

        if(board[6]!='X' and board[6]!='O'):
            random_corner.append(6)

        if(board[8]!='X' and board[8]!='O'):
            random_corner.append(8)

        #if we have at least 1 unfilled corner        
        if(len(random_corner)>0):
            #here we avoid a simple trick to win
            if(len(random_corner)==2):
                if((0 in random_corner and 8 in random_corner) or (2 in random_corner and 6 in random_corner)):
                    if(board[4]!='O'):
                        board[random.choice(random_corner)]='O'
                        return
                else:
                    board[random.choice(random_corner)]='O'
                    return
            else:
                board[random.choice(random_corner)]='O'
                return

        #finally we randomly pick a side position, bc they are in the fewest winning combos- 2
        random_side=[]
        #we add corner indices of unfilled cells, here we can run loop
        for i in range(1,8,2):
            if(board[i]!='X' and board[i]!='O'):
                random_side.append(i)

        #if we have at least 1 unfilled corner        
        if(len(random_side)>0):
            board[random.choice(random_side)]='O'
            return

    def check_board():
        count = 0
        for a in win_commbinations:
            if board[a[0]] == board[a[1]] == board[a[2]] == "X":
                if(choice=="PvP"):
                    df.loc[df.Name==p1_name,['PvP wins']]+=1
                    df.loc[df.Name==p2_name,['PvP losses']]+=1
                else:
                    df.loc[df.Name==p1_name,['AI wins']]+=1
                print(p1_name,"wins!")
                return True
        
            if board[a[0]] == board[a[1]] == board[a[2]] == "O":
                if(choice=="PvP"):
                    df.loc[df.Name==p2_name,['PvP wins']]+=1
                    df.loc[df.Name==p1_name,['PvP losses']]+=1
                    print(p2_name,"wins!")
                else:
                    df.loc[df.Name==p1_name,['AI losses']]+=1
                    print("Computer wins!")
                return True
                
        for a in range(9):
            if board[a] == "X" or board[a] == "O":
                count += 1
            if count == 9:
                if(choice=="PvP"):
                    df.loc[df.Name==p1_name,['PvP ties']]+=1
                    df.loc[df.Name==p2_name,['PvP ties']]+=1
                else:
                    df.loc[df.Name==p1_name,['AI ties']]+=1
                print("The game ends in a Tie!")
                return True

    while not end:
        draw()
        end = check_board()
        if end == True:
            break
        print(p1_name,"choose where to place a cross")
        p1()
        print()
        draw()
        end = check_board()
        if end == True:
            break
        if(choice=="PvP"):
            print(p2_name,"choose where to place a nought")
        p2()
        print()
    
    #confirming all the changes to the df
    df.to_csv("records.csv", index=False)

    print()
    print("Returning to main menu")
    main_menu()

def view_all():
    temp=pd.read_csv("records.csv")
    print()
    if(len(temp.index)==0):
        print("No games have been played yet.")
    else:
        print(temp)
    records()

def view_single():
    temp=pd.read_csv("records.csv")
    print()
    try:
        name=input("Please enter your name: ")
        name=name.strip().lower()
    except Exception:
        print("Name should be a string, try again.")
        view_single()
    if(not temp.isin([name]).any().any()):
        print("No record found!")
    else:
        print()
        print(temp.loc[temp.Name==name])
    records()

def delete():
    temp=pd.read_csv("records.csv")
    print()
    try:
        name=input("Please enter your name: ")
        name=name.strip().lower()
    except Exception:
        print("Name should be a string, try again.")
        delete()
    if(not temp.isin([name]).any().any()):
        print("No record found!")
    else:
        i=temp[(temp.Name==name)].index
        temp.drop(i, inplace=True)
        print("Record deleted successfully!")
    temp.to_csv("records.csv", index=False)
    records()

def change_name():
    temp=pd.read_csv("records.csv")
    print()
    try:
        name=input("Please enter your current username: ")
        name=name.strip().lower()
    except Exception:
        print("Name should be a string, try again.")
        change_name()
    if(not temp.isin([name]).any().any()):
        print("No record found!")
    else:
        try:
            new_name=input("Please enter your new username: ")
            new_name=new_name.strip().lower()
        except Exception:
            print("Name should be a string, try again.")
            change_name()
        if(temp.isin([new_name]).any().any()):
                print("Name already in use, try again")
                change_name()
        else:
            temp.loc[temp.Name==name,['Name']]=new_name
            print("Name changed successfully!")
    temp.to_csv("records.csv", index=False)
    records()

if not os.path.isfile('./records.csv'):
    import test
    test.create()

#df.drop(columns='Unnamed: 0')

#for appending a csv file: df.to_csv('existing.csv', mode='a', index=False, header=False)
#notes for pandas work:
#we don't need to keep appending or importing csv files
#if the name doesn't exist already for p1 and/or p2, we just add their attribute dictionary to the dataframe and we append the dataframe to the main data
#from there we just need to update the values corresponding to each player
#initially, read the main data as a 'df' dataframe and if required, we make a new df everytime we play the game and just append it to the main data DataFrame
#since we have read the main data file, making changes like updating vals deleting cols will be straightforward 

#update: there is no need to create a dataframe, since we already have the main data, we can just append the dicts to it directly

main_menu()