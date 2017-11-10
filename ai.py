import time

class GameAI(object):
	def __init__(self, game):
		super().__init__()
		self.game = game
		self.move = (-1,-1)

	def move(self):
		# A* & Alpha-Beta Pruning

		# perform move (there must be an available move)
		self.game.performMove(self.move[0], self.move[1])