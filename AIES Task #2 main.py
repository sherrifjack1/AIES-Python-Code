#Core Libaries
import os
import time

#Global Variables
reloadTime = 2
gameBoard = [' ' for _ in range(9)]

#Core Game Logic
def getWinner():
    # Check rows
    for row in range(0, 9, 3):
        if gameBoard[row] == gameBoard[row + 1] == gameBoard[row + 2] and gameBoard[row] != ' ':
            return True
    
    # Check columns
    for col in range(3):
        if gameBoard[col] == gameBoard[col + 3] == gameBoard[col + 6] and gameBoard[col] != ' ':
            return True
    
    # Check diagonals
    if gameBoard[0] == gameBoard[4] == gameBoard[8] and gameBoard[0] != ' ':
        return True
    if gameBoard[2] == gameBoard[4] == gameBoard[6] and gameBoard[2] != ' ':
        return True
    
    return False

#Minimax Algorithm
def getMinimaxDecision(aiPlayer,opponentPlayer):
    # Define the maximizing player (AI)
    aiPlayer = 'O'
    opponentPlayer = 'X'
    
    def minimax(board, isMaximizing):
        #Check Winner of specific boards
        def getWinnerSpecific(player, board):
            # Check rows
            for row in range(0, 9, 3):
                if board[row] == board[row + 1] == board[row + 2] == player:
                    return True
            # Check columns
            for col in range(3):
                if board[col] == board[col + 3] == board[col + 6] == player:
                    return True
            # Check diagonals
            if board[0] == board[4] == board[8] == player:
                return True
            if board[2] == board[4] == board[6] == player:
                return True
            return False
        
        # Base case: check for terminal states
        if getWinnerSpecific(aiPlayer, board):
            return 1
        elif getWinnerSpecific(opponentPlayer, board):
            return -1
        elif ' ' not in board:
            return 0

        # Maximizing turn
        if isMaximizing:
            bestScore = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = aiPlayer
                    score = minimax(board, False)
                    board[i] = ' '
                    bestScore = max(bestScore, score)
            return bestScore

        # Minimizing turn
        else:
            bestScore = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = opponentPlayer
                    score = minimax(board, True)
                    board[i] = ' '
                    bestScore = min(bestScore, score)
            return bestScore

    # Actual decision-making
    bestMove = None
    bestScore = -float('inf')
    for i in range(9):
        if gameBoard[i] == ' ':
            gameBoard[i] = aiPlayer
            score = minimax(gameBoard, False)
            gameBoard[i] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = i

    return bestMove

#Alpha-Beta pruning Algorithm
def getAlphaBetaDecision(aiPlayer,opponentPlayer):
    def alphabeta(board, depth, alpha, beta, isMaximizing):
        # Check winner of specific boards
        def getWinnerSpecific(player, board):
            # Check rows
            for row in range(0, 9, 3):
                if board[row] == board[row + 1] == board[row + 2] == player:
                    return True
            # Check columns
            for col in range(3):
                if board[col] == board[col + 3] == board[col + 6] == player:
                    return True
            # Check diagonals
            if board[0] == board[4] == board[8] and board[0] == player:
                return True
            if board[2] == board[4] == board[6] and board[2] == player:
                return True
            return False
        
        # Base cases
        if getWinnerSpecific(aiPlayer, board):
            return 1
        elif getWinnerSpecific(opponentPlayer, board):
            return -1
        elif ' ' not in board:
            return 0

        if isMaximizing:
            maxEval = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = aiPlayer
                    eval = alphabeta(board, depth + 1, alpha, beta, False)
                    board[i] = ' '
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cut-off
            return maxEval
        else:
            minEval = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = opponentPlayer
                    eval = alphabeta(board, depth + 1, alpha, beta, True)
                    board[i] = ' '
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
            return minEval

    # Actual decision-making
    bestMove = None
    bestScore = -float('inf')
    for i in range(9):
        if gameBoard[i] == ' ':
            gameBoard[i] = aiPlayer
            score = alphabeta(gameBoard, 0, -float('inf'), float('inf'), False)
            gameBoard[i] = ' '
            if score > bestScore:
                bestScore = score
                bestMove = i

    return bestMove

#Front End Interface
def matchSingle():
    #Begin Loop
    option = 1
    aiPlayer = '0'
    humanPlayer = 'X'
    playerTurn = humanPlayer
    while option > 0:
        #Clear the screen
        os.system('cls')
    
        #Start Message
        print("Simgle Player match") 
        displayBoard()
        
        # process player turn
        if playerTurn == humanPlayer:
            #Give Player Options
            print("Human Player select your option: ")
        
            #Print only valid option numbers
            print("0. Exit")
            print("Valid Slots: ",[idx + 1 for idx, value in enumerate(gameBoard) if value == ' '])
            
            #Get the Player's Option
            option = getInterfaceOption()
            print("Human Player has selected ",option)
            
            #Process the Options
            validMove = False
            if option == 0:
                exit()
            elif gameBoard[option - 1] == ' ':
                gameBoard[option - 1] = humanPlayer
                validMove = True
            else:
                processInvalidRange()
        else:
            #AI player processing
            option = getMinimaxDecision(aiPlayer,humanPlayer)
            print("AI Player has selected ",option)
            gameBoard[option] = aiPlayer
            validMove = True
            
        #Check if the board has no more valid options
        if ' ' not in gameBoard:
            break
            
        #Check if the player won
        if getWinner():
            break
        
        #If ValidMove Change Players
        if validMove:
            if playerTurn == humanPlayer: playerTurn = aiPlayer
            else: playerTurn = humanPlayer
    #Clear the screen
    os.system('cls')
    
    #Print the winning player and match Result
    if getWinner():
        displayInterfaceResult(playerTurn)
    else:
        displayInterfaceResult("")
    
