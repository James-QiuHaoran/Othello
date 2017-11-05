import pygame;
import sys, time, math;
import othello;

BLOCK_SIZE = 50
PADDING_SIZE = 5
WINDOW_WIDTH = BLOCK_SIZE * 8
WINDOW_HEIGHT = BLOCK_SIZE * 8 + 20

class Game_Engine(object):
	def __init__(self):
		super().__init__()
		self.images = {}    # image resources
		self.keys_down = {} # records of down-keys
		
		# create game object
		self.game = othello.Othello()

	def preparation(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption('Othello')

		# set font
		self.font = pygame.font.SysFont("Helvetica", 48)

		# set images
		self.images['board'] = pygame.image.load('images/board.png')
		self.images['black'] = pygame.image.load('images/black.png')
		self.images['white'] = pygame.image.load('images/white.png')

		self.drawBoard()

	def newGame(self):
		self.game.__init__()

	def quitGame(self):
		pygame.quit()
		sys.exit()

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

	def drawText(self, text, font, screen, x, y):
		textObj = font.render(text, 1, (0,0,0))
		textRect = textObj.get_rect()
		textRect.topleft = (x, y)
		screen.blit(textObj, textRect)

	def drawBoard(self):
		# draw the board
		board = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
		self.screen.blit(self.images['board'], board)

		# draw the menu at the bottom
		menu = pygame.Rect(0, 8 * BLOCK_SIZE, WINDOW_WIDTH, 20)
		pygame.draw.rect(self.screen, (255, 255, 255), menu)
		self.menuFont = pygame.font.SysFont("comicsansms", 15)
		self.drawText("Restart", self.menuFont, self.screen, WINDOW_WIDTH / 2 - 80, 8 * BLOCK_SIZE - 1)
		self.drawText("Exit", self.menuFont, self.screen, WINDOW_WIDTH / 2 + 20, 8 * BLOCK_SIZE - 1)

		# draw blocks and tiles
		for row in range(0, 8):
			for col in range(0, 8):
				block = self.game.board[row][col]
				chessman_size = BLOCK_SIZE - 2 * PADDING_SIZE
				chessman = pygame.Rect(row * BLOCK_SIZE + PADDING_SIZE, col * BLOCK_SIZE + PADDING_SIZE, chessman_size, chessman_size)
				if block == 1:
					self.screen.blit(self.images['white'], chessman)
				elif block == 2:
					self.screen.blit(self.images['black'], chessman)
				elif block == 0:
					pass
				else:
					sys.exit('Error occurs - player number incorrect!')
		
		# game ending check
		if self.game.victory == -1:
			self.drawText("Draw!", self.font, self.screen, 95, 10)
		elif self.game.victory == 1:
			self.drawText("White Won!", self.font, self.screen, 95, 10)
		elif self.game.victory == 2:
			self.drawText("Black Won!", self.font, self.screen, 95, 10)

		# update display
		pygame.display.update()

	# Definition of Event Handlers
	def keydownHandler(self, event):
		self.keys_down[event.key] = time.time()

	def keyupHandler(self, event):
		if event.key in self.keys_down:
			del(self.keys_down[event.key])

	def mousedownHandler(self, event):
		# do not need this
		pass

	def mouseupHandler(self, event):
		x, y = event.pos

		if x >= WINDOW_WIDTH / 2 - 80 and x <= WINDOW_WIDTH / 2 - 80 + self.menuFont.size("Restart")[0] and y > 8 * BLOCK_SIZE:
			self.newGame()
		elif x >= WINDOW_WIDTH / 2 + 20 and x  <= WINDOW_WIDTH / 2 + 20 + self.menuFont.size("Exit")[0] and y > 8 * BLOCK_SIZE:
			self.quitGame()

		chessman_x = int(math.floor(x / BLOCK_SIZE))
		chessman_y = int(math.floor(y / BLOCK_SIZE))

		# TODO

	def mousemoveHandler(self, event):
		# do not need this
		pass

if __name__ == '__main__':
	engine = Game_Engine()
	engine.start()