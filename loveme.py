import pygame, sys, time, math

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lyric Simple")

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

# -------- BACKGROUND RED BLACK NHẸ --------
def draw_background(t):
    for y in range(HEIGHT):
        base = int(20 + (y/HEIGHT)*80)
        pulse = int(15 * (1 + math.sin(t*2)) / 2)

        r = min(255, base + pulse + 30)
        screen.fill((r, 0, 0), (0, y, WIDTH, 1))

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

        # fade nhẹ (mượt nhưng đơn giản)
        progress = word_index / max(len(words),1)
        alpha = int(min(255, progress * 255))

        for row in wrapped:
            text_surface = font.render(row, True, WHITE)
            text_surface.set_alpha(alpha)

            rect = text_surface.get_rect(center=(WIDTH//2, y))
            screen.blit(text_surface, rect)

            y += font.get_height() + 10

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