def matchMulti():
    #Begin Loop
    option = 1
    player = 'X'
    while option > 0:
        #Clear the screen
        os.system('cls')
    
        #Start Message
        print("Multiplayer match") 
        displayBoard()
        
        #Give Player Options
        print("Player ",player," select your option: ")
        
        #Print only valid option numbers
        print("0. Exit")
        print("Valid Slots: ",[idx + 1 for idx, value in enumerate(gameBoard) if value == ' '])
        
        #Get the Player's Option
        option = getInterfaceOption()
        print("Player ",player," has selected ",option)
        
        #Process the Options
        validMove = False
        if option == 0:
            exit()
        elif gameBoard[option - 1] == ' ':
            gameBoard[option - 1] = player
            validMove = True
        else:
            processInvalidRange()
        
        #Check if the board has no more valid options
        if ' ' not in gameBoard:
            break
            
        #Check if the player won
        if getWinner():
            break
        
        #If ValidMove Change Players
        if validMove:
            if player == 'X': player = '0'
            else: player = 'X'
    #Clear the screen
    os.system('cls')
    
    #Print the winning player and match Result
    displayInterfaceResult(player)
    
def matchTest():
    #Begin Loop
    option = 1
    minimaxPlayer = '0'
    alphaBetaPlayer = 'X'
    playerTurn = alphaBetaPlayer
    
    # Time tracking
    alphaBetaTimes = []
    minimaxTimes = []
    
    while option > 0:
        #Clear the screen
        os.system('cls')
    
        #Start Message
        print("Alpha Beta vs Minimax match") 
        displayBoard()
        
        # process player turn
        if playerTurn == alphaBetaPlayer:
            #Alpha Beta player processing
            start_time = time.time()
            option = getAlphaBetaDecision(alphaBetaPlayer, minimaxPlayer) + 1
            end_time = time.time()
            alphaBetaTimes.append(end_time - start_time)
            print("Alpha Beta Player has selected ",option)
            print(f"Alpha Beta Decision Time: {end_time - start_time:.5f} seconds")
            gameBoard[option-1] = alphaBetaPlayer
            validMove = True
        else:
            #Minimax player processing
            start_time = time.time()
            option = getMinimaxDecision(minimaxPlayer,alphaBetaPlayer)+1
            end_time = time.time()
            minimaxTimes.append(end_time - start_time)
            print("Minimax Player has selected ",option)
            print(f"Minimax Decision Time: {end_time - start_time:.5f} seconds")
            gameBoard[option-1] = minimaxPlayer
            validMove = True
            
        #Check if the board has no more valid options
        if ' ' not in gameBoard:
            break
            
        #Check if the player won
        if getWinner():
            break
        
        #If ValidMove Change Players
        if validMove:
            if playerTurn == alphaBetaPlayer: playerTurn = minimaxPlayer
            else: playerTurn = alphaBetaPlayer
        
        time.sleep(2)
    #Clear the screen
    os.system('cls')
    
    #Match Analysis
    avgAlphaBeta = sum(alphaBetaTimes) / len(alphaBetaTimes)
    print(f"\nAverage Alpha Beta Decision Time: {avgAlphaBeta:.5f} seconds")
    avgMinimax = sum(minimaxTimes) / len(minimaxTimes)
    print(f"Average Minimax Decision Time: {avgMinimax:.5f} seconds")
    
    #Print the winning player and match Result
    if getWinner():
        displayInterfaceResult(playerTurn)
    else:
        displayInterfaceResult("")
        
    
    
def beginMatchMain(matchType):
    print(matchType)
    #Reset Data
    global gameBoard 
    gameBoard = [' ' for _ in range(9)]
    
    #Process Match Type
    if matchType == 1:
        matchSingle()
    elif matchType == 2:
        matchMulti() 
    elif matchType == 3:
        matchTest()
        
def getInterfaceOption():
    #Infinite loop till receive valid type int input
    while True:
        try:
            option = int(input("Enter selected number: "))
            return option
        except ValueError:
            print("Invalid input. Please enter a number.")

def processInvalidRange():
    #Wait time till entering new options, if option is not in range
    print("Selected number not in range.")
    x = reloadTime
    while x > 0:
        print("Reloading in ",x," seconds.")
        time.sleep(1)
        x-=1

def displayBoard():
    for row in [gameBoard[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def displayInterfaceResult(player):
    
    #Display Results
    if player=="":
        print("It's a TIE!")
    else:
        print("Player ",player," has Won!")
    displayBoard()
    
    #Display options
    print("0. Play Again")
    
    #Get Options
    option = getInterfaceOption()
    print("You have chosen ",option)
    
    #Process Options
    if option == 0:
        displayInterfacePlay()
    else:
        processInvalidRange()
        displayInterfaceResult(player)
    
def displayInterfacePlay():
    #Clear the screen
    os.system('cls')
    
    #Display options
    print("0. Exit")
    print("1. Singleplayer")
    print("2. Multiplayer")
    print("3. TestAI")
    
    #Get Options
    option = getInterfaceOption()
    print("You have chosen ",option)
    
    #Process Options
    if option == 0:
        exit()
    elif option >= 1 and option <= 3:
        beginMatchMain(option)
    else:
        processInvalidRange()
        
        displayInterfaceMain()
    
def displayInterfaceMain():
    #Clear the screen
    os.system('cls')
    
    #Display options
    print("0. Exit")
    print("1. Play")
    
    #Get Options
    option = getInterfaceOption()
    print("You have chosen ",option)
    
    #Process Options
    if option == 0:
        exit()
    elif option == 1:
        displayInterfacePlay()
    else:
        processInvalidRange()
        
        displayInterfaceMain()
        
displayInterfaceMain()
