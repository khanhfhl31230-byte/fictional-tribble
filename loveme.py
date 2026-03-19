import pygame
import sys
import time
import math

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lyric + Butterfly")

font = pygame.font.SysFont("Arial", 40, bold=True)  # chữ nhỏ lại
clock = pygame.time.Clock()

lyrics = [
    ("With no makeup she a ten", 0.3, 0.8),
    ("And she the best with that head", 0.1, 0.5),
    ("Even better than Karrine", 0.25, 1),
    ("She dont want money", 0.25, 1),
    ("She want the time that we could spend", 0.25, 1.0),
]

WHITE = (255, 255, 255)

# -------- BACKGROUND --------
def draw_background():
    for y in range(HEIGHT):
        color = int(20 + (y / HEIGHT) * 120)
        pygame.draw.line(screen, (color, 0, 0), (0, y), (WIDTH, y))

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

# -------- VẼ BƯỚM --------
def draw_butterfly(t):
    x = 200 + math.sin(t * 2) * 30
    y = HEIGHT // 2 + math.sin(t * 3) * 20

    # cánh trái
    pygame.draw.ellipse(screen, (200, 0, 0), (x - 40, y - 20, 40, 30))
    pygame.draw.ellipse(screen, (255, 50, 50), (x - 35, y + 5, 35, 25))

    # cánh phải
    pygame.draw.ellipse(screen, (200, 0, 0), (x, y - 20, 40, 30))
    pygame.draw.ellipse(screen, (255, 50, 50), (x, y + 5, 35, 25))

    # thân
    pygame.draw.rect(screen, (50, 0, 0), (x - 5, y - 20, 10, 50))

# -------- MAIN --------
line_index = 0
word_index = 0
last_update = time.time()
start_time = time.time()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_background()

    t = time.time() - start_time
    draw_butterfly(t)  # vẽ bướm bên trái

    if line_index < len(lyrics):

        line, word_delay, line_delay = lyrics[line_index]
        words = line.split()

        if time.time() - last_update > word_delay:
            word_index += 1
            last_update = time.time()

        visible = " ".join(words[:word_index])

        if word_index > len(words):
            time.sleep(line_delay)
            line_index += 1
            word_index = 0

        wrapped = wrap_text(visible, font, WIDTH * 0.4)

        # căn bên phải
        y = HEIGHT // 2 - len(wrapped) * font.get_height() // 2

        for row in wrapped:
            text_surface = font.render(row, True, WHITE)
            rect = text_surface.get_rect(right=WIDTH - 50, y=y)
            screen.blit(text_surface, rect)
            y += font.get_height() + 10

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
