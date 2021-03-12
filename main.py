import math
import pygame
from pygame.math import Vector2

pygame.font.init()
pygame.mixer.init()


print('How to play:\n Player one movements: w,s,a,d\n Player one attack: q\n\n Player two movements: up,down,left,right\n Player two attack: RCTRL')
user = input('Want to play (y/n)? ')

if user == 'y':
    play = True
else:
    play = False

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255,255,0)

#font and sound
HEALTH_FONT = pygame.font.SysFont('comicsans', 40) #size 40
#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/hit.mp3')
#BULLET_SOUND = pygame.mixer.Sound('Assets/shoot.mp3')


pygame.init()
pygame.key.set_repeat(500,30)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Space Battles')
screen_rect = screen.get_rect()
    
MAX_BULLETS = 3

YELLOW_SPACESHIP = pygame.image.load('Assets/spaceship_yellow.png').convert()
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP, (73,73)), 180)
YELLOW_SPACESHIP.set_colorkey((255, 255, 255))

RED_SPACESHIP = pygame.image.load('Assets/spaceship_red.png').convert()                 
RED_SPACESHIP =  pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP, (73,73)), 180)
RED_SPACESHIP.set_colorkey((255, 255, 255))


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2



class Player(pygame.sprite.Sprite):

    def __init__(self, x,y , img):
        super(Player, self).__init__()
        self.image = pygame.Surface([20, 40], pygame.SRCALPHA)

        self.rect = pygame.Rect(100, 300, 73, 73)
        self.image = pygame.Surface((73, 73)) # 1
        self.image.blit(img, (0, 0))
        self.original_image = self.image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x,y))
        self.position = Vector2((x,y))
        # The vector points upwards.
        self.direction = Vector2(0, -1)
        self.speed = 0
        self.angle_speed = 0
        self.angle = 0

    def update(self):
        if self.angle_speed != 0:
            # Rotate the direction vector and then the image
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        # Update the position vector and the rect.
        self.position += self.direction * self.speed
        self.rect.center = self.position


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, x,y, direction, angle, color):
        """Take the pos, direction and angle of the player."""
        super(Bullet, self).__init__()
        self.image = pygame.Surface([4, 10], pygame.SRCALPHA)
        self.image.fill(color)
        # Rotate the image by the player.angle (negative since y-axis is flipped).
        self.image = pygame.transform.rotozoom(self.image, -angle, 1)
        # Pass the center of the player as the center of the bullet.rect.
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x,y))
        self.position = Vector2((x,y))  # The position vector.
        self.velocity = direction * -11  # Multiply by desired speed.

    def update(self):
        """Move the bullet."""
        self.position += self.velocity  # Update the position vector.
        self.rect.center = self.position  # And the rect.

        #if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            #self.kill()


def yellow_move(pressed, yellow):
    if pressed[pygame.K_w]: yellow.speed -= 0.5 # 6
    if pressed[pygame.K_s]: yellow.speed += 0.2 # 6

    if pressed[pygame.K_a]: yellow.angle_speed = yellow.speed / 1.5 # 7
    if pressed[pygame.K_d]: yellow.angle_speed = -yellow.speed / 1.5 # 7
    yellow.x -= yellow.speed * math.sin(math.radians(yellow.angle_speed )) # 8
    yellow.y -= yellow.speed * math.cos(math.radians(-yellow.angle_speed )) # 8

def red_move(pressed, red):
    if pressed[pygame.K_UP]: red.speed -= 0.5 # 6
    if pressed[pygame.K_DOWN]: red.speed += 0.2 # 6

    if pressed[pygame.K_LEFT]: red.angle_speed = red.speed / 1.5 # 7
    if pressed[pygame.K_RIGHT]: red.angle_speed = -red.speed / 1.5 # 7
    red.x -= red.speed * math.sin(math.radians(red.angle)) # 8
    red.y -= red.speed * math.cos(math.radians(-red.angle)) # 8


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.update()
        pygame.draw.rect(screen, YELLOW_COLOR, bullet)

        if red.rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT)) #call event
            yellow_bullets.remove(bullet)
        elif bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH or bullet.rect.y < 0 or bullet.rect.y > SCREEN_HEIGHT:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.update()
        pygame.draw.rect(screen, RED_COLOR, bullet)

        if yellow.rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH or bullet.rect.y < 0 or bullet.rect.y > SCREEN_HEIGHT:
            red_bullets.remove(bullet)


def draw_winner(text):
    WIN_FONT = pygame.font.SysFont('comicsans', 100).render(text, 1, WHITE)
    screen.blit(WIN_FONT, (SCREEN_WIDTH//2 - WIN_FONT.get_width()//2, SCREEN_HEIGHT//2 - WIN_FONT.get_height()//2))

    pygame.display.update()
    pygame.time.delay(3000)





def main():
    YELLOW = Player(100, 300, YELLOW_SPACESHIP)
    RED = Player(1100, 300, RED_SPACESHIP)

    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(YELLOW)
    all_sprites_list.add(RED)

    yellow_bullet_group = []
    red_bullet_group = []
    RED_HP = 10
    YELLOW_HP = 10

    clock = pygame.time.Clock()

    while play:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(yellow_bullet_group) < MAX_BULLETS:
                    bullet = Bullet(YELLOW.rect.centerx, YELLOW.rect.centery, YELLOW.direction, YELLOW.angle, YELLOW_COLOR)
                    yellow_bullet_group.append(bullet)
                    #BULLET_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullet_group) < MAX_BULLETS:
                    bullet = Bullet(RED.rect.centerx, RED.rect.centery, RED.direction, RED.angle, RED_COLOR)
                    red_bullet_group.append(bullet)
                    #BULLET_SOUND.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    YELLOW.angle_speed = 0
                elif event.key == pygame.K_d:
                    YELLOW.angle_speed = 0

                if event.key == pygame.K_LEFT:
                    RED.angle_speed = 0
                elif event.key == pygame.K_RIGHT:
                    RED.angle_speed = 0

            if event.type == RED_HIT:
                    RED_HP -= 1
                    #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                YELLOW_HP -= 1
                #BULLET_HIT_SOUND.play()
    
        winner = ''
        if RED_HP  <= 0:
            winner = 'Yellow Wins!'
        if YELLOW_HP <= 0:
            winner = 'Red Wins!'

        pressed = pygame.key.get_pressed()
        YELLOW.speed *= 0.9 
        RED.speed *= 0.9 

        yellow_move(pressed, YELLOW)
        red_move(pressed, RED)


        all_sprites_list.update()
        #Manage if spaceship can go off screen or not
        '''
        YELLOW.rect.clamp_ip(screen_rect)
        RED.rect.clamp_ip(screen_rect)
        '''

        screen.fill(BLACK)
        all_sprites_list.draw(screen)
        handle_bullets(yellow_bullet_group, red_bullet_group, YELLOW, RED)

        red_hp_txt = HEALTH_FONT.render('Health: ' + str(RED_HP), 1, WHITE)
        yellow_hp_txt = HEALTH_FONT.render('Health: ' + str(YELLOW_HP), 1, WHITE)
        screen.blit(red_hp_txt, (SCREEN_WIDTH-red_hp_txt.get_width() - 10, 10))
        screen.blit(yellow_hp_txt, (10, 10))

        pygame.display.flip()

        if winner:
            draw_winner(winner)
            break

    main() #game starts again


if __name__ == '__main__':
    main()