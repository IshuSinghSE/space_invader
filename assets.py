import pygame, os, time
from pygame import mixer 

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)



pygame.init()
pygame.font.init()
mixer.init()
                                # CHECKED #
WIDTH , HEIGHT = (400,400)
WIN = pygame.display.set_mode((400,400), pygame.SCALED)#| pygame.FULLSCREEN)

line_height = HEIGHT//8
spacing = 120
scale1 = 0.5
scale2=0.3
 
# Background
BG2 = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "background-black1.png"))), (WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "background-black2.png"))), (WIDTH, HEIGHT))

clicked = mixer.Sound(resource_path("assets/music/click.wav"))

#ICON
pygame_icon = pygame.image.load(resource_path("assets/logo/icon.ico")).convert_alpha()

#button class
class Button():

	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
				mixer.Sound.play(clicked)
				time.sleep(0.5)

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
        
		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))
       
		return action
		
#LOAD SOUND FILES


sfx1 = mixer.Sound(resource_path("assets/music/hit.wav")) #enemy killed 

sfx2 = mixer.Sound(resource_path("assets/music/shoot.wav")) #shoot 

sfx3 = mixer.Sound(resource_path("assets/music/enemy_shoot.wav")) #enemy shoot

sfx4 = mixer.Sound(resource_path("assets/music/level.mp3")) #level up

sfx5 = mixer.Sound(resource_path("assets/music/live_lost.wav")) #lose lives

sfx6 = mixer.Sound(resource_path("assets/music/health_lose.wav")) #helath lose/enemy collide

sfx7 = mixer.Sound(resource_path("assets/music/game_over.wav")) #lose

muxic = mixer.Sound(resource_path("assets/music/MUXIC.wav")) #bg

sfx9 = mixer.Sound(resource_path("assets/music/won.wav")) #won

#MAIN MENU
start_img = pygame.image.load(resource_path('assets/button/start.png')).convert_alpha()
score_img = pygame.image.load(resource_path('assets/button/score.png')).convert_alpha()
option_img = pygame.image.load(resource_path('assets/button/option.png')).convert_alpha()
about_img = pygame.image.load(resource_path('assets/button/about.png')).convert_alpha()
help_img  = pygame.image.load(resource_path('assets/button/help.png')).convert_alpha()
exit_img = pygame.image.load(resource_path('assets/button/exit.png')).convert_alpha()
#create button instances
start_button = Button(WIDTH/2- start_img.get_width()/7, spacing, start_img, scale2)
score_button = Button(WIDTH/2 - score_img.get_width()/7, spacing+line_height, score_img, scale2)
option_button = Button(WIDTH/2 - option_img.get_width()/7, spacing+2*line_height, option_img,scale2)
about_button = Button(WIDTH/2 - about_img.get_width()/7+4, spacing+3*line_height-10, about_img, scale2)
help_button = Button(WIDTH-40, HEIGHT- 40, help_img,scale2-0.17)
exit_button = Button(WIDTH/2- start_img.get_width()/7, spacing + 4*line_height+5 , exit_img, scale2)


#PAUSED MENU
resume_img = pygame.image.load(resource_path('assets/button/resume.png')).convert_alpha()
retry_img = pygame.image.load(resource_path('assets/button/retry.png')).convert_alpha()
quit_img = pygame.image.load(resource_path('assets/button/quit.png')).convert_alpha()
main_menu_img = pygame.image.load(resource_path('assets/button/main_menu.png')).convert_alpha()
reset_img = pygame.image.load(resource_path('assets/button/reset.png')).convert_alpha()
yes_img = pygame.image.load(resource_path('assets/button/yes.png')).convert_alpha()
no_img = pygame.image.load(resource_path('assets/button/no.png')).convert_alpha()

resume_button = Button(WIDTH/2- start_img.get_width()/7, spacing, resume_img, scale2)
retry_button = Button(WIDTH/2 - score_img.get_width()/7, spacing+2*line_height, retry_img, scale2-0.03)
quit_button = Button(WIDTH/2- exit_img.get_width()/7, spacing + 4*line_height , quit_img, scale2)
main_menu_button = Button(WIDTH/2 - quit_img.get_width()/7, spacing+3*line_height, main_menu_img, scale2)
 
#FLOATING MENU
menu_img = pygame.image.load(resource_path('assets/button/menu.png')).convert_alpha()
highscore_img = pygame.image.load(resource_path('assets/button/highscore.png')).convert_alpha()
lives_img =pygame.transform.scale(pygame.image.load(resource_path('assets/button/lives.png')),(25,25))
level_ring=pygame.transform.scale(pygame.image.load(resource_path('assets/button/level_ring.png')),(25,25))
game_over_img = pygame.transform.scale(pygame.image.load(resource_path('assets/button/game_over.png')),(270,200))
 
 
menu_button = Button(WIDTH - menu_img.get_width()/4, HEIGHT-start_img.get_height()/3, menu_img, .2)
highscore_button = Button(WIDTH/2 - highscore_img.get_width()/10, 0, highscore_img, scale2-0.1)
shoot_button = Button(WIDTH/2 - highscore_img.get_width()/4, 0, highscore_img, scale2)
