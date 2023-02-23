import pygame, os, time
from pygame import mixer 
from assets import *

                                # CHECKED #

#CONSTANT

music = True 
sound = True 
IMAGES = {}
FONT = "comicsans"  
               
                                 ##########  MAINS #######

def scn(image):
    return pygame.transform.scale(image,(20,24))
IMAGES['numbers'] = (scn(pygame.image.load(resource_path('assets/sprites/0.png')).convert_alpha()), scn(pygame.image.load(resource_path('assets/sprites/1.png')).convert_alpha()), scn(pygame.image.load('assets/sprites/2.png').convert_alpha()), scn(pygame.image.load('assets/sprites/3.png').convert_alpha()), scn(pygame.image.load('assets/sprites/4.png').convert_alpha()), scn(pygame.image.load('assets/sprites/5.png').convert_alpha()), scn(pygame.image.load('assets/sprites/6.png').convert_alpha()), scn(pygame.image.load('assets/sprites/7.png').convert_alpha()), scn(pygame.image.load('assets/sprites/8.png').convert_alpha()), scn(pygame.image.load('assets/sprites/9.png').convert_alpha()))


def scx(image):
    return pygame.transform.scale(image,(10,10))
    
# Load images
RED_SPACE_SHIP = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "pixel_ship_red_small.png"))),(50,50))

GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "pixel_ship_green_small.png"))),(50,50))

BLUE_SPACE_SHIP = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "pixel_ship_blue_small.png"))),(50,50))

YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "pixel_ship_yellow_small.png"))),(50,50))

# Player player
PLAYER_SPACE_SHIP = pygame.image.load(resource_path(os.path.join("assets", "pixel_ship_yellow.png")))

# Lasers
RED_LASER = scx(pygame.image.load(resource_path(os.path.join("assets", "pixel_laser_red.png"))))
GREEN_LASER = scx(pygame.image.load(resource_path(os.path.join("assets", "pixel_laser_green.png"))))
BLUE_LASER = scx(pygame.image.load(resource_path(os.path.join("assets", "pixel_laser_blue.png"))))
YELLOW_LASER = scx(pygame.image.load(resource_path(os.path.join("assets", "pixel_laser_yellow.png"))))
PLAYER_LASER = scx(pygame.image.load(resource_path(os.path.join("assets", "pixel_laser_player.png"))))


#SUB_FUNCTION

########## SCORE BOARD ##########

"""   DRAW LIVES ♡♡♡♡♡  """
def draw_lives(surface, x, y, lives, image):
    '''display ship's lives on the screen'''
    
    for i in range(lives):
        img_rect = image.get_rect()
        width = image.get_width()
        height = image.get_height()
        img_rect.x = x + image.get_width() * i
        img_rect.y = y
        surface.blit(image, img_rect)  

def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.       
       
def about():
       
        title_font = pygame.font.SysFont("consolas", 14)
        txt ="            ABOUT\n\n" \
       "Space Invader has developed to\n" \
       "entertain you. Its fun to fight\n"  \
       "those enemies coming one after\n" \
       "one while protecting yourself,\n" \
       "and beat the highscore.\n" \
       "We hope you enjoyed the game..\n\n\n\n" \
       "            -Developed by \n" \
       "             @Its___ashu.13"
       
        running= True
        while running:
            WIN.blit(BG,(0,0))
            main_menu_button = Button(WIDTH/2 - main_menu_img.get_width()/8, HEIGHT - main_menu_img. get_height()/2.5, main_menu_img,.25)
            title_label = title_font.render(txt, 1, (255,255,255))
           
            blit_text(WIN,txt,(80, 110),title_font)
            for event in pygame.event.get(): 
                if main_menu_button.draw(WIN)  or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False 
                                
                pygame.display.update()        

def help():
       
        title_font = pygame.font.SysFont("consolas", 15)
        txt ="- TO MOVE PLAYER SHIP\n\n\n\n" \
       "- TO SHOOT LASERS\n\n\n\n"  \
       "- TO SAVE SCORE\n\n\n\n" \
       "- TO GO BACK OR EXIT\n" 
       
       
        running= True
        while running:
            WIN.blit(BG,(0,0))
            main_menu_button = Button(WIDTH/2 - main_menu_img.get_width()/8, HEIGHT - main_menu_img. get_height()/2.5, main_menu_img,.25)
            title_label = title_font.render(txt, 1, (255,255,255))
            font = pygame.font.SysFont("consolas", 30)       
            help_ = font.render(f"HELP", 1, (8,100,255))
            WIN.blit(help_, (160,20))
           
          #  about=pygame.transform.scale(pygame.image.load('assets/background2.png').convert_alpha(),(WIDTH,HEIGHT))
            control=pygame.transform.scale(pygame.image.load(resource_path('assets/icon/control.png')).convert_alpha(),(100,100))
            space=pygame.transform.scale(pygame.image.load(resource_path('assets/icon/space.png')).convert_alpha(),(80,30))
            enter=pygame.transform.scale(pygame.image.load(resource_path('assets/icon/enter.png')).convert_alpha(),(80,30))
            esc=pygame.transform.scale(pygame.image.load(resource_path('assets/icon/esc.png')).convert_alpha(),(65,65))
            
           
            WIN.blit(control,(20 ,50))
            WIN.blit(space,(30 ,150))
            WIN.blit(enter,(30 ,210))
            WIN.blit(esc,(40 ,260))            

            blit_text(WIN,txt,(130, 100),title_font)
            for event in pygame.event.get(): 
                if main_menu_button.draw(WIN)  or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False 
                                
                pygame.display.update() 


def Name():   
                title_font = pygame.font.SysFont("", 40)                
                sfx_font = pygame.font.SysFont("", 30)
                
                title = title_font.render(" SETTING ", 1, ('dodgerblue'))
                WIN.blit(title, (WIDTH/2 - title.get_width()/2, 50))
                               
                music = sfx_font.render("MUSIC", 1, ('aliceblue'))
                WIN.blit(music, (WIDTH/2 - music.get_width()*1.65, spacing*1.2))            
                
                sound = sfx_font.render("SOUND", 1, ('aliceblue'))
                WIN.blit(sound, (WIDTH/2 + sound.get_width()/1.8, spacing*1.2))
               
def option():
            global music , sound        
            pygame.mixer.init()
            run = True 
            while run:                          
                WIN.blit(BG,(0,0)) 
                Name()
                mixer.set_num_channels(12)
                ############## MUSIC ########
                for event in pygame.event.get():
                    if music:                    
                        mixer.Channel(1).play(muxic, -1) #bg
                        music_on_img= pygame.image.load(resource_path('assets/icon/music_on.png'))
                        
                        music_on_button = Button(WIDTH/2- music_on_img.get_width()/5, spacing+line_height, music_on_img, scale2-.2)
                    else:                    
                        music_on_img= pygame.image.load(resource_path('assets/icon/music_off.png'))
                        
                        music_on_button = Button(WIDTH/2- music_on_img.get_width()/5, spacing+line_height, music_on_img, scale2-.2)
                        mixer.Sound.stop(muxic)                
                        if music_on_button.draw(WIN):                      
                            music = True 
                    ############## SOUND #########
                    
                    if sound:                    
                        sound_on_img= pygame.image.load(resource_path('assets/icon/sound_on.png'))
                        
                        sound_on_button = Button(WIDTH/3 + sound_on_img.get_width()/4.5, spacing+line_height, sound_on_img, scale2-.2)
                    else:                    
                        sound_on_img= pygame.image.load(resource_path('assets/icon/sound_off.png'))
                        
                        sound_on_button = Button(WIDTH/3 + sound_on_img.get_width()/4.5, spacing+line_height, sound_on_img, scale2-.2)
                        
                        mixer.Sound.stop(sfx1)    
                        mixer.Sound.stop(sfx2)
                        mixer.Sound.stop(sfx3)
                        mixer.Sound.stop(sfx4)
                        mixer.Sound.stop(sfx5)
                        mixer.Sound.stop(sfx6)
                        mixer.Sound.stop(sfx7)         
                        mixer.Sound.stop(sfx9)   
                        if sound_on_button.draw(WIN):                      
                            sound = True 
                    
                       
                if music_on_button.draw(WIN):                   
                    music = False 
                                    
                if sound_on_button.draw(WIN):                   
                    sound = False 

                if main_menu_button.draw(WIN) or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    run=False
              
                pygame.display.update()       

                                 
                                                                                                                          
