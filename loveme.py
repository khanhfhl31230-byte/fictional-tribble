import pygame
import sys
import time
import math
import random

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lyric + Pixel Butterfly")

font = pygame.font.SysFont("Arial", 40, bold=True)
clock = pygame.time.Clock()

# Lyric
lyrics = [
    ("With no makeup she a ten", 0.3, 0.8),
    ("And she the best with that head", 0.1, 0.5),
    ("Even better than Karrine", 0.25, 1),
    ("She dont want money", 0.25, 1),
    ("She want the time that we could spend", 0.25, 1.0),
]

WHITE = (255, 255, 255)

# -------- PARTICLES --------
particles = []
for _ in range(80):  # nhiều hơn, nhìn sống động
    particles.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.uniform(0.5, 2.0),  # tốc độ
        random.randint(2, 5)       # size
    ])

def draw_particles():
    for p in particles:
        p[1] -= p[2]
        if p[1] < 0:
            p[0] = random.randint(0, WIDTH)
            p[1] = HEIGHT
        pygame.draw.circle(screen, (255, 50, 50), (int(p[0]), int(p[1])), p[3])

# -------- BACKGROUND --------
def draw_background(t):
    for y in range(HEIGHT):
        base = int(20 + (y / HEIGHT) * 100)
        pulse = int(30 * (1 + math.sin(t*1.5)) / 2)
        r = min(255, base + pulse + 40)
        screen.fill((r, 0, 0), (0, y, WIDTH, 1))

# -------- PIXEL BUTTERFLY --------
def draw_pixel_butterfly(x, y, scale=8):
    # ma trận pixel (1 = vẽ)
    shape = [
        [0,1,1,0,0,0,1,1,0],
        [1,1,1,1,0,1,1,1,1],
        [1,1,1,1,0,1,1,1,1],
        [0,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,0,0,0],
    ]
    for row_i, row in enumerate(shape):
        for col_i, col in enumerate(row):
            if col == 1:
                rect = pygame.Rect(x + col_i*scale, y + row_i*scale, scale, scale)
                pygame.draw.rect(screen, (255, 0, 0), rect)
                # glow xung quanh
                pygame.draw.rect(screen, (255, 100, 100), rect.inflate(2,2), 1)

# -------- WRAP TEXT --------
def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for w in words:
        test = current + w + " "
        if font.size(test)[0] < max_width:
            current = test
        else:
            lines.append(current)
            current = w + " "
    lines.append(current)
    return lines

# -------- MAIN --------
line_index = 0
word_index = 0
last_update = time.time()

waiting = False
wait_start = 0

start_time = time.time()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.time() - start_time

    draw_background(t)
    draw_particles()
    draw_pixel_butterfly(120, HEIGHT//2 - 100, scale=8)  # bướm pixel nổi bật bên trái

    if line_index < len(lyrics):
        line, word_delay, line_delay = lyrics[line_index]
        words = line.split()

        if not waiting and time.time() - last_update > word_delay:
            word_index += 1
            last_update = time.time()

        visible = " ".join(words[:word_index])

        if word_index > len(words):
            if not waiting:
                waiting = True
                wait_start = time.time()
            if time.time() - wait_start > line_delay:
                line_index += 1
                word_index = 0
                waiting = False

        wrapped = wrap_text(visible, font, WIDTH*0.4)

        # chữ nhỏ bên phải
        y = HEIGHT//2 - len(wrapped)*font.get_height()//2
        for row in wrapped:
            text_surface = font.render(row, True, WHITE)
            rect = text_surface.get_rect(right=WIDTH - 50, y=y)
            screen.blit(text_surface, rect)
            y += font.get_height() + 10

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
