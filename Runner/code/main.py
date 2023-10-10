import pygame,sys
from sprites import Runner,Enemy, rotate_flip
from random import choice


pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font("visuals\Super-Mario-Bros--3.ttf",25)
font_controls = pygame.font.Font("visuals\Super-Mario-Bros--3.ttf",15)
current_time = 0


def display_score():
    global current_time
    current_time = int((pygame.time.get_ticks()/100) - start_time) 
    score_display = font.render(f"score {current_time}",False,(0,0,0))
    hi_display = font.render(f"high {highscore}", False, (0,0,0))
    score_rect = score_display.get_rect(topleft = (20,50))
    hi_rect = hi_display.get_rect(topleft = (20,20))
    screen.blit(score_display,score_rect)
    screen.blit(hi_display,hi_rect)

def game_over_screen():
    title = font.render("bullets and shells",False,(255,0,0))
    title_rect = title.get_rect(center = (350,100))

    to_launch = font.render("space to begin",False,(255,0,0))
    to_launch_rect = to_launch.get_rect(center = (350,150))

    to_jump = font_controls.render("space to jump",False,(255,0,0))
    to_jump_rect = to_jump.get_rect(center = (350,300))

    to_crouch = font_controls.render("down to crouch", False, (255,0,0))
    to_crouch_rect = to_crouch.get_rect(center = (350,320))

    screen.blit(title,title_rect)
    screen.blit(to_launch,to_launch_rect)
    screen.blit(to_jump,to_jump_rect)
    screen.blit(to_crouch,to_crouch_rect)

start_time = 0
screen_width =  700
screen_height = 360
screen = pygame.display.set_mode((screen_width,screen_height))
game_active = False

fv = open("visuals\\high_score","r+")
highscore =  fv.readline()


background = pygame.image.load("visuals\\background.png").convert()
background = pygame.transform.scale2x(background)

mario = pygame.sprite.GroupSingle()
mario.add(Runner())

obstacle = pygame.sprite.Group()

timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer,900)


score = 0
scroll = 0




while True:
    
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == timer:
                obstacle.add(Enemy(choice(["shell","shell","bullet"])))
                
        if not game_active:
            if keys[pygame.K_SPACE]:
                game_active = True


    if game_active:

        if mario.sprites()[0].scrolling:
            for i in range(0,3):
                screen.blit(background,(i*1000  + scroll,0))

            scroll -= 5
            if abs(scroll) > 1000:
                scroll = 0
        else:
            for i in range(0,3):
                screen.blit(background,(i*1000  + scroll,0))
        


        obstacle.draw(screen)
        obstacle.update()

        mario.draw(screen)
        mario.update()

        display_score()

        if pygame.sprite.spritecollide(mario.sprite,obstacle,False):
            obstacle.empty()
            game_active = False

    else:   
        screen.fill((0,0,0))
        start_time = int((pygame.time.get_ticks()/100))
        game_over_screen()
        if int(current_time) > int(highscore):
        
            fv = open("visuals\\high_score","r+")
            highscore = current_time
            fv.write(f"{current_time}")
            fv.close()

    pygame.display.update()
    clock.tick(60)