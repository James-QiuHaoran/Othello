import pygame;
import os;

def quitGame():
	pygame.quit()
	sys.exit()

class Game_Engine(object):
	def __init__(self):
		super().__init__()
		# TODO

	def preparation(self):
		# TODO

	def newGame(self):
		# TODO

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

	def drawBoard(self):
		# TODO

	# Definition of Event Handlers
	def keydownHandler(self, event):
		# TODO
	def keyupHandler(self, event):
		# TODO 
	def mousedownHandler(self, event):
		# TODO
	def mouseupHandler(self, event):
		# TODO
	def mousemoveHandler(self, event):
		# TODO

if __name__ == '__main__':
	engine = Game_Engine()
	engine.start()