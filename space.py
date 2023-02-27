import pygame
import os
import time
import random
import sys
import sqlite3
# import mysql.connector as mc

from assets import *
from function import *
from function import music, sound
from database import create_TB
from pygame import mixer
from pygame.locals import *
from pygame import freetype


#Initialzation
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.init()

#constants
FONT = 'comicsans'
FPS=60

version = "1.0"
SCORE = 0
lasers = []
music = True 
sound = True 

WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED|pygame.RESIZABLE)
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(pygame_icon)
 
class Laser:
    global lasers
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)
        
class Ship:
    global score, FPS
    COOLDOWN = FPS//2

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
       
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
   
    def move_lasers(self, vel, obj):
        self.cooldown()    
        for laser in self.lasers:
            laser.move(vel)           
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):            
                mixer.Sound.play(sfx6)  #helath lose
                obj.health -=10
                self.lasers.remove(laser)
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x +17, self.y, self.laser_img)          
            self.lasers.append(laser)    
            self.cool_down_counter = 1
            if len(lasers) < 100:
                lasers.append(1)
                
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
        
class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale(PLAYER_SPACE_SHIP,(WIDTH//6,HEIGHT//6))
        self.laser_img = pygame.transform.scale(PLAYER_LASER,(30,20))
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
     
          
    def move_lasers(self, vel, objs):
        global SCORE, lasers
        
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT-50):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):  
                        if sound:
                            mixer.Sound.play(sfx1) #enemy killed                    
                        objs.remove(obj)
                        self.lasers.remove(laser)                                       
                        SCORE+=10
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window,(255,0,100), (self.x, self.y + self.ship_img.get_height() - 10, self.ship_img.get_width(), 3))
        pygame.draw.rect(window, (0,255,150), (self.x, self.y + self.ship_img.get_height() - 10, self.ship_img.get_width() * (self.health/self.max_health), 3))

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                "yellow":(YELLOW_SPACE_SHIP,YELLOW_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel
                   
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+20, self.y+35, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
 
 #score saving & showing 
def save(highscores):
    conn = sqlite3.connect('SPACE.db') 
    cursor = conn.cursor() 
    cursor.execute('INSERT INTO score (RANK , PLAYER_NAME, SCORE) VALUES' + str(highscores) + ';')
    conn.commit()
    conn.close()

def load():
   conn = sqlite3.connect('SPACE.db') 
   cursor = conn.cursor()  
   cursor.execute('select PLAYER_NAME, SCORE from score order by SCORE desc limit 10;')
   b = cursor.fetchall()
   conn.close()
   return b

def reset():
    conn = sqlite3.connect('SPACE.db') 
    cursor = conn.cursor() 
    cursor.execute('DELETE FROM score;')
    conn.commit()
    conn.close()    
 
def main():
    global SCORE, lasers, FPS  
    run = True
    
    SCORE =0
    level = 0
    lives = 5
    enemies = []
    wave_length = 0
    laser_vel = 2
    player_vel = laser_vel - 1
    enemy_vel = laser_vel - 1
    spawn_distance = -1000
    shoot_rate = FPS*3

    player = Player(WIDTH//2- PLAYER_SPACE_SHIP. get_width()//6,  HEIGHT-PLAYER_SPACE_SHIP. get_height()//3)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        global SCORE, FPS
        WIN.blit(BG, (0,0))
        draw_lives(WIN,5,5,lives,lives_img)  
        main_font = pygame.font.SysFont(FONT, 20)
        level_label = main_font.render(f"Level  {level}", 1, (255,255,255))
        showScore(SCORE)
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 2))
        WIN.blit(level_ring, (WIDTH -  28, 6))
        
        ###paused ###
        if menu_button.draw(WIN):
            paused()   
              
        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)

        if lost:  
            if SCORE > 0:
                if sound:
                    mixer.Sound.play(sfx9) #Won
                won()
            else:     
                if sound:                              
                    mixer.Sound.play(sfx7) #lose
                game_over()
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        pygame.init()
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 2:
                run = False
            else:
                continue
      
        if len(enemies) == 0 :
            level += 1
            if sound:                           
                mixer.Sound.play(sfx4) #level up
            wave_length += 5
            spawn_distance -= level*500       
            laser_vel +=1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(0, WIDTH-50), random.randrange(spawn_distance, -100), random.choice(["red", "blue", "green","yellow"]))
                enemies.append(enemy)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == KEYDOWN and event.key == K_SPACE or event.type == MOUSEBUTTONDOWN:
                     if sound:                            
                         mixer.Sound.play(sfx2) #shoot 
                     player.shoot()

        
        keys = pygame.key.get_pressed()
        #left
        if keys[pygame.K_a] and player.x - player_vel > 0 : #left
            player.x -= player_vel +2
        if keys[pygame.K_LEFT] and player.x - player_vel > 0 : #left
            player.x -= player_vel +2    
        if keys[pygame.K_KP4] and player.x - player_vel > 0 : #left
            player.x -= player_vel +2 
   
        #right
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel +2
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel +2
        if keys[pygame.K_KP6] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel +2

        #up
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel +2
        if keys[pygame.K_UP] and player.y - player_vel > 0: # up
            player.y -= player_vel +2
        if keys[pygame.K_KP8] and player.y - player_vel > 0: # up
            player.y -= player_vel +2

        #down
        if keys[(pygame.K_s)] and player.y + player_vel + player.get_height()  < HEIGHT: # down
            player.y += player_vel +2
        if keys[(pygame.K_DOWN)] and player.y + player_vel + player.get_height()  < HEIGHT: # down
            player.y += player_vel +2
        if keys[(pygame.K_KP2)] and player.y + player_vel + player.get_height()  < HEIGHT: # down
            player.y += player_vel +2
            
        if keys[pygame.K_SPACE] or keys[(pygame.K_KP0)]:
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            time.sleep(.1)
            quit()
     
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, shoot_rate) == 1 and enemy.y >= -20:               
                if sound:                            
                    mixer.Sound.play(sfx3) #enemy shoot
                enemy.shoot()

            if collide(enemy, player):              
                if sound:
                    mixer.Sound.play(sfx6)  #helath lose/enemy collide
                    player.health -= 10
                enemies.remove(enemy)
                
            elif enemy.y + enemy.get_height()/2.5 > HEIGHT:      
                if sound:                 
                    mixer.Sound.play(sfx5) #lose lives
                lives -= 1
                enemies.remove(enemy)       

        player.move_lasers(-laser_vel, enemies)
        
        
