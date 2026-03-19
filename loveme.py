import pygame, sys, time, random, math

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love Me - Lyric")

font = pygame.font.SysFont("Arial", 70, bold=True)
clock = pygame.time.Clock()

lyrics = [
    ("With no makeup she a ten", 0.3, 0.8, "center"),
    ("And she the best with that head", 0.1, 0.5, "center"),
    ("Even better than Karrine", 0.25, 1, "center"),
    ("She dont want money", 0.25, 1, "center"),
    ("She want the time that we could spend", 0.25, 1.0, "center"),
]

WHITE = (255,255,255)

# ---------------- BACKGROUND ----------------
def draw_background(t):
    for y in range(HEIGHT):
        base = int(30 + (y/HEIGHT)*100)

        # hiệu ứng nhịp đỏ
        pulse = int(20 * (1 + math.sin(t*2)) / 2)

        r = min(255, base + pulse + 40)
        g = 0
        b = 0

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

# ---------------- TEXT EFFECT ----------------
def draw_text_effect(text, font, x, y, alpha, scale=1.0):
    text_surface = font.render(text, True, WHITE)

    # zoom nhẹ
    size = text_surface.get_size()
    text_surface = pygame.transform.smoothscale(
        text_surface,
        (int(size[0]*scale), int(size[1]*scale))
    )

    # glow đỏ
    glow = font.render(text, True, (255, 50, 50))
    for dx in [-3, -2, -1, 1, 2, 3]:
        for dy in [-3, -2, -1, 1, 2, 3]:
            glow.set_alpha(alpha//3)
            screen.blit(glow, (x+dx, y+dy))

    text_surface.set_alpha(alpha)
    rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, rect)

# ---------------- WRAP TEXT ----------------
def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines=[]
    current=""

    for w in words:
        test=current+w+" "
        if font.size(test)[0] < max_width:
            current=test
        else:
            lines.append(current)
            current=w+" "

    lines.append(current)
    return lines

# ---------------- MAIN ----------------
line_index=0
word_index=0
last_update=time.time()

start_time = time.time()

running=True

while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    t = time.time() - start_time
    draw_background(t)

    if line_index < len(lyrics):

        line,word_delay,line_delay,align = lyrics[line_index]
        words=line.split()

        if time.time()-last_update > word_delay:
            word_index+=1
            last_update=time.time()

        visible=" ".join(words[:word_index])

        if word_index > len(words):
            time.sleep(line_delay)
            line_index+=1
            word_index=0

        wrapped=wrap_text(visible,font,WIDTH*0.8)

        y=HEIGHT//2 - len(wrapped)*font.get_height()//2

        # progress để tạo hiệu ứng
        progress = word_index / max(len(words),1)
        alpha = int(min(255, progress * 255))
        scale = 1 + 0.2*(1-progress)

        for row in wrapped:
            draw_text_effect(row, font, WIDTH//2, y, alpha, scale)
            y += font.get_height() + 10

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
