import ai

class IllegalMove(Exception):
	pass

class Othello(object):
	# 0 - Empty
	# 1 - Black (Player 1)
	# 2 - White (Player 2)

	def __init__(self):
		super().__init__()

		self.player = 1
		self.victory = 0  # 0 - ongoing | 1 - black win | 2 - white win | (-1) - draw
		self.whiteTiles = 2
		self.blackTiles = 2

		self.board = [[0 for x in range(8)] for x in range(8)]
		self.board[3][3] = 1
		self.board[3][4] = 2
		self.board[4][3] = 2
		self.board[4][4] = 1

		# set useAI = False to disable AI opponent - two-player mode
		self.useAI = False

		# set up AI - player-computer mode
		self.ai = ai.GameAI(self)
		
		self.changed = True
		self.AIReadyToMove = False

	def playerMove(self, x, y):
		# if the game is over or not player's turn
		if self.victory != 0 or (self.useAI and self.player != 1):
			return

		self.performMove(x, y)

		# AI's turn and AI is ready to move
		if self.useAI and self.player == 2:
			self.AIReadyToMove = True

	def performMove(self, x, y):
		print("Check whether move (" + str(x) + ", " + str(y) + ") is legal or not ...")
		# check whether the block has been occupied
		if self.board[x][y] != 0:
			raise IllegalMove("Block has already been occupied!")
		else:
			# place the piece and flip necessary pieces
			numFlipped = self.placePiece(x, y, self.player, PLAYMODE=True)
			print("Flipped " + str(numFlipped) + " pieces!")
			self.changed = True

			# check game ending
			allTiles = [item for sublist in self.board for item in sublist]
			emptyTiles = sum(1 for tile in allTiles if tile == 0)
			whiteTiles = sum(1 for tile in allTiles if tile == 2)
			blackTiles = sum(1 for tile in allTiles if tile == 1)
			print("empty: " + str(emptyTiles) + " white: " + str(whiteTiles) + " black: " + str(blackTiles))
			
			# no moves left to make
			if whiteTiles < 1 or blackTiles < 1 or emptyTiles < 1:
				self.endGame(whiteTiles, blackTiles)
				return
			
			# check available moves of its opponent
			movesFound = self.moveCanBeMade(3 - self.player)
			if not movesFound:
				# opponent cannot move, do not alternate
				movesFound = self.moveCanBeMade(self.player)
				if not movesFound:
					# this player cannot move either, end game
					self.endGame(whiteTiles, blackTiles)
					return
				else:
					pass
			else:
				# alternate between player 1 and 2
				self.player = 3 - self.player
				self.changed = True

	def moveCanBeMade(self, playerID):
		movesFound = False
		for row in range(0, 8):
			for col in range(0, 8):
				if movesFound:
					continue
				elif self.board[row][col] == 0:
					numAvailableMoves = self.placePiece(row, col, playerID, PLAYMODE=False)
					if numAvailableMoves > 0:
						movesFound = True
		return movesFound

	def AIMove(self):
		self.ai.move()
		self.AIReadyToMove = False

	def endGame(self, whiteTiles, blackTiles):
		if whiteTiles > blackTiles:
			self.victory = 2
		elif whiteTiles < blackTiles:
			self.victory = 1
		else:
			self.victory = -1
		self.changed = True
		self.whiteTiles = whiteTiles
		self.blackTiles = blackTiles

	""" return: the number of flips given that (row, col) will be occupied by player.
		param: PLAYMODE: 
		- True for board flipping after a piece is put by the player
		- False for available number of moves checking
	"""
	def placePiece(self, row, col, playerID, PLAYMODE=True):
		if PLAYMODE:
			self.board[row][col] = self.player
		count = 0  # record number of flips

		# record current row and column
		__column = self.board[row]
		__row = [self.board[i][col] for i in range(0,8)]

		# check up direction
		if playerID in __column[:col]:
			changes = []
			searchCompleted = False

			for i in range(col-1, -1, -1):
				if searchCompleted:
					continue
				piece = __column[i]
				if piece == 0:
					changes = []
					searchCompleted = True
				elif piece == playerID:
					searchCompleted = True
				else: 
					changes.append(i)

			# perform flippings
			if searchCompleted:
				count += len(changes)
				if PLAYMODE:
					for i in changes:
						self.board[row][i] = self.player

		# check down direction
		if playerID in __column[col:]:
			changes = []
			searchCompleted = False

			for i in range(col+1, 8, 1):
				if searchCompleted:
					continue
				piece = __column[i]
				if piece == 0:
					changes = []
					searchCompleted = True
				elif piece == playerID:
					searchCompleted = True
				else: 
					changes.append(i)

			# perform flippings
			if searchCompleted:
				count += len(changes)
				if PLAYMODE:
					for i in changes:
						self.board[row][i] = self.player

		# check left direction
		if playerID in __row[:row]:
			changes = []
			searchCompleted = False

			for i in range(row-1, -1, -1):
				if searchCompleted:
					continue
				piece = __row[i]
				if piece == 0:
					changes = []
					searchCompleted = True
				elif piece == playerID:
					searchCompleted = True
				else: 
					changes.append(i)

			# perform flippings
			if searchCompleted:
				count += len(changes)
				if PLAYMODE:
					for i in changes:
						self.board[i][col] = self.player

		# check right direction
		if playerID in __row[row:]:
			changes = []
			searchCompleted = False

			for i in range(row+1, 8, 1):
				if searchCompleted:
					continue
				piece = __row[i]
				if piece == 0:
					changes = []
					searchCompleted = True
				elif piece == playerID:
					searchCompleted = True
				else: 
					changes.append(i)

			# perform flippings
			if searchCompleted:
				count += len(changes)
				if PLAYMODE:
					for i in changes:
						self.board[i][col] = self.player

		# check along diagonal directions
		# upper-left direction
		i = 1
		ulDiagonal = []
		while row - i >= 0 and col - i >= 0:
			ulDiagonal.append(self.board[row-i][col-i])
			i += 1
		if playerID in ulDiagonal:
			changes = []
			searchCompleted = False

			for i in range(0, len(ulDiagonal)):
				piece = ulDiagonal[i]
				if searchCompleted:
					continue
				if piece == 0:
					changes = []
					searchCompleted = True
				elif piece == playerID:
					searchCompleted = True
				else: 
					changes.append((row-(i+1), col-(i+1)))

			# perform flippings
			if searchCompleted:
				count += len(changes)
				if PLAYMODE:
					for i,j in changes:
						self.board[i][j] = self.player

		# upper-right direction
		i = 1
		urDiagonal = []
		while row + i < 8 and col - i >= 0:
			urDiagonal.append(self.board[row+i][col-i])
			i += 1
		if playerID in urDiagonal:
			changes = []
			searchCompleted = False

			for i in range(0, len(urDiagonal)):
				piece = urDiagonal[i]
				if searchCompleted:
					continue
				if piece == 0:
					changes = []
					searchCompleted = True
				elif piece == playerID:
					searchCompleted = True
				else: 
					changes.append((row+(i+1), col-(i+1)))

			# perform flippings
			if searchCompleted:
				count += len(changes)
				if PLAYMODE:
					for i,j in changes:
						self.board[i][j] = self.player

		# lower-left direction
		i = 1
		llDiagonal = []
		while row - i >= 0 and col + i < 8:
			llDiagonal.append(self.board[row-i][col+i])
			i += 1
		if playerID in llDiagonal:
			changes = []
			searchCompleted = False

			for i in range(0, len(llDiagonal)):
				piece = llDiagonal[i]
				if searchCompleted:
					continue
				if piece == 0:
					changes = []
					searchCompleted = True
				elif piece == playerID:
					searchCompleted = True
				else: 
					changes.append((row-(i+1), col+(i+1)))

			# perform flippings
			if searchCompleted:
				count += len(changes)
				if PLAYMODE:
					for i,j in changes:
						self.board[i][j] = self.player

		# lower-right direction
		i = 1
		lrDiagonal = []
		while row + i < 8 and col + i < 8:
			lrDiagonal.append(self.board[row+i][col+i])
			i += 1
		if playerID in lrDiagonal:
			changes = []
			searchCompleted = False

			for i in range(0, len(lrDiagonal)):
				piece = lrDiagonal[i]
				if searchCompleted:
					continue
				if piece == 0:
					changes = []
					searchCompleted = True
				elif piece == playerID:
					searchCompleted = True
				else: 
					changes.append((row+(i+1), col+(i+1)))

			# perform flippings
			if searchCompleted:
				count += len(changes)
				if PLAYMODE:
					for i,j in changes:
						self.board[i][j] = self.player

		if count == 0 and PLAYMODE:
			self.board[row][col] = 0
			raise IllegalMove("Placing piece at (" + str(row) + ", " + str(col) + ") does not have any flips!")

		return count