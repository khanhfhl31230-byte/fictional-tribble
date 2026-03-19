import pygame, sys, time, math

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love Me - Lyric")

font = pygame.font.SysFont("Arial", 70, bold=True)
clock = pygame.time.Clock()

lyrics = [
    ("With no makeup she a ten", 0.3, 0.8),
    ("And she the best with that head", 0.1, 0.5),
    ("Even better than Karrine", 0.25, 1),
    ("She dont want money", 0.25, 1),
    ("She want the time that we could spend", 0.25, 1.0),
]

WHITE = (255,255,255)

# -------- BACKGROUND (RED BLACK + PULSE) --------
def draw_background(t):
    for y in range(HEIGHT):
        base = int(20 + (y/HEIGHT)*100)
        pulse = int(30 * (1 + math.sin(t*2)) / 2)

        r = min(255, base + pulse + 40)
        screen.fill((r, 0, 0), (0, y, WIDTH, 1))

# -------- TEXT CACHE (TRÁNH LAG) --------
text_cache = {}

def get_text_surface(text):
    if text not in text_cache:
        base = font.render(text, True, WHITE)
        glow = font.render(text, True, (255, 60, 60))
        text_cache[text] = (base, glow)
    return text_cache[text]

# -------- DRAW TEXT (MƯỢT) --------
def draw_text(text, x, y, alpha, scale):
    base, glow = get_text_surface(text)

    # scale nhẹ nhưng đã cache → không lag
    if scale != 1:
        size = base.get_size()
        base_scaled = pygame.transform.smoothscale(
            base, (int(size[0]*scale), int(size[1]*scale))
        )
        glow_scaled = pygame.transform.smoothscale(
            glow, (int(size[0]*scale), int(size[1]*scale))
        )
    else:
        base_scaled = base
        glow_scaled = glow

    # glow nhẹ (ít draw → mượt)
    glow_scaled.set_alpha(alpha//4)
    rect = glow_scaled.get_rect(center=(x, y))
    screen.blit(glow_scaled, rect.move(-2,-2))
    screen.blit(glow_scaled, rect.move(2,2))

    # chữ chính
    base_scaled.set_alpha(alpha)
    rect = base_scaled.get_rect(center=(x, y))
    screen.blit(base_scaled, rect)

# -------- WRAP TEXT --------
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

# -------- MAIN --------
line_index=0
word_index=0
last_update=time.time()
start_time=time.time()

running=True

while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    t = time.time() - start_time
    draw_background(t)

    if line_index < len(lyrics):

        line, word_delay, line_delay = lyrics[line_index]
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

        # hiệu ứng mượt
        progress = word_index / max(len(words),1)
        alpha = int(min(255, progress * 255))

        # zoom mượt (không giật)
        scale = 1 + 0.15 * (1 - progress)

        for row in wrapped:
            draw_text(row, WIDTH//2, y, alpha, scale)
            y += font.get_height() + 10

    pygame.display.flip()
    clock.tick(75)

pygame.quit()
sys.exit()
