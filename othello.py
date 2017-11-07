class IllegalMove(Exception):
	pass

class Othello(object):
	# 0 - Empty
	# 1 - White (Player 1)
	# 2 - Black (Player 2)

	def __init__(self):
		super().__init__()

		self.turn = 1
		self.player = 1
		self.victory = 0  # 0 - ongoing | 1 - white win | 2 - black win | -1 - draw

		self.board = [[0 for x in range(8)] for x in range(8)]
		self.board[3][3] = 1
		self.board[3][4] = 2
		self.board[4][3] = 2
		self.board[4][4] = 1

		# setup AI
		self.useAI = True
		# self.ai = ai.gameAI(self)
		
		self.hasChanged = True
		self.AIReady = False

	def playerMove(self, x, y):
		# if the game is over or not player's turn
		if self.victory != 0 or (self.useAI and self.player != 1):
			return

		self.performMove(x, y)

		# AI is ready to move
		if self.useAI:
			self.AIReady = True

	def performMove(self, x, y):
		# check whether the block has been occupied
		if self.board[x][y] != 0:
			raise IllegalMove("Block has already been occupied!")
		else:
			# place the piece and flip necessary pieces
			self.placePiece(x, y)

			# check game ending
			allTiles = [item for sublist in self.board for item in sublist]
	        emptyTiles = sum(1 for tile in allTiles if tile == 0)
	        whiteTiles = sum(1 for tile in allTiles if tile == 1)
	        blackTiles = sum(1 for tile in allTiles if tile == 2)
	        
	        # no moves left to make
	        if whiteTiles < 1 or blackTiles < 1 or emptyTiles < 1:
	            self.endGame(whiteTiles, blackTiles)
	            return
	        
	        # check available moves
	        movesFound = self.moveCanBeMade()
	        if not movesFound:
	            self.endGame(whiteTiles, blackTiles)
	            return
	        
	        # alternate between player 1 and 2
	        self.player = 3 - self.player
	        self.hasChanged = True

	def moveCanBeMade(self):
		movesFound = False
		for row in range(0, 8):
			for col in range(0, 8):
				if movesFound:
					continue
				elif self.board[row][col] == 0:
					status = self.placePiece(row, col, AUTOMODE=False)
					if status > 0:
						movesFound = True
		return movesFound

	def AIMove(self):
		pass

	def endGame(self, whiteTiles, blackTiles):
		if whiteTiles > blackTiles:
			self.victory = 1
		elif whiteTiles < blackTiles:
			self.victory = 2
		else:
			self.victory = -1
		self.hasChanged = True

	""" AUTOMODE: 
		- True for board flipping after a piece is put by the player
		- False for available moves checking
	"""
	def placePiece(self, row, col, AUTOMODE=True):
		if AUTOMODE:
			self.board[row][col] = self.player
		count = 0  # record number of flips

		# record current row and column
		__column = self.board[row]
		__row = [self.board[i][col] for i in range(0,8)]

		# check up direction
		if self.player in __column[:col]:
			pass

		# check down direction
		if self.player in __column[col:]:
			pass

		# check left direction
		if self.player in __row[:row]:
			pass

		# check right direction
		if self.player in __row[row:]:
			pass

		# check along diagonal directions