class GameError(Exception):
	pass

class IllegalMove(GameError):
	pass

class GameRuleError(GameError):
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
		
		self.has_changed = True
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
	            self.endGame()
	            return
	        
	        # check available moves
	        movesFound = self.moveCanBeMade()
	        if not movesFound:
	            self.endGame()
	            return
	        
	        # alternate between player 1 and 2
	        self.player = 3 - self.player
	        self.has_changed = True

	def moveCanBeMade(self):
		pass

	def AIMove(self):
		pass

	def endGame(self):
		pass

	def placePiece(self, x, y, live_mode=True):
		pass