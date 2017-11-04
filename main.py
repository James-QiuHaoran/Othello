import pygame;
import sys;

BLOCK_SIZE = 50
WINDOW_WIDTH = BLOCK_SIZE * 8
WINDOW_HEIGHT = BLOCK_SIZE * 8

def quitGame():
	pygame.quit()
	sys.exit()

class Game_Engine(object):
	def __init__(self):
		super().__init__()
		# TODO

	def preparation(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption('Othello')

		# set font
		self.font = pygame.font.SysFont(None, 48)

		# set images
		self.images['board'] = pygame.image.load('images/board.png')
        self.images['black'] = pygame.image.load('images/black.png')
        self.images['white'] = pygame.image.load('images/white.png')
		# TODO

	def newGame(self):
		# TODO
		pass

	def start(self):
		self.preparation()
		self.newGame()

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quitGame()
				elif event.type == pygame.KEYDOWN:
					self.keydownHandler(event)
				elif event.type == pygame.KEYUP:
					self.keyupHandler(event)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.mousedownHandler(event)
				elif event.type == pygame.MOUSEBUTTONUP:
					self.mouseupHandler(event)
				elif event.type == pygame.MOUSEMOTION:
					self.mousemoveHandler(event)
				else:
					pass
			# TODO
		# TODO
		quitGame()

	def drawText(self, text, font, surface, x, y):
		# TODO
		pass

	def drawBoard(self):
		# TODO
		pass

	# Definition of Event Handlers
	def keydownHandler(self, event):
		# TODO
		pass

	def keyupHandler(self, event):
		# TODO
		pass

	def mousedownHandler(self, event):
		# TODO
		pass

	def mouseupHandler(self, event):
		# TODO
		pass

	def mousemoveHandler(self, event):
		# TODO
		pass

if __name__ == '__main__':
	engine = Game_Engine()
	engine.start()