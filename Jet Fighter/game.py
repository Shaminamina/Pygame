import pygame, random, os, math
from pygame.locals import *

w, h = 500, 500

pygame.init()
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Jet Fighter")

fps = 60
clock = pygame.time.Clock()

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

def animation(folder, w, h):
    anime = []
    for filename in os.listdir(folder):
        frame = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
        frame = pygame.transform.scale(frame, (w, h))
        anime.append(frame)

    return anime

def run(obj):
    obj.counter += 1
    if obj.counter >= len(obj.anime) * obj.spd:
        obj.counter = 0

    return obj.counter

def collision (x, y, r, x2, y2, r2):
    #pygame.draw.circle(win, (255, 0, 0), (x, int(y)), r, 2)
    #pygame.draw.circle(win, (255, 0, 0), (x2, int(y2)), r2, 2)
    avst = math.sqrt(math.pow(y - y2, 2) + math.pow(x2 - x, 2))

    return r + r2 > avst

start_0 = False
start_1 = False
start_2 = False
def jet_choose(jet):
    if start_1 == False:
        if collision(jet.x + jet_base.w // 2, jet.y + jet_base.h // 2, jet_base.r, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10):
            jet.anime = [pygame.transform.scale(frame, (jet_base.w * 2, jet_base.h * 2)) for frame in jet.anime]
            win.blit(jet.anime[jet.counter // jet.spd], [jet.x - jet_base.w // 2, jet.y - jet_base.h // 2])
        else:
            jet.anime = [pygame.transform.scale(frame, (jet_base.w, jet_base.h)) for frame in jet.anime]
            win.blit(jet.anime[jet.counter // jet.spd], [jet.x, jet.y])
        
        return jet.anime
    else:
        jet.anime = [pygame.transform.scale(frame, (jet_base.w, jet_base.h)) for frame in jet.anime]
        win.blit(jet.anime[jet.counter // jet.spd], [jet.x, jet.y])

        return jet.anime

jet = None
jet_anime = None
jet_counter = None
def click(jet_stats):
    global jet
    global jet_anime
    global jet_counter
    global start_1
    for e in jet_stats:
        jet_rect = pygame.draw.rect(win, [255, 0, 0], (e[0].x, e[0].y, jet_base.w, jet_base.h), 1)
        if pygame.mouse.get_pressed()[0] and jet_rect.collidepoint(pygame.mouse.get_pos()):
            jet = e[0]
            jet_anime = e[1]
            jet_counter = e[2]
            start_1 = True

def update_fireball(fireball, jet, base_fireball):
    fireball.y += base_fireball.g
    
    base_fireball.g += base_fireball.g_add

    if fireball.y > h:
        fireball.x = random.randint(-base_fireball.w // 4, w - base_fireball.w // 1.5)
        fireball.y = -base_fireball.h

    if collision(jet.x + jet_base.w // 2, jet.y + jet_base.h // 2, jet_base.r2, fireball.x + base_fireball.w // 2, fireball.y + base_fireball.h // 2, base_fireball.r):
        fireball.y = -base_fireball.h
        fireball.x = random.randint(-base_fireball.w // 4, w - base_fireball.w // 1.5)
        misc.life -= base_fireball.dmg

class Misc:
    def __init__(self):
        self.life = 3
        self.points = 0
        self.point_add = 1
misc = Misc()

class Background:
    def __init__(self):
        self.w = w
        self.h = h
        self.x = 0
        self.y = 0
        self.spd = 2
        self.folder = "Jet Fighter/background"
        self.anime = animation(self.folder, self.w, self.h)
        self.counter = 0
bg = Background()

class Jet:
    def __init__(self, x, y, folder, spd):
        self.w = w // 10
        self.h = w // 10
        self.vel = w // 30
        self.r = self.w // 2
        self.r2 = self.w // 4
        self.x = x
        self.y = y
        self.folder = folder
        self.spd = spd
        self.anime = animation(self.folder, self.w, self.h)
        self.counter = 0
jet_base = Jet(None, None, "Jet Fighter/jets/jet 0", 1)
jet_0 = Jet(jet_base.w // 2, h // 2, "Jet Fighter/jets/jet 0", 1)
jet_1 = Jet(w // 2 - jet_base.w // 2, h // 2, "Jet Fighter/jets/jet 1", 1)
jet_2 = Jet(w - jet_base.w * 1.5, h // 2, "Jet Fighter/jets/jet 2", 1)
jet_3 = Jet(jet_base.w // 2, h // 4, "Jet Fighter/jets/jet 3", 1)
jet_4 = Jet(w // 2 - jet_base.w // 2, h // 4, "Jet Fighter/jets/jet 4", 1)
jet_5 = Jet(w - jet_base.w * 1.5, h // 4, "Jet Fighter/jets/jet 5", 1)

class Fireball:
    def __init__(self):
        self.w = w // 3
        self.h = w // 3
        self.dmg = 1
        self.g = 0
        self.g_add = 0.01
        self.spd = 1
        self.folder = "Jet Fighter/fireball"
        self.r = self.h // 5
        self.x = random.randint(self.w // 4, w - self.w // 1.5)
        self.y = -self.h
        self.anime = animation(self.folder, self.w, self.h)
        self.counter = 0
fireball = Fireball()
fireball_0 = Fireball()
fireball_1 = Fireball()
fireball_2 = Fireball()

class Font:
    def __init__(self):
        self.font = "Jet Fighter/font/SpaceMono-Regular.ttf"
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

def main():
    play = True

    global start_0
    global start_1
    global start_2

    trail_length = 15
    trail = []

    while play:
        clock.tick(fps)
        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                pygame.quit()
                exit(0)

        bg.counter = run(bg)
        win.blit(bg.anime[bg.counter // bg.spd], [bg.x, bg.y])

        jet_0.counter = run(jet_0)
        jet_1.counter = run(jet_1)
        jet_2.counter = run(jet_2)
        jet_3.counter = run(jet_3)
        jet_4.counter = run(jet_4)
        jet_5.counter = run(jet_5)

        text("Jet Shooter", font.color, "mid", h // 5 , font.font, 15)
        start_button = button("Click to start", h - h // 3, button_base.w, button_base.h, button_base.ic, button_base.ac, font.font, button_base.size, button_base.rgb, button_base.rgb2)
        text("Shaminamina Game Studio", font.color, "mid", h - h // 4, font.font, 5)

        if pygame.mouse.get_pressed()[0] and start_button.collidepoint(pygame.mouse.get_pos()):
            start_0 = True

        if start_0 == True:
            win.blit(bg.anime[bg.counter // bg.spd], [bg.x, bg.y])

            text("Choose your jet!", font.color, "mid", h // 20, font.font, 15)

            jet_choose(jet_0)
            jet_choose(jet_1)
            jet_choose(jet_2)
            jet_choose(jet_3)
            jet_choose(jet_4)
            jet_choose(jet_5)

            jet_stats = [
                (jet_0, jet_0.anime, jet_0.counter),
                (jet_1, jet_1.anime, jet_1.counter),
                (jet_2, jet_2.anime, jet_2.counter),
                (jet_3, jet_3.anime, jet_3.counter),
                (jet_4, jet_4.anime, jet_4.counter),
                (jet_5, jet_5.anime, jet_5.counter)
            ]

            click(jet_stats)

        if start_1 == True:
            jet.counter = run(jet)
            win.blit(bg.anime[bg.counter // bg.spd], [bg.x, bg.y])
            win.blit(jet.anime[jet.counter // jet.spd], [jet.x, jet.y])

            fireball.counter = run(fireball)
            win.blit(fireball.anime[fireball.counter // fireball.spd], [fireball_0.x, fireball_0.y])
            win.blit(fireball.anime[fireball.counter // fireball.spd], [fireball_1.x, fireball_1.y])
            win.blit(fireball.anime[fireball.counter // fireball.spd], [fireball_2.x, fireball_2.y])

            text("Life: " + str(misc.life), font.color, "right", 0, font.font, 3)
            text("Points: " + str(misc.points), font.color, "left", 0, font.font, 3)

            misc.points += misc.point_add

            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                jet.x += jet_base.vel
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                jet.x -= jet_base.vel
            if key[pygame.K_UP] or key[pygame.K_w]:
                jet.y -= jet_base.vel
            if key[pygame.K_DOWN] or key[pygame.K_s]:
                jet.y += jet_base.vel

            if jet.x < 0:
                jet.x = 0
            if jet.x > w - jet_base.w:
                jet.x = w - jet_base.w
            if jet.y < 0:
                jet.y = 0
            if jet.y > h - jet_base.h:
                jet.y = h - jet_base.h

            trail.append((jet.x, jet.y))
            if len(trail) >= trail_length:
                trail.pop(0)
            for i, (jet.x, jet.y) in enumerate(trail):
                alpha = int(255 * (i / trail_length)) // 2
                jet_surface = jet.anime[jet.counter // jet.spd].convert_alpha()
                jet_surface.set_alpha(alpha)
                win.blit(jet_surface, [jet.x, jet.y])

            update_fireball(fireball_0, jet, fireball)
            update_fireball(fireball_1, jet, fireball)
            update_fireball(fireball_2, jet, fireball)

            if misc.life <= 0:
                start_2 = True

        if start_2 == True:
            misc.point_add = 0
            jet.vel = 0
            fireball.g = 0
            win.blit(bg.anime[bg.counter // bg.spd], [bg.x, bg.y])

            text("Game Over", font.color, "mid", h // 5, font.font, 15)
            text("Points: " + str(misc.points), font.color, "mid", h // 2, font.font, 5)
            
            reset_button = button("Click to reset", h - h // 3, button_base.w, button_base.h, button_base.ic, button_base.ac, font.font, button_base.size, button_base.rgb, button_base.rgb2)

            if pygame.mouse.get_pressed()[0] and reset_button.collidepoint(pygame.mouse.get_pos()):
                misc.life = 3
                misc.points = 0
                misc.point_add = 1

                jet.vel = 15

                fireball.g = 0

                fireball_0.y = -fireball.h
                fireball_1.y = -fireball.h
                fireball_2.y = -fireball.h

                start_2 = False

                main()

        pygame.display.update()

if __name__ == "__main__":
    main()