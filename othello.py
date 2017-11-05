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
		# TODO

	def playerMove(self, x, y):
		pass

	def performMove(self, x, y):
		pass

	def moveCanBeMade(self):
		pass

	def aiMove(self):
		pass

	def endGame(self):
		pass

	def placePiece(self, x, y, live_mode=True):
		pass