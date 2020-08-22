import random
import copy 


def listValidMoves(board,player):
    possibleMoves=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        moveRowInc=-1
    else:
        playerTokens=["r","R"]
        moveRowInc=1
    kingTokens=["B","R"]
    for row in range(8): #For every row
        for col in range(8):  #For every square in a row
            if board[row][col] in playerTokens: #If the board contains either a regular or king checker of the given player
                if board[row][col] not in kingTokens: #if checker is NOT a king
                    for colInc in [-1,1]: #for each diagonal square in the correct row direction
                        if row+moveRowInc in validRange and col+colInc in validRange and board[row+moveRowInc][col+colInc] =='e':
                            possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+moveRowInc)+str(col+colInc))
                else:  #checker is a king
                    for rowInc in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]: #for each diagonal square in each row direction
                            if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] =='e':
                                possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+rowInc)+str(col+colInc))              
    return possibleMoves

def listSingleJumps(board,player):
    possibleSingleJumps=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        enemyTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        enemyTokens=["b","B"]
    kingTokens=["B","R"]
    for row in range(8): #For every row
        for col in range(8):
            if board[row][col] in playerTokens:
                if board[row][col] not in kingTokens:  #if checker is NOT a king
                    for colInc in [-1,1]:
                        if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] in enemyTokens:                        
                            colJumpInc=2 * colInc
                            rowJumpInc=2 * rowInc
                            if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
                else: #checker is a king
                    for rowIncs in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]:
                            if row+rowIncs in validRange and col+colInc in validRange and board[row+rowIncs][col+colInc] in enemyTokens:                        
                                colJumpInc=2 * colInc
                                rowJumpInc=2 * rowIncs
                                if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                    possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
    return possibleSingleJumps

def listMultipleJumps(board,player,jumpsList):
    newJumps=expandJumps(board,player,jumpsList)
    while newJumps != jumpsList:
        jumpsList=newJumps[:]
        newJumps=expandJumps(board,player,jumpsList)
    return newJumps

def expandJumps(board,player,oldJumps):
    INCs=[1,-1]
    VALID_RANGE=[0,1,2,3,4,5,6,7]
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        opponentTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        opponentTokens=["b","B"]
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if board[startRow][startCol] not in ["R","B"]: #not a king
            for colInc in INCs:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and board[jumprow][jumpcol] in opponentTokens and board[torow][tocol]=='e':
                    newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                    if oldJump in newJumps:
                        newJumps.remove(oldJump)
        else: #is a king
            for colInc in INCs:
                for newRowInc in INCs:
                    jumprow=row+newRowInc
                    jumpcol=col+colInc
                    torow=row+2*newRowInc
                    tocol=col+2*colInc
                    if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                    and board[jumprow][jumpcol] in opponentTokens and (board[torow][tocol]=='e' or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                    and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)) and (chr(torow+65)+str(tocol)!=oldJump[-5:-3]):
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
    return newJumps          

def findCrownRowMovesOrJumps(board,player,movesList):
    kingingList=[]
    for move in movesList:
        FROM=move[0:2]
        FROMRow=ord(FROM[0])-65
        FROMCol=int(FROM[1])
        TO=move[-2:]
        TORow=TO[0]
        if player=="r":
            kingRow="H"
        else:
            kingRow="A"
        if board[FROMRow][FROMCol]==player and TORow==kingRow:
            kingingList.append(move)
            movesList=movesList[:movesList.index(move)]+movesList[movesList.index(move)+1:]
    return kingingList

def findJumpBlockOpponent(playerJumps,opponentMoves):
    blockMovesList=[]
    for jump in playerJumps:
        for move in opponentMoves:
            if jump[-2:] in move:
                blockMovesList.append(jump)
    return blockMovesList

def protectHomeRow(player,playerMoves):
    outsideMovesList=[]
    if player=="b":
        for move in playerMoves:
            if move[:1]!="H":
                outsideMovesList.append(move)  
    else:
        for move in playerMoves:
            if move[:1]!="A":
                outsideMovesList.append(move)   
    return outsideMovesList

