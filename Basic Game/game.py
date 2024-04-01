import pygame, random
from pygame.locals import *

pygame.init()

w, h = 500, 500
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Basic Game")

def text(msg, rgb, x, y, font, size):
    font_size = int(min(w, h) * size / 100)
    font_final = pygame.font.SysFont(font, font_size)
    text = font_final.render(msg, True, rgb)
    text_rect = text.get_rect()

    if x == "mid":
        win.blit(text, ((w - text_rect.width) // 2, y))
    elif x == "right":
        win.blit(text, (w - text_rect.width, y))
    elif x == "left":
        win.blit(text, (0, y))
    else:
        win.blit(text, (x, y))

def button(msg, y, w_rect, h_rect, ic, ac, font, size, rgb, rgb2):
    mouse = pygame.mouse.get_pos()

    font_size = int(min(w, h) * size / 100)
    font_final = pygame.font.SysFont(font, font_size)
    text = font_final.render(msg, True, rgb)

    x = (w - w_rect) // 2

    text_x = x + (w_rect // 2) - (text.get_width() // 2)
    text_y = y + (h_rect // 2) - (text.get_height() // 2)

    if x + w_rect > mouse[0] > x and y + h_rect > mouse[1] > y:
        textRect = pygame.draw.rect(win, ac, (x, y, w_rect, h_rect))
        text = font_final.render(msg, True, rgb2)
    else:
        textRect = pygame.draw.rect(win, ic, (x, y, w_rect, h_rect))
        text = font_final.render(msg, True, rgb)
    
    win.blit(text, (text_x, text_y))

    return textRect

class Font:
    def __init__(self):
        self.font = "TimesNewRoman"
        self.color = [255, 200, 100]
font = Font()

class Button:
    def __init__(self):
        self.w = w // 5
        self.h = h // 15
        self.ic = [100, 100, 100]
        self.ac = [255, 255, 255]
        self.size = 3
        self.rgb = [0, 255, 0]
        self.rgb2 = [255, 0, 0]
button_base = Button()

class Player:
    def __init__(self):
        self.x = w // 2
        self.y = h // 2
        self.w = 50
        self.h = 50
        self.rgb = [200, 0, 0]
        self.vel = 10
        self.r = 25
player = Player()

class Coin:
    def __init__(self):
        self.rgb = [255, 255, 255]
        self.r = 25
        self.x = random.randint(self.r, w - self.r)
        self.y = random.randint(self.r, h - self.r)
coin = Coin()

def main():
    fps = 60
    clock = pygame.time.Clock()

    start = False
    end = False

    countdown = 1000
    countdown_minus = 1
    point = 0

    trail_length = 15
    trail = []

    play = True

    while play:
        clock.tick(fps)
        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                pygame.quit()
                exit(0)

        win.fill([0, 0, 0])

        if start == False:
            text("Basic Game", font.color, "mid", h // 20, font.font, 15)
            press_start_button = button("Click to start", h - h // 3, button_base.w, button_base.h, button_base.ic, button_base.ac, font.font, button_base.size, button_base.rgb, button_base.rgb2)
            if pygame.mouse.get_pressed()[0] and press_start_button.collidepoint(pygame.mouse.get_pos()):
                start = True

        if start == True:
            text("Point: " + str(point), font.color, "left", 0, font.font, 5)
            text("Time: " + str(countdown), font.color, "right", 0, font.font, 5)

            trail.append((player.x, player.y))

            if len(trail) >= trail_length:
                trail.pop(0)

            for i, (player.x, player.y) in enumerate(trail):
                alpha_surface = pygame.Surface((player.w, player.h), pygame.SRCALPHA)
                alpha_surface.fill((player.rgb[0], player.rgb[1], player.rgb[2], 25))
                win.blit(alpha_surface, (player.x, player.y))

            player_rect = pygame.draw.rect(win, player.rgb, [player.x, player.y, player.w, player.h])
            coin_circle = pygame.draw.circle(win, coin.rgb, [coin.x, coin.y], coin.r)

            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                player.x += player.vel
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                player.x -= player.vel
            if key[pygame.K_UP] or key[pygame.K_w]:
                player.y -= player.vel
            if key[pygame.K_DOWN] or key[pygame.K_s]:
                player.y += player.vel

            if player.x < 0:
                player.x = 0
            if player.x > w - player.w:
                player.x = w - player.w
            if player.y < 0:
                player.y = 0
            if player.y > h - player.h:
                player.y = h - player.h

            if key[pygame.K_SPACE]:
                player.rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            if player_rect.colliderect(coin_circle):
                coin.x = random.randint(coin.r, w - coin.r)
                coin.y = random.randint(coin.r, h - coin.r)
                point += 1

            countdown -= countdown_minus

            if countdown <= 0:
                end = True

        if end == True:
            win.fill([0, 0, 0])
            
            player.vel = 0

            text("Game Over!", font.color, "mid", h // 20, font.font, 15)
            text("Final score: " + str(point), font.color, "mid", h // 2, font.font, 15)
            
            reset_button = button("Click to reset", h - h // 3, button_base.w, button_base.h, button_base.ic, button_base.ac, font.font, button_base.size, button_base.rgb, button_base.rgb2)

            if pygame.mouse.get_pressed()[0] and reset_button.collidepoint(pygame.mouse.get_pos()):
                player.vel = 5
                
                main()

        pygame.display.update()

if __name__ == "__main__":
    main()