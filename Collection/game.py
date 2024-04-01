import pygame, os, subprocess
from pygame.locals import *

w, h = 752, 484

pygame.init()
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Collection")

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

def button(msg, x, y, w_rect, h_rect, ic, ac, font, size, rgb, rgb2):
    mouse = pygame.mouse.get_pos()

    font_size = int(min(w, h) * size / 100)
    font_final = pygame.font.SysFont(font, font_size)
    text = font_final.render(msg, True, rgb)

    if x == "mid":
        x = (w - w_rect) // 2
    elif x == "right":
        x = w - w_rect
    elif x == "left":
        x = 0

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

def split_list(input_list, chunk_size):
    split_lists = []
    current_chunk = []

    for item in input_list:
        current_chunk.append(item)
        if len(current_chunk) == chunk_size:
            split_lists.append(current_chunk)
            current_chunk = []

    if current_chunk:
        split_lists.append(current_chunk)

    return split_lists

def game(names):
    chunk_size = 5
    result = split_list(names, chunk_size)


    for i in range(len(result)):  
        for name in result[i]:
            x = button_base.w * (names.index(name) - chunk_size * i)
            y = h - h // 1.5 + button_base.h * i
            press = button(name, x, y, button_base.w, button_base.h, button_base.ic, button_base.ac, font.font, button_base.size, button_base.rgb, button_base.rgb2)
            if pygame.mouse.get_pressed()[0] and press.collidepoint(pygame.mouse.get_pos()):
                subprocess.run(["python", name + "/game.py"])

class Font:
    def __init__(self):
        self.font = "TimeNewRoman"
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

class Backround():
    def __init__(self):
        self.w = w
        self.h = h
        self.x = 0
        self.y = 0
        self.spd = 2
        self.folder = "Collection/background"

        self.anime = animation(self.folder, self.w, self.h)
        self.counter = 0
bg = Backround()

def main():
    play = True

    while play:
        clock.tick(fps)
        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                pygame.quit()
                exit(0)

        bg.counter = run(bg)
        win.blit(bg.anime[bg.counter // bg.spd], [bg.x, bg.y])

        text("Game collection", font.color, "mid", h // 5 , font.font, 15)
        text("Shaminamina Game Studio", font.color, "mid", h - h // 4, font.font, 5)

        games = []
        for filename in os.listdir("../Github"):
            games.append(filename)

        game(games)

        pygame.display.update()

if __name__ == "__main__":
    main()