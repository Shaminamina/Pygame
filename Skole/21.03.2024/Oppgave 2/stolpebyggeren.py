import pygame, sys, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()

w, h = 800, 500

win = pygame.display.set_mode((w, h))

pygame.display.set_caption("Stolpebyggeren")

fps = 30
clock = pygame.time.Clock()

class Stolpebyggeren():
    def __init__(self):
        self.body = pygame.image.load("21.03.2024\Oppgave 2\player_stand.png")
        self.w = 68
        self.h = 84
        self.x = w // 2 - self.w // 2
        self.y = h - self.h
        self.body = pygame.transform.scale(self.body, (self.w, self.h))
        self.body = pygame.transform.flip(self.body, False, False)
        self.liv = 3
        self.vel = 10
player = Stolpebyggeren()

class Stolpestykker():
    def __init__(self, w, h, x, g, rgb):
        self.w = w
        self.h = h
        self.x = x
        self.y = 0
        self.g = g
        self.rgb = rgb
        self.rotate = 0

        self.win = pygame.Surface((self.w, self.h))
        self.win.fill(self.rgb)

    def faller(self):
        a = pygame.draw.rect(win, self.rgb, (self.x, self.y, self.w, self.h), 1)
        rotated_surface = pygame.transform.rotate(self.win, self.rotate)
        win.blit(rotated_surface, (self.x, self.y))

        self.y += self.g

        if self.y >= h:
            self.y = 0
            player.liv -= 1

        return a

stolpestykker1 = Stolpestykker(100, 50, w // 4, 3, (255, 0, 0))
stolpestykker2 = Stolpestykker(50, 50, w - w // 4, 2, (0, 255, 0))

hovedstolpe = []

random_pos = random.randint(0 + 50, w - 50)

def collision(player_rect, stolpe):
    global hovedstolpe
    global random_pos
    grense2 = hoved()
    if player_rect.colliderect(stolpe.faller()):
        stolpe.g = 0
        stolpe.rotate = 90
        stolpe.x = w - stolpe.h
        stolpe.y = grense2 - stolpe.w
        hovedstolpe.append(stolpe)
        random_pos = random.randint(0 + 50, w - 50)

def hoved():
    global hovedstolpe
    grense = h
    for e in hovedstolpe:
        q = Stolpestykker(e.w, e.h, random_pos, e.g, e.rgb)
        q.faller()
        grense -= e.w

    return grense

def main():
    play = True
    over = False

    font_final = pygame.font.Font(None, h)

    while play:
        global hovedstolpe

        clock.tick(fps)
        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        win.fill((200, 200, 200))
        text = font_final.render(str(player.liv), True, (0, 0, 0))
        player_rect = pygame.draw.rect(win, (0, 0, 0), (player.x, player.y, player.w, player.h), 1)
        win.blit(text, (w // 2 - text.get_width() // 2, h // 2 - text.get_height() // 2))
        win.blit(player.body, (player.x, player.y))
        
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            player.x += player.vel
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            player.x -= player.vel

        stolpestykker1.faller()
        stolpestykker2.faller()

        collision(player_rect, stolpestykker1)
        collision(player_rect, stolpestykker2)

        hoved()

        if player.liv == 0:
            over = True

        if over:
            pass

        pygame.display.flip()

if __name__ == "__main__":
    main()
