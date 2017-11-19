import time, math

class GameAI(object):
	def __init__(self, game):
		super().__init__()
		self.game = game
		self.move = (-1,-1)
		self.timeLimit = 3  # 3 seconds is the time limit for search
		self.debug = False  # True for debugging

	# AI perform move (there must be an available move due to the pre-move check)
	def performMove(self):
		# Iterative Deepening MiniMax Search with Alpha-Beta Pruning
		tmpBoard = [row[:] for row in self.game.board] # we don't want to make changes to the game board
		self.move = self.miniMax(tmpBoard)

		# perform move (there must be an available move)
		self.game.performMove(self.move[0], self.move[1])

	""" Iterative Deepening MiniMax Search Algorithm within Time Limit
		From depth = 3, if still within the time limit, continue search to get more insight.
		Return the optimal move within limited resources. 
	"""
	def miniMax(self, board):
		optimalFlipping = 0
		if board[0][0] == 0:
			flippingAtCorner = self.game.placePiece(board, 0, 0, 2, PLAYMODE=False)
			if flippingAtCorner > optimalFlipping:
				optimalFlipping = flippingAtCorner
				optimalMove = (0, 0)
		if board[7][0] == 0:
			flippingAtCorner = self.game.placePiece(board, 7, 0, 2, PLAYMODE=False)
			if flippingAtCorner > optimalFlipping:
				optimalFlipping = flippingAtCorner
				optimalMove = (7, 0)
		if board[0][7] == 0:
			flippingAtCorner = self.game.placePiece(board, 0, 7, 2, PLAYMODE=False)
			if flippingAtCorner > optimalFlipping:
				optimalFlipping = flippingAtCorner
				optimalMove = (0, 7)
		if board[7][7] == 0:
			flippingAtCorner = self.game.placePiece(board, 7, 7, 2, PLAYMODE=False)
			if flippingAtCorner > optimalFlipping:
				optimalFlipping = flippingAtCorner
				optimalMove = (7, 7)
		if optimalFlipping > 0:	
			return optimalMove

		startTime = time.time()
		timeElapsed = 0
		depth = 2
		optimalMove = (-1, -1)
		optimalBoard = board
		stopDigging = False
		while not stopDigging and timeElapsed < self.timeLimit:
			(stopDigging, optimalBoard) = self.IDMiniMax(board, 0, depth, 2, -math.inf, math.inf);
			endTime = time.time()
			timeElapsed += endTime - startTime
			startTime = endTime
			depth += 1
		print("[Console MSG] Time used by AI: " + str(timeElapsed))

		for row in range(0, 8):
			for col in range(0, 8):
				if board[row][col] != optimalBoard[row][col]:
					optimalMove = (row, col)

		return optimalMove

	""" Iterative Deepening MiniMax Search with Alpha-Beta Pruning
		board - state at current node
		player - player at current node (AI - white - maximizer; Player - black - minimizer)
		currentLevel - level at current node
		maxLevel - used to judge whether go deeper or not
		Return the optimal board (state) found in the current level for the current node.
	"""
	def IDMiniMax(self, board, currentLevel, maxLevel, player, alpha, beta):
		if self.debug:
			print("Level: " + str(currentLevel) + " maxLevel: " + str(maxLevel))
		stopDigging = False
		if (not self.game.moveCanBeMade(board, player) or currentLevel == maxLevel):
			return (stopDigging, board)

		successorBoards = self.findSuccessorBoards(board, player)
		if len(successorBoards) == 0:
			stopDigging = True
			return (stopDigging, board)
		bestBoard = None

		if player == 2:
			maxValue = -math.inf
			for idx in range(0, len(successorBoards)):
				stopDigging, lookaheadBoard = self.IDMiniMax(successorBoards[idx], currentLevel+1, maxLevel, 1, alpha, beta)
				utility = self.utilityOf(lookaheadBoard)
				if utility > maxValue:
					maxValue = utility
					bestBoard = successorBoards[idx]
				alpha = max(alpha, utility)
				if utility >= beta:
					return (stopDigging, lookaheadBoard)  # prune
		else:
			minValue = math.inf
			for idx in range(0, len(successorBoards)):
				stopDigging, lookaheadBoard = self.IDMiniMax(successorBoards[idx], currentLevel+1, maxLevel, 2, alpha, beta)
				utility = self.utilityOf(lookaheadBoard)
				if utility < minValue:
					minValue = utility
					bestBoard = successorBoards[idx]
				beta = min(beta, utility)
				if utility <= alpha:
					return (stopDigging, lookaheadBoard)  # prune

		return (stopDigging, bestBoard)

	# return a list of successor boards
	def findSuccessorBoards(self, board, player):
		successorBoards = []
		for row in range(0, 8):
			for col in range(0, 8):
				if board[row][col] == 0:
					numAvailableMoves = self.game.placePiece(board, row, col, player, PLAYMODE=False)
					if numAvailableMoves > 0:
						successorBoard = [row[:] for row in board]
						successorBoard[row][col] = player
						successorBoards.append(successorBoard)
		return successorBoards

	# evaluation function (heuristics for non-final node) in this state (board)
	# AI - white | maximizer;
	# Player - black | minimizer;
	def utilityOf(self, board):
		return self.pieceDifference(board) + self.cornerCaptions(board) + self.cornerCloseness(board) + self.mobility(board) + self.stability(board)

	# piece difference when evaluating 
	def pieceDifference(self, board):
		allTiles = [item for sublist in board for item in sublist]
		whiteTiles = sum(1 for tile in allTiles if tile == 2)
		blackTiles = sum(1 for tile in allTiles if tile == 1)

		if whiteTiles > blackTiles:
			return (whiteTiles / (blackTiles + whiteTiles)) * 100
		else:
			return - (blackTiles / (blackTiles + whiteTiles)) * 100

	# how many corners are owned by each player
	def cornerCaptions(self, board):
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

		return 25 * (numCorners[1] - numCorners[0])

	# how many corner-closeness pieces are owned by each player
	def cornerCloseness(self, board):
		numCorners = [0, 0]
		for row in range(1, 7):
			if board[row][0] == 1:
				numCorners[0] += 1
			elif board[row][0] == 2:
				numCorners[1] += 1

			if board[row][7] == 1:
				numCorners[0] += 1
			elif board[row][7] == 2:
				numCorners[1] += 1

		for col in range(1, 7):
			if board[0][col] == 1:
				numCorners[0] += 1
			elif board[7][col] == 2:
				numCorners[1] += 1

			if board[row][7] == 1:
				numCorners[0] += 1
			elif board[row][7] == 2:
				numCorners[1] += 1		

		return 4 * (numCorners[1] - numCorners[0])

	# relative mobility of a player to another (how many steps can a player move)
	def mobility(self, board):
		blackMobility = self.game.moveCanBeMade(board, 1)
		whiteMobility = self.game.moveCanBeMade(board, 2)

		if blackMobility + whiteMobility == 0:
			return 0
		else:
			return 100 * whiteMobility / (whiteMobility + blackMobility)

	# for a piece: stable - 1; semi-stable: 0; instable - -1
	def stability(self, board):
		stability = [0, 0]
		blackStability, whiteStability = stability[0], stability[1]

		for row in range(1, 7):
			for col in range(1, 7):
				instabilityScale = 0
				current = board[row][col]
				if current == 0:
					continue
				if board[row+1][col+1] == 0:
					instabilityScale += 1
				if board[row-1][col-1] == 0:
					instabilityScale += 1
				if board[row+1][col] == 0:
					instabilityScale += 1
				if board[row-1][col] == 0:
					instabilityScale += 1
				if board[row+1][col-1] == 0:
					instabilityScale += 1
				if board[row-1][col+1] == 0:
					instabilityScale += 1
				if board[row][col+1] == 0:
					instabilityScale += 1
				if board[row][col-1] == 0:
					instabilityScale += 1

				if instabilityScale >= 7:
					stability[current - 1] -= 1;
				elif instabilityScale <= 3:
					stability[current - 1] += 1;

		whiteStability, blackStability = stability[1], stability[0]

		if whiteStability + blackStability == 0:
			return 0
		else:
			return 100 * whiteStability / (whiteStability + blackStability)