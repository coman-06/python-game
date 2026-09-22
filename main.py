import pygame
import time
import random
import math 

pygame.init()
pygame.mixer.init() 

display_width = 1200
display_height = 1000

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tank Rush')

black = (0, 0, 0)
white = (255, 255, 255)
menu_bg = (40, 45, 50)      
game_bg = (30, 32, 35)  

red = (180, 40, 40)
bright_red = (220, 60, 60)
green = (40, 160, 60)
bright_green = (60, 200, 80)

clock = pygame.time.Clock()

try:
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.set_volume(0.3) 
    
    crash_sound = pygame.mixer.Sound('crash.mp3')
    crash_sound.set_volume(0.8) 
except Exception as e:
    print("Audio files not found.")
    crash_sound = None

vehicleImg = pygame.image.load('tank.png').convert_alpha()
vehicle_mask = pygame.mask.from_surface(vehicleImg)
visible_rect = vehicleImg.get_bounding_rect()

vehicle_width = vehicleImg.get_width()
vehicle_height = vehicleImg.get_height()

paused = False

def objects_dodged(count):
    font = pygame.font.SysFont(None, 35) 
    shadow = font.render("Dodged: " + str(count), True, black)
    text = font.render("Dodged: " + str(count), True, white)
    display.blit(shadow, (22, 22))
    display.blit(text, (20, 20))

def draw_barricade(x, y, w, h):
    x, y, w, h = int(x), int(y), int(w), int(h)
    
    pygame.draw.rect(display, (70, 75, 80), [x, y, w, h], border_radius=10)
    
    stripe_w = w / 5
    for i in range(5):
        color = (200, 180, 0) if i % 2 == 0 else (20, 20, 20)
        pygame.draw.rect(display, color, [x + (i * stripe_w), y, stripe_w + 1, 15])
        pygame.draw.rect(display, color, [x + (i * stripe_w), y + h - 15, stripe_w + 1, 15])

    pygame.draw.rect(display, (40, 45, 50), [x + 8, y + 15, w - 16, h - 30], border_radius=5)
    
    center_x = x + w / 2
    center_y = y + h / 2
    
    pulse = int(abs(math.sin(time.time() * 6)) * 205) + 50
    
    pygame.draw.circle(display, (pulse, 30, 30), (center_x, center_y), w / 3.5)

    pygame.draw.circle(display, (255, 100, 100), (center_x, center_y), w / 6)

def vehicle(x, y):
    display.blit(vehicleImg, (x, y))

def text_obj(text, font, color=black):
    surface = font.render(text, True, color)
    return surface, surface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(display, ac, (x, y, w, h), border_radius=12)
        if click[0] == 1 and action != None:
            pygame.time.delay(150) 
            action()
    else:
        pygame.draw.rect(display, ic, (x, y, w, h), border_radius=12)

    text = pygame.font.Font("freesansbold.ttf", 30)
    surface, rect = text_obj(msg, text, white)
    rect.center = ((x + (w / 2)), (y + (h / 2)))
    display.blit(surface, rect)

def unpause():
    global paused
    paused = False
    pygame.mixer.music.unpause()

def quitgame():
    pygame.quit()
    quit()

def pause():
    global paused
    paused = True
    pygame.mixer.music.pause()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        display.fill(menu_bg)
        
        text = pygame.font.Font('freesansbold.ttf', 100)
        surface, rect = text_obj("PAUSED", text, white)
        rect.center = (display_width / 2, 300) 
        display.blit(surface, rect)

        button("Continue", 450, 450, 300, 80, green, bright_green, unpause)
        button("Quit Game", 450, 580, 300, 80, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)

def crash():
    pygame.mixer.music.stop() 
    if crash_sound:
        crash_sound.play() 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        display.fill(menu_bg)
        
        text = pygame.font.Font('freesansbold.ttf', 110)
        surface, rect = text_obj("YOU LOST!", text, bright_red)
        rect.center = (display_width / 2, 300)
        display.blit(surface, rect)

        button("Play Again", 450, 480, 300, 80, green, bright_green, game_loop)
        button("Quit Game", 450, 600, 300, 80, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        display.fill(menu_bg)
        
        text = pygame.font.Font('freesansbold.ttf', 120)
        surface, rect = text_obj("TANK RUSH", text, white)
        rect.center = (display_width / 2, 300)
        display.blit(surface, rect)

        button("START GAME", 450, 500, 300, 80, green, bright_green, game_loop)
        button("QUIT", 450, 630, 300, 80, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    pygame.mixer.music.play(-1) 
    
    x = (display_width / 2) - (vehicle_width / 2) 
    y = (display_height * 0.45)

    x_change = 0
    base_speed = 6 
    
    obj_startx = random.randrange(0, display_width - 100)
    obj_starty = -600
    obj_speed = 7
    obj_width = 100
    obj_height = 100

    bg_scroll = 0
    
    rocks = []
    for _ in range(40):
        rocks.append([
            random.randint(0, display_width), 
            random.randint(0, display_height), 
            random.randint(2, 6),
            random.randint(15, 25)
        ])

    dodged = 0
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -base_speed
                elif event.key == pygame.K_RIGHT:
                    x_change = base_speed
                elif event.key == pygame.K_p:
                    pause()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                    
        x += x_change
        
        display.fill(game_bg)
        
        bg_scroll += (obj_speed - 2) 
        if bg_scroll >= 100: 
            bg_scroll = 0
            
        for rock in rocks:
            rock[1] += (obj_speed - 1)
            if rock[1] > display_height:
                rock[0] = random.randint(0, display_width)
                rock[1] = -20
            pygame.draw.circle(display, (rock[3], rock[3], rock[3]), (rock[0], int(rock[1])), rock[2])

        for i in range(-100, display_height, 100):
            pygame.draw.rect(display, (200, 200, 200), [(display_width * 0.33), i + bg_scroll, 8, 40])
            pygame.draw.rect(display, (200, 200, 200), [(display_width * 0.66), i + bg_scroll, 8, 40])

        draw_barricade(obj_startx, obj_starty, obj_width, obj_height)
        obj_starty += obj_speed
        
        vehicle(x, y)
        objects_dodged(dodged)

        true_left_edge = x + visible_rect.x
        true_right_edge = x + visible_rect.x + visible_rect.width

        if true_left_edge < 0 or true_right_edge > display_width:
            crash()

        if obj_starty > display_height:
            obj_starty = 0 - obj_height
            obj_startx = random.randrange(0, display_width - int(obj_width))
            dodged += 1
            obj_speed += 0.5 

            obj_width += int(dodged * 1.2) 
            obj_height += int(dodged * 1.2)

        enemy_mask = pygame.mask.Mask((int(obj_width), int(obj_height)))
        enemy_mask.fill()
        
        offset_x = int(obj_startx - x)
        offset_y = int(obj_starty - y)
        
        if vehicle_mask.overlap(enemy_mask, (offset_x, offset_y)):
            crash()

        pygame.display.update()
        clock.tick(60)

game_intro()