import numpy as np
import sys

board = [
		[0,0,3,0,0,8,0,9,0],
		[0,5,0,0,0,0,0,0,0],
		[0,0,0,0,6,0,0,0,8],
		[2,0,0,0,0,0,0,3,0],
		[0,0,0,0,0,0,0,0,0],
		[0,6,0,0,0,0,0,0,9],
		[0,0,0,7,0,0,0,0,0],
		[0,0,6,0,0,0,4,0,0],
		[0,4,0,0,0,0,0,0,1],
		]

#a = np.matrix(board)
# def solve2(board):
# 	for x in range(9):
# 		for y in range(9):
# 			if board[x][y] == 0:
# 				for i in range(1,10):
# 					if check_valid(x,y,i,board):
# 						board[x][y] = i
# 						solve(board)
# 						board[x][y] = 0
# 				return
# 	#input("more?")

def solve(board):
	find = find_empty_pos(board)
	if not find:
		return True
	
	x, y= find
	for guess in range(1,10):
		if check_valid(x,y,guess,board):
			board[x][y] = guess
			if solve(board):
				return True
			board[x][y] = 0
	return False

def check_valid(x,y,n,board):
	for i in range(0,9):
		if int(board[x][i]) == n or int(board[i][y]) == n:
			return False
	
	#return True
	x_pos = x //3
	y_pos = y //3
	for i in range(x_pos*3,x_pos*3 + 3):
		for j in range(y_pos*3,y_pos*3 +3):
			if board[i][j] == n and (i,j) !=(x,y):
				return False
	return True


def find_empty_pos(board):
	for i in range(0,9):
		for j in range(0,9):
			if board[i][j] == 0:
				return i,j
	return None

solve(board)
print(np.matrix(board))
print("done")