def moveHomeRow(player,playerMoves):
    homeRowMovesList=[]
    if player=="b":
        for move in playerMoves:
            if move[:1]=="H":
                homeRowMovesList.append(move)
        return homeRowMovesList
    else:
        for move in playerMoves:
            if move[:1]=="A":
                homeRowMovesList.append(move)
        return homeRowMovesList

def cornerHomeMoves(player,homeRowMovesList):
    cornerRowList=[]
    middleList=[]
    if player=="r":
        for move in homeRowMovesList:
            if move[1]=="0":
                cornerRowList.append(move)
            else:
                middleList.append(move)
    else:
        for move in homeRowMovesList:
            if move[1]=="7":
                cornerRowList.append(move)
            else:
                middleList.append(move)
    return cornerRowList,middleList

def cornerMoves(player,movesList):
    cornerRowList=[]
    middleList=[]
    for move in movesList:
        if move[3:]=="A0"or move[3:]=="H7":
            cornerRowList.append(move)
        else:
            middleList.append(move)
    return cornerRowList,middleList
                
       

def jumpCrownsFirst(playerJumps,board,player,opponentKing):
    validRange=[1,2,3,4,5,6,7]
    kingJumps=[]
    if player=="r":
        oppKing="B"
        rowInc=1
    else:
        oppKing="R"
        rowInc=-1
    kingTokens=["B","R"]
    for jump in playerJumps:
        row=ord(jump[0])-65
        col=int(jump[1])
        if board[row][col] not in kingTokens:
            for colInc in [-1,1]:
                if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc]==oppKing:
                    colJumpInc=2 * colInc
                    rowJumpInc=2 * rowInc
                    if row+rowJumpInc in validRange and col+colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e" and (chr(row+rowJumpInc+65)+str(col+colJumpInc))==jump[3:5]:
                        kingJumps.append(jump)
        else:
            for rowIncs in [-1,1]: #for each row direction (forward and backward)
                for colInc in [-1,1]:
                    if row+rowIncs in validRange and col+colInc in validRange and board[row+rowIncs][col+colInc]==oppKing:
                        colJumpInc=2 * colInc
                        rowJumpInc=2 * rowIncs
                        if row+rowJumpInc in validRange and col+colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e" and (chr(row+rowJumpInc+65)+str(col+colJumpInc))==jump[3:5]:
                            kingJumps.append(jump)
   # print(kingJumps)
    return kingJumps

def takeLongestJump(moveList):
    longest=moveList[0]
    for move in moveList:
        if len(move)>len(longest):
            longest=move
    return longest

def safeMoves(playerList,opponentPlayerList):
    pcopy=playerList
    oppcopy=opponentPlayerList
    unsafeMovesList=[]
    for playerMove in pcopy:
        for opponentMove in oppcopy:
            if (playerMove[-2:] == opponentMove[-2:]) and playerMove not in unsafeMovesList:
                unsafeMovesList.append(playerMove)

    for move in unsafeMovesList:
        if move in pcopy:
            pcopy.remove(move)
    return pcopy,unsafeMovesList

def inBetween(unsafeMovesList,board,player,opponentTokens,playerTokens):
    validRange=[0,1,2,3,4,5,6,7]
    safe=[]
    for move in unsafeMovesList:
        row=ord(move[3])-65
        col=int(move[4])
        if col+1 in validRange and col-1 in validRange and row-1 in validRange and row+1 in validRange:
            if (board[row-1][col+1]!="e") and board[row+1][col-1] in opponentTokens and board[row+1][col+1] not in opponentTokens and (chr(row-1+65)+str(col+1)) not in move:
                safe.append(move)
            elif (board[row-1][col-1]!="e") and board[row+1][col+1] in opponentTokens and board[row+1][col-1] not in opponentTokens and (chr(row-1+65)+str(col-1)) not in move:
                safe.append(move)
            elif (board[row+1][col+1]!="e") and board[row-1][col-1] in opponentTokens and board[row-1][col+1] not in opponentTokens and (chr(row+1+65)+str(col+1)) not in move:
                safe.append(move)
            elif (board[row+1][col-1]!="e") and board[row-1][col+1] in opponentTokens and board[row-1][col-1] not in opponentTokens and (chr(row+1+65)+str(col-1)) not in move:
                safe.append(move)
    #print("safe in between moves",safe)
    return safe

#THIS IS IN THE PROCESS FOR AN ADDITIONAL HEURISTIC -- IGNORE FOR MP13

##def inBetweenJumps(unsafeList,board,player,opponentTokens,playerTokens):
##    validRange=[0,1,2,3,4,5,6,7]
##    unsafe=[]
##    safe=[]
##    for move in unsafeList:
##        startRow=ord(move[0])-65
##        startCol=int(move[1])
##        row=ord(move[3])-65
##        col=int(move[4])
##        print(board[row+1][col-1])
##        if col+1 in validRange and col-1 in validRange and row-1 in validRange and row+1 in validRange:
####            if (player=="r" and board[startRow][startCol]=="r"
####            if board[row+1][col+1] in opponentTokens and board[row-1][col-1] in playerTokens and board[row+1][col-1] not in opponentTokens and (chr(row-1+65)+str(col+1)) not in move:
####                safe.append(move)
####                print(safe)
####            elif board[row+1][col-1] in opponentTokens  and board[row+1][col+1] not in opponentTokens and board[row-1][col+1] in playerTokens and (chr(row-1+65)+str(col+1)) not in move:
####                safe.append(move)
##            if board[row-1][col-1]in opponentTokens and board[row-1][col+1] not in opponentTokens and board[row+1][col+1]!="e" and (chr(row-1+65)+str(col+1)) not in move:
##                safe.append(move)
##            elif board[row-1][col+1]in opponentTokens and board[row-1][col-1] not in opponentTokens and board[row+1][col-1] !="e" and (chr(row-1+65)+str(col+1)) not in move:
##                safe.append(move)
##    print(safe)
##    return safe

def blockCrowningMove(playerMoves,opponentMoves):
    pcopy=playerMoves
    ocopy=opponentMoves
    blockList=[]
    for omove in ocopy:
        for move in pcopy:
            if omove[-2:]==move[-2:]:
                blockList.append(move)
    return blockList                
    

def getValidMove(board,player):
    if player=="b":
        playerName="black"
        playerTokens=["b","B"]
        opponent="r"
        opponentTokens=["r","R"]
        opponentKing="R"
    else:
        playerName="red"
        playerTokens=["r","R"]
        opponent="b"
        opponentTokens=["b","B"]
        opponentKing="B"

    #Get player move options
    movesList=listValidMoves(board,player)
    movesListCopy=movesList
    jumpsList=listSingleJumps(board,player)
    jumpsList=listMultipleJumps(board,player,jumpsList)
    jumpsListCopy=jumpsList
    crowningJumps=findCrownRowMovesOrJumps(board,player,jumpsList)
    crowningMoves=findCrownRowMovesOrJumps(board,player,movesList)

    #Get opponent move options
    opponentMovesList=listValidMoves(board,opponent)
    opponentJumpsList=listSingleJumps(board,opponent)
    opponentJumpsList=listMultipleJumps(board,opponent,opponentJumpsList)
    opponentCrowningJumps=findCrownRowMovesOrJumps(board,opponent,opponentJumpsList)
    opponentCrowningMoves=findCrownRowMovesOrJumps(board,opponent,opponentMovesList)

    blockCrownMovesWithKing=blockCrowningMove(movesList,opponentCrowningMoves)
    jumpKingsList=jumpCrownsFirst(jumpsList,board,player,opponentKing)
    
    if crowningJumps !=[]: #Heuristic 3 (crowning jumps)
        if jumpKingsList!=[]:
            return jumpKingsList[random.randrange(0,len(jumpKingsList))]            #Heuristic 15 (jump a king first)
        else:
            return takeLongestJump(crowningJumps)                                      #Heuristic 9(take longest crowning jump)
    if jumpsList != []: #Heuristic 1 (jumps)
        #print(jumpsList)
        if opponentCrowningJumps !=[]: #Heuristic 5
            longestJump=takeLongestJump(opponentCrowningJumps)
            endPlacement=longestJump[3:5]
            blocking = findJumpBlockOpponent(jumpsList,opponentCrowningJumps)
            if blocking != []:                                                 
                for move in blocking:
                    if move[-2:]==endPlacement:
                      # print("THIS BLOCKS THE LONGEST CROWINGING JUMP",move)
                        return move
        if opponentCrowningMoves != []: #Heuristic 6
            blocking = findJumpBlockOpponent(jumpsList,opponentCrowningMoves)
            if blocking != []:
                return blocking[random.randrange(0,len(blocking))]
            if blockCrownMovesWithKing!=[]:
                #print(blockCrownMovesWithKing)                                  #Heuristic 13 (block crowning Moves with a king move)
                return blockCrownMovesWithKing[random.randrange(0,len(blockCrownMovesWithKing))]
        if opponentJumpsList != []: #Heuristic 7
            longestJump=takeLongestJump(opponentJumpsList)
            endPlacement=longestJump[3:5]
            blocking = findJumpBlockOpponent(jumpsList,opponentJumpsList)
            if blocking != []:                                                   #Heuristic 10 (block opponent's longest jump with a jump)
                for move in blocking:
                    if move[-2:]==endPlacement:
                       #print("THIS BLOCKS THE LONGEST JUMP",move)
                        return move
            return jumpsList[random.randrange(0,len(jumpsList))]
        else:
            if jumpKingsList!=[]:
                #print(jumpKingsList)
                return jumpKingsList[random.randrange(0,len(jumpKingsList))]            #Heuristic 15 (jump a king first)
            else:
                move=takeLongestJump(jumpsListCopy)                                 #Heuristic 9(take longest regular jump)
                return move 
##                safeJumpsList,unsafeJumpsList=safeMoves(jumpsList,opponentMovesList)
##                safeJumpsList+=inBetweenJumps(unsafeJumpsList,board,player,opponentTokens,playerTokens)
##                if safeJumpsList!=[]:
##                    return safeJumpsList[random.randrange(0,len(safeJumpsList))]        
##                else:                                                                     
##                    #print("This is the longest jump",move)
                     
            
                

    if crowningMoves != []: #Heuristic 4 (crowning move)
        avoidCorners,safeMiddles=cornerMoves(player,crowningMoves)
        if safeMiddles!=[]:                                 #Heuristic 16 (don't move into a corner space if you can avoid it)
            return safeMiddles[random.randrange(0,len(safeMiddles))]
        else:
            return avoidCorners[random.randrange(0,len(avoidCorners))]
    else: #Heuristic 2 (moves)  
        if opponentJumpsList!=[]:                                                                                      
            longestJump=takeLongestJump(opponentJumpsList)
            endPlacement=longestJump[3:5]
            blocking = findJumpBlockOpponent(movesListCopy,opponentJumpsList)
            if blocking != []:                                                  #Heuristic 11 (block opponent's longest jump with a move)
                for move in blocking:
                    if move[-2:]==endPlacement:
                        return move
        
        #print(blockCrownMovesWithKing)
        if blockCrownMovesWithKing!=[]:                                          #Heuristic 13 (block crowning Moves with a king move)
            return blockCrownMovesWithKing[random.randrange(0,len(blockCrownMovesWithKing))]
        safeMovesList,unsafeMovesList=safeMoves(movesListCopy,opponentMovesList)         #Heuristic 12 (take a safe move: don't take a move if your opponent can move there as well)
        safeMovesList+=inBetween(unsafeMovesList,board,player,opponentTokens,playerTokens) #Heuristic 14 (in between moves are now safe)
        outsideMovesList=protectHomeRow(player,safeMovesList)                   #Heuristic 8(keep checkers in home row as long as possible)
        homeRowMovesList=moveHomeRow(player,safeMovesList)
        
        
        if safeMovesList!=[]:
            avoidCorners,safeMiddles=cornerMoves(player,outsideMovesList)
            corners,middle=cornerHomeMoves(player,homeRowMovesList)                 
            if outsideMovesList != []:
                if safeMiddles!=[]:                                 #Heuristic 16 (don't move into a corner space if you can avoid it)
                    return safeMiddles[random.randrange(0,len(safeMiddles))]
                else:
                    return avoidCorners[random.randrange(0,len(avoidCorners))]
            if homeRowMovesList!=[]:                   
                if corners!=[]:                                 #Heuristic 17 (keep middle two home row spots filled as long as possible - take a side home row move first)
                    return corners[random.randrange(0,len(corners))]
                else:
                    return middle[random.randrange(0,len(middle))]
        return unsafeMovesList[random.randrange(0,len(unsafeMovesList))]



