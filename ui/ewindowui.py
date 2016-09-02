import pygame, sys,os
from pygame.locals import *
os.environ['SDL_VIDEO_CENTERED'] = "center"

class eWindowUI:
	# COLORS
	GREY=(192,192,192)
	BLUE=(0,0,200)
	BLACK = (0,0,0)

	screen = None

	def __init__(self):
		pygame.init()

	def _makeScreen(self, size):
		if self.screen:
			pygame.display.quit()
		pygame.display.init()
		#size = [640, 360]
		self.screen = pygame.display.set_mode(size, pygame.NOFRAME)

	def showText(self, textStr, size=64, color=GREY):

		basicfont = pygame.font.SysFont(None, size)
		text = basicfont.render(textStr, True, color, (0,0,0))

		self._makeScreen([text.get_rect().width + 40,text.get_rect().height + 40])

		textrect = text.get_rect()

		textrect.centerx = self.screen.get_rect().centerx
		textrect.centery = self.screen.get_rect().centery

		self.screen.fill((0,0,0))
		self.screen.blit(text, textrect)

		pygame.display.update()

	def showSelectionList(self, title, list):
		titlefont = pygame.font.SysFont(None, 80)
		basicfont = pygame.font.SysFont(None, 60)

		self._makeScreen([400,600])
		self.screen.fill((0,0,0))

		text = titlefont.render(title, True, self.GREY, self.BLACK)
		textrect = text.get_rect()
		textrect.centerx = self.screen.get_rect().centerx
		textrect.centery = 40
		self.screen.blit(text, textrect)

		for idx, val in enumerate(list):
			if idx == 0:
				text = basicfont.render("   %s   " % val, True, self.GREY, self.BLUE)
			elif idx > 4:
				break
			else:
				text = basicfont.render("   %s   " % val, True, self.GREY, self.BLACK)
			textrect = text.get_rect()
			textrect.centerx = self.screen.get_rect().centerx
			textrect.centery = 100 + 64 * idx
			self.screen.blit(text, textrect)

		pygame.display.update()


	def stop(self):
		pygame.quit()
		screen = None
