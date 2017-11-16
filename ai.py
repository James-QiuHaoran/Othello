import time

class GameAI(object):
	def __init__(self, game):
		super().__init__()
		self.game = game
		self.move = (-1,-1)
		self.timelimit = 3  # 3 seconds is the time limit for search

	def move(self):
		# Iterative Deepening MiniMax Search with Alpha-Beta Pruning

		# perform move (there must be an available move)
		self.game.performMove(self.move[0], self.move[1])

	# evaluation function for player 1 (black) or 2 (white) in this state (board)
	def evaluation(self, player, board):
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