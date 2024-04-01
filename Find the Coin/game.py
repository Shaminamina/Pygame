import pygame, random, math
from pygame.locals import *

w, h = 500, 500

pygame.init()
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Find the Coin")

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
    chunk_size = int(math.sqrt(len(names)))
    result = split_list(names, chunk_size)
    i = 0
    for i in range(chunk_size):  
        for name in result[i]:
            x = button_base.w * 2 * (names.index(name) - chunk_size * i)
            y = h - h // 1.5 + button_base.h * i * 1.5
            press = button(name, x, y, button_base.w, button_base.h, button_base.ic, button_base.ac, font.font, button_base.size, button_base.rgb, button_base.rgb2)
            if pygame.mouse.get_pressed()[0] and press.collidepoint(pygame.mouse.get_pos()):
                print("hit")
        i += 1

class Font:
    def __init__(self):
        self.font = None
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

class Coin:
    def __init__(self):
        self.rgb = [255, 200, 100]
        self.r = int(37.5)
        self.x = random.choice([(100 + self.r), (200 + self.r), (300 + self.r)])
        self.y = random.choice([(100 + self.r), (200 + self.r)])
coin = Coin()

def main():
    start = False

    while True:
        clock.tick(fps)
        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                pygame.quit()
                exit(0)
                
        win.fill((0, 0, 0))

        text("Find the Coin!", font.color, "mid", h // 10, font.font, 15)

        start_button = button("Click to start", "mid", h - h // 3, button_base.w, button_base.h, button_base.ic, button_base.ac, font.font, button_base.size, button_base.rgb, button_base.rgb2)
        
        if pygame.mouse.get_pressed()[0] and start_button.collidepoint(pygame.mouse.get_pos()):
            start = True

        if start == True:
            win.fill((0, 0, 0))
            text("Find the Coin!", font.color, "mid", h // 10, font.font, 15)
            boxes = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            game(boxes)

        pygame.display.update()

if __name__ == "__main__":
    main()