def score_board():    
        run = True
        
        while run:
            WIN.blit(BG,(0,0))    
            show_score()
            highscore_button.draw(WIN)
            main_menu_button = Button(WIDTH/2 - main_menu_img.get_width()/2.5, HEIGHT - main_menu_img.get_height()/2.5, main_menu_img, .25)
            reset_button = Button(WIDTH/(2/3) - main_menu_img.get_width(), HEIGHT - reset_img.get_height()/2.9, reset_img, .24)
          
            for event in pygame.event.get():
                if main_menu_button.draw(WIN) or event.type == KEYDOWN and event.key == K_ESCAPE:
                    run = False 
                if reset_button.draw(WIN):
                    reset_prompt()
                if event.type == pygame.QUIT:
                    sys.exit()
                            
                pygame.display.update()  
                  
def reset_prompt():    
        run = True 
        while run:
            WIN.blit(BG,(0,0))   
            font = pygame.font.SysFont("consolas", 35) 
            help_ = font.render(f"RESET SCORE", 1, (255,10,25))
            WIN.blit(help_, (100,20))
            main_menu_button = Button(WIDTH/2 - main_menu_img.get_width()/8, HEIGHT - main_menu_img.get_height()/2.5, main_menu_img, .3)
           
            yes_button = Button(WIDTH/2  - no_img.get_width()/2.5, 150, yes_img, .35)
            no_button = Button(WIDTH/2  + no_img.get_width()/20, 150, no_img, .35)
            
            for event in pygame.event.get():
                if main_menu_button.draw(WIN) or event.type == KEYDOWN and event.key == K_ESCAPE:
                    run = False 
                if yes_button.draw(WIN):  
                    reset()
                    time.sleep(0.2)
                    run =  False
                if no_button.draw(WIN): 
                    run =  False
                if event.type == pygame.QUIT:
                    sys.exit()
                            
                pygame.display.update()                    
              
def paused():
        global SCORE                 
        title_font = pygame.font.SysFont(FONT, 70)
        run = True
        while run:
            WIN.blit(BG,(0,0))
            retry_button = Button(WIDTH/2 - score_img.get_width()/7, spacing+line_height, retry_img, scale2-0.03)
            for event in pygame.event.get():
                if resume_button.draw(WIN):
                        run = False 
                                
                if retry_button.draw(WIN):                    
                        run = False
                        main()
                        
                if option_button.draw(WIN):
                        option()
                
                if main_menu_button.draw(WIN):
                    if SCORE > 0:         
                    
                        won()                 
                    else:
                        game_over()  
                if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == pygame.QUIT:
                        run = False 
                        quit()
            
                pygame.display.update()     

def showScore(SCORE):
    """displays score in center of WIN"""
    scoreDigits = [int(x) for x in list(str(SCORE))]
    totalWidth = 0  # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (WIDTH - totalWidth) / 2

    for digit in scoreDigits:
        WIN.blit(IMAGES['numbers'][digit], (Xoffset, HEIGHT * 0.02))
        Xoffset += IMAGES['numbers'][digit].get_width()
       
def show_score(): 
        pygame.font.init()
        BLUE = pygame.Color('dodgerblue')
        highscores = load()
       
        title_font = pygame.font.SysFont(FONT, 20)
        header = title_font.render(" "+'RANK       NAME       SCORE', 1,BLUE)
        WIN.blit(header, (70, 70))
        count=0
        for score in highscores:
           
            rank  =  title_font.render("     "+f'{count+1}'   , 1,(255,255,225))            
            name  =  title_font.render("     "+f'{score[0]}', 1,(255,255,225)) 
            score =  title_font.render("     "+f'{score[1]}', 1,(255,255,225))
            txtRect = name.get_rect()
            txtRect.center = (WIDTH//2-15,110+count*25)
           
            count +=1        
            if count <= 10: 
                WIN.blit(rank, (60, 70+count*25))
                WIN.blit(name, txtRect)
                WIN.blit(score, (260, 70+count*25))

def game_over():         
           global SCORE
           run = True 
           while run:
                WIN.fill((0,0,0))
                lost_font = pygame.font.SysFont(FONT, 30)
                game_over = pygame.transform.scale(pygame.image.load(resource_path('assets/button/game_over.png')),(WIDTH-80,200))       
                WIN.blit(game_over, (40,0))                    
                lost_label = lost_font.render(f"Your Score: {SCORE}", 1, (255,255,255))
                WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2,line_height+spacing))
                for event in pygame.event.get():                      
                    if retry_button.draw(WIN):
                        run = False
                        main()
                       
                    if main_menu_button.draw(WIN) or (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == pygame.QUIT:         
                        run = False 
                        main_menu()
                    SCORE = 0
                    pygame.display.update()              
                
def won():
    global SCORE
    user_text="Player"
    score_key = len(load())
    color_active = pygame.Color('dodgerblue') 
    color_passive = pygame.Color("aliceblue") 
    color = color_passive                   
    input_rect = pygame.Rect(150,160,100,30)
    pygame.time.delay(100)
    flag = True 
    active = False
    while flag :
            WIN.fill((0,0,0))
            
            lost_font = pygame.font.SysFont(FONT, 25)
            warn_font =pygame.font.SysFont(FONT, 15)
            game_over = pygame.transform.scale(pygame.image.load(resource_path('assets/button/new_highscore.png')),(250,80))       
            WIN.blit(game_over, (80,50))                    
                
            warn = warn_font.render("Enter name should be 1-12 long!",1,(255,0,0))
            lost_lab = lost_font.render(f"Your Score: {SCORE}", 1, (255,255,255))
            
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                        if input_rect.collidepoint(event.pos): 
                            active = True
                        else: 
                            active = False                          
                            
                if event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]  
                            if input_rect.x <= 150:
                                input_rect.x  += 10
                        elif len(user_text) >= 12:                                  
                            WIN.blit(warn,(90,190))
                            time.sleep(1)
                            
                        else :         
                            if event.unicode not in "1234567890":     
                                user_text += event.unicode
                                if input_rect.x >= 100:
                                    input_rect.x  -= 10
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                        quit()
                if  event.type == pygame.QUIT:
                      sys.exit()
                      
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    user_text = user_text[:-1]
                    if user_text != '':
                        highscores = (score_key+1,user_text,SCORE) 
                        save(highscores)
                        flag = False 
                        main_menu() 
                    else:           
                        WIN.blit(warn,(90,190))
                        time.sleep(1)
                # pygame.display.update()     
            if active: 
                color = color_active        
                border = 2       
                pygame.key.start_text_input()
                pygame.key.set_text_input_rect(input_rect)
            else:               
                color = color_passive 
                border = 1
                pygame.key.stop_text_input()
                            
            pygame.draw.rect(WIN, color, input_rect,border,5) 
            text_surface = lost_font.render(user_text, True, ("ghostwhite")) 
            WIN.blit(text_surface, (input_rect.x+5, input_rect.y))         
            input_rect.w = max(100, text_surface.get_width()+10) 
                                  
            if retry_button.draw(WIN):
                if user_text != '':
                    highscore = (score_key+1,user_text,SCORE) 
                    save(highscore)                                           
                    flag = False 
                    main()               
                
            if main_menu_button.draw(WIN):
                if user_text != '':
                    highscores = (score_key+1,user_text,SCORE) 
                    save(highscores)
                    flag = False 
                    main_menu() 
                else:           
                    WIN.blit(warn,(90,190))
                    time.sleep(1)
            
            pygame.display.update()
            
def main_menu():
    run = True
    while run:
        WIN.blit(BG, (0,0))
        font = pygame.font.SysFont("comicsans", 14)       
        ver = font.render(f"version {version}", 1, (8,100,255))
        WIN.blit(ver, (1,HEIGHT - ver.get_height()))
        logo=pygame.transform.scale(pygame.image.load(resource_path('assets/logo/logo.png')).convert_alpha(),(280,50))
        WIN.blit(logo,(WIDTH//2 - logo.get_width()//2,HEIGHT//10))      
        
        for event in pygame.event.get():
            if start_button.draw(WIN): 
                create_TB()
                main()           
            if score_button.draw(WIN):
                create_TB()
                score_board()
            if option_button.draw(WIN):
                option()
            if about_button.draw(WIN):
                about()       	      	
            if help_button.draw(WIN):
                help()
            if exit_button.draw(WIN) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                time.sleep(0.1)
                run = False
            if event.type == pygame.QUIT:
                pygame.display.update()
                sys.exit()
            pygame.display.update()
                    
    pygame.quit()

#####Program execution #####
if __name__ == "__main__":

        main_menu()