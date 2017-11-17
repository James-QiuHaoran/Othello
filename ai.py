import time, math

class GameAI(object):
	def __init__(self, game):
		super().__init__()
		self.game = game
		self.move = (-1,-1)
		self.timelimit = 3  # 3 seconds is the time limit for search

	# AI perform move (there must be an available move due to the pre-move check)
	def move(self):
		# Iterative Deepening MiniMax Search with Alpha-Beta Pruning
		self.move = miniMax(board)

		# perform move (there must be an available move)
		self.game.performMove(self.move[0], self.move[1])

	""" Iterative Deepening MiniMax Search Algorithm within Time Limit
		From depth = 3, if still within the time limit, continue search to get more insight.
		Return the optimal move within limited resources. 
	"""
	def miniMax(self, board):
		startTime = time.time()
		timeElapsed = 0
		depth = 3
		optimalMove = (-1, -1)
		optimalBoard = board
		while timeDifference < 3:
			optimalBoard = IDMiniMax(board, 0, depth, 2, -math.inf, math.inf);
			endTime = time.time()
			timeElapsed += endTime - startTime
			startTime = endTime
			depth += 1

		for row in range(0, 8):
			for col in range(0, 8):
				if board[row][col] != optimalBoard[row][col]:
					optimalMove = (row, col)

		return optimalMove

	""" Iterative Deepening MiniMax Search with Alpha-Beta Pruning
		board - state at current node
		player - player at current node
		currentLevel - level at current node
		maxLevel - used to judge whether go deeper or not
		Return the optimal board (state) found in the current level for the current node.
	"""
	def IDMiniMax(self, board, currentLevel, maxLevel, player, alpha, beta):
		if (currentLevel == maxLevel):
			return board

		successorBoards = findSuccessorBoards(board)
		scores = []
		for idx in range(0, len(successorBoards)):
			scores.append(utility(successorBoards[idx]))

		bestBoard = None
		if player == 1:
			maxValue = -math.inf
			for idx in range(0, len(successorBoards)):
				lookaheadBoard = IDMiniMax(successorBoards[idx], currentLevel+1, maxLevel, 2, alpha, beta)
				utility = utility(lookaheadBoard)
				if utility > maxValue:
					maxValue = utility
					bestBoard = successorBoards[idx]
				alpha = math.max(alpha, utility)
				if utility >= beta:
					return lookaheadBoard  # prune
		else:
			minValue = math.inf
			for idx in range(0, len(successorBoards)):
				lookaheadBoard = IDMiniMax(successorBoards[idx], currentLevel+1, maxLevel, 1, alpha, beta)
				utility = utility(lookaheadBoard)
				if utility < minValue:
					minValue = utility
					bestBoard = successorBoards[idx]
				beta = math.min(beta, utility)
				if utility <= alpha:
					return lookaheadBoard  # prune

	# return a list of successor boards
	def findSuccessorBoards(self, board, player):
		successorBoards = []
		for row in range(0, 8):
			for col in range(0, 8):
				if self.board[row][col] == 0:
					numAvailableMoves = self.game.placePiece(row, col, player, PLAYMODE=False)
					if numAvailableMoves > 0:
						board[row][col] = player
						successorBoards.append(board)
						board[row][col] = 0
		return successorBoards

	# evaluation function for player 1 (black) or 2 (white) in this state (board)
	def utility(self, player, board):
		if player != 1 and player != 2:
			print("Error - Unknown Player!")
			raise IllegalMove("Error - Unknown Player!")
		return pieceDifference(player, board) + cornerCaptions(player, board) + cornerCloseness(player, board) + mobility(player, board) + stability(player, board)

	# piece difference when evaluating 
	def pieceDifference(self, player, board):
		allTiles = [item for sublist in board for item in sublist]
		whiteTiles = sum(1 for tile in allTiles if tile == 2)
		blackTiles = sum(1 for tile in allTiles if tile == 1)

		if whiteTiles + blackTiles == 0:
			return 0
		elif player == 1:
			if blackTiles > whiteTiles:
				return (blackTiles / (blackTiles + whiteTiles)) * 100
			else:
				return - (whiteTiles / (blackTiles + whiteTiles)) * 100
		else:
			if whiteTiles > blackTiles:
				return (whiteTiles / (blackTiles + whiteTiles)) * 100
			else:
				return - (blackTiles / (blackTiles + whiteTiles)) * 100

	# how many corners are owned by the player
	def cornerCaptions(self, player, board):
		numCorners = [0, 0]
		if board[0][0] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[0][7] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[7][0] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[7][7] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1

		if player == 1:
			return 25 * (numCorners[0] - numCorners[1])
		else:
			return 25 * (numCorners[1] - numCorners[0])

	# how many corner-closeness piece are owned by the player
	def cornerCloseness(self, player, board):
		numCorners = [0, 0]
		if board[0][1] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[1][0] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[7][1] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[6][0] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[6][7] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[7][6] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[0][6] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1
		if board[1][7] == 1:
			numCorners[0] += 1
		else:
			numCorners[1] += 1

		if player == 1:
			return 12.5 * (numCorners[0] - numCorners[1])
		else:
			return 12.5 * (numCorners[1] - numCorners[0])

	# relative mobility of a player to another (how many steps can a player move)
	def mobility(self, player, board):
		meMobility = self.game.moveCanBeMade(player)
		opponentMobility = self.game.moveCanBeMade(3 - player)

		if meMobility + opponentMobility == 0:
			return 0
		elif meMobility > opponentMobility:
			return 100 * meMobility / (meMobility + opponentMobility)
		else:
			return -100 * opponentMobility / (meMobility + opponentMobility)

	# for a piece: stable - 1; semi-stable: 0; unstable - -1
	def stability(self, player, board):
		stability = [0, 0]
		meStability, opponentStability = stability[0], stability[1]

		for row in range(1, 7):
			for col in range(1, 7):
				if (board[row-1][col-1] != 0):
					stability[player-1] += 1
				if (board[row-1][col] != 0):
					stability[player-1] += 1
				if (board[row-1][col+1] != 0):
					stability[player-1] += 1
				if (board[row+1][col-1] != 0):
					stability[player-1] += 1
				if (board[row+1][col] != 0):
					stability[player-1] += 1
				if (board[row+1][col+1] != 0):
					stability[player-1] += 1
				if (board[row][col-1] != 0):
					stability[player-1] += 1
				if (board[row][col+1] != 0):
					stability[player-1] += 1

		if player == 1:
			meStability, opponentStability = stability[0], stability[1]
		else
			meStability, opponentStability = stability[1], stability[0]

		if meStability + opponentStability == 0:
			return 0
		elif meStability > opponentStability:
			return 100 * meStability / (meStability + opponentStability)
		else:
			return -100 * opponentStability / (meStability + opponentStability)