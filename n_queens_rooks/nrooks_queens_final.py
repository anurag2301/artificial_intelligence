# nrooks_queens_final.py : Solve the N-Rooks-Queens problem!
# Anurag K. Jain, August 2016
# Anurag Kumar Jain		jainanur@iu.edu		812-369-0624
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

# The N-queens problem is: Given an empty NxN chessboard, place N queens on the board so that no queens
# can take any other

# This is N, the size of the board.
N = 20

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] )

# check if pieces is present in a row, if even one piece is present in the asked row return 1, as there can't be more than 1 in a row for the optimized solution
def modified_count_on_row(board, row):
    for col in range(0,N):
        if board[row][col] == 1:
            return 1
    return 0

# check if pieces is present in a row, if even one piece is present in the asked column return 1, as there can't be more than 1 in a row for the optimized solution
def modified_count_on_col(board, col):
    for row in range(0,N):
        if board[row][col] == 1:
            return 1
    return 0

# Modified count pieces takes benefit of the fact that if rth row has no queen\rook placed than rows after than will never have queen\rook placed on it and if xth row have a queen\rook than all rows before that will have a queen\rook. 
# So, we just need to check the last row where queen\rook is present and we have our count. The for loop runs in reverse to take the benifit
def modified_count_pieces(board):
    count = N
    while count>0:
        current_row = modified_count_on_row(board, count - 1)
        if current_row == 0:
            return 0
        count -= 1
    return count

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "Q" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

# modified version of is_goal(modified_is_goal) is used with this function. This funtion checks if the current board already has N rooks than return[]. 
# Also while calling add_piece for adding a rook at pos r,c, it makes sure that a rook is not already present at that position(board[r][c])
def successors2(board):
    no_of_queens_rooks = count_pieces(board)
    if no_of_queens_rooks == N:
        return []
    result = []
    for r in range(0, N):
        for c in range(0,N):
            if board[r][c]==0:
                result += [add_piece(board, r, c)]
    return result

# successor knows that it can't have a board with already N rooks(as any board returned by this func with N rooks is a solution)
# while adding a rook at pos r,c it checks if the rth row or the cth column already have a rook on it, if so skip that add_piece call for that row/col
def successors3(board):
    #no_of_queens_rooks = modified_count_pieces(board)
    #if no_of_queens_rooks == N:                            #not required as every board with N rooks is a solution if successor3 is used and is_goal would have already returned the result
    #    return []
    result = []
    for r in range(0, N):
        # we don't want to add rook in a row where a rook already exists
        if modified_count_on_row(board, r) == 1:
            continue
        for c in range(0,N):
            # we don't want to add rook in a column where a rook already exists
            if modified_count_on_col(board, c) == 1:
                continue
            result += [add_piece(board, r, c)]
        break												#we just wanna add queens to the one row
    return result

# successor knows that it can't have a board with already N queens(as any board returned by this func with N queens is a solution)
# while adding a queen at pos r,c it checks if the rth row or the cth column already have a queen on it, if so skip that add_piece call for that row/col
# while adding a queen the func also checks if the queen which we are adding attacks any other queen on the current board, if so don't add that queen
def nqueens_successors(board):
    #no_of_queens_rooks = count_pieces(board)
    #if no_of_queens_rooks == N:                            #not required as every board with N rooks is a solution if successor3 is used
    #return []
    result = []
    for r in range(0, N):
        # we don't want to add queen in a row where a queen already exists
        if count_on_row(board, r) == 1:
            continue
        for c in range(0,N):
            # we don't want to add queen in a column where a queen already exists
            if count_on_col(board, c) == 1:
                continue
            #if board[r][c]==0:                            #not required, already checking if row has a queen on it, so this will be redundant
            #checking if we add a queen at r,c then it shouldn't attack any other queen on the board. If it is attacking one, the board will never result to a solution so we don't wanna add that to the list of boards
            if is_goal_queen(add_piece(board, r, c)):
                result += [add_piece(board, r, c)]
        break												 #we just wanna add queens to the one row
    return result

# a function for trial and error, not used in final code
def successors_trial(board):
    no_of_queens_rooks = modified_count_pieces(board)
    if no_of_queens_rooks == N:
        return []
    result = []
    for r in range(0, N):
        if modified_count_on_row(board, r) == 1:
            continue
        for c in range(0,N):
            if modified_count_on_col(board, c) == 1:
                continue
            result += [add_piece(board, r, c)]
        break
    return result

# a function for trial and error, not used in final code
def nqueens_successors_trial(board):
    no_of_queens_rooks = modified_count_pieces(board)
    if no_of_queens_rooks == N:
        return []
    result = []
    for r in range(0, N):
        if count_on_row(board, r) == 1:
            continue
        for c in range(0,N):
            if count_on_col(board, c) == 1:
                continue
            if board[r][c]==0:
                if is_goal_queen(add_piece(board, r, c)):
                    result += [add_piece(board, r, c)]
    return result

# Checking if the queen at the last row is attacking any other queen on the board or not. 
# We are not checking other queens than the last one, as we would have already checked that earlier while succesor_queen added the queen to the board. 
# So we know when we get a board only last added queen can attack the existing ones


#Used logic given in Fundamentals of Computer Algorithms 1st Edition
#by E. Horowitz (Author), S. Sahni (Author) to check diagonals which I studied in 2nd year
def is_goal_queen(board):
    # we just need to check diagonals of the queen on the last row as the board is already checked for queens on the same row/column
    
    #creating a list on queens on board
    queens_on_board = []
    queen = []
    for r in range(0,N):
        for c in range(0,N):
            if board[r][c]==1:
                queens_on_board.append([r,c])
                break
   
   # while(len(queens)>1):                      #no need to run this for all queens as we already have it checked for all queens except last one
    queen = queens_on_board.pop()
    
    #diagonal check for queen on bottom-most row of the current board
    for pos in queens_on_board:
        if(abs(queen[0]-pos[0]) == abs(queen[1]-pos[1])):
            return False
    return True

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# check if board is a goal state
def modified_is_goal(board):
    return modified_count_on_row(board, N-1) == 1 #and \
        #all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        #all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    #count = 1
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if modified_is_goal(s):
                
                #print all results-uncomment count = 1
            	"""print "\n"+ str(count) + "\n" + printable_board(s)
            	count += 1
            	continue"""

            	#return result
            	return s
            fringe.append(s)
    return False

# Solve n-queens!
def nqueens_solve(initial_board):
    fringe = [initial_board]
    #count = 1
    while len(fringe) > 0:
        for s in nqueens_successors( fringe.pop() ):
            if modified_is_goal(s):
                
                #print all results-uncomment count = 1
                """print "\n"+ str(count) + "\n" + printable_board(s)
                count += 1
                continue"""

                #return result
                return s
               
            fringe.append(s)
    return False

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
#start_time =  time.time()
#print time.asctime( time.localtime(time.time()) )
initial_board = [[0]*N]*N
print "Starting from initial board:\n" + printable_board(initial_board) 
#ifTrue:
#if int(sys.argv[2])==0:
print "\n\nLooking for n rooks solution...\n"
solution = solve(initial_board)
print printable_board(solution) if solution else "Sorry, no solution found. :("
#print "\n\n" + time.asctime( time.localtime(time.time()) )
#if int(sys.argv[2])==1:
#if False:
print "\n\nLooking for n queen solution...\n"
solution = nqueens_solve(initial_board)
print printable_board(solution) if solution else "Sorry, no solution found. :("
#end_time =  time.time()
#print time.asctime( time.localtime(time.time()) )
#print "Total time: " + str(end_time-start_time)