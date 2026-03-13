import pygame, sys, time, random

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love Me - Lyric")

font = pygame.font.SysFont("Arial", 70, bold=True)
clock = pygame.time.Clock()

lyrics = [
    ("With no makeup she a ten", 0.3, 0.8, "center"),
    ("And she the best with that head", 0.1, 0.5, "center"),
    ("Even better than Karrine", 0.2, 0.8, "center"),
    ("She dont want money", 0.2, 0.8, "center"),
    ("She want the time that we could spend", 0.2, 1.0, "center"),
]

WHITE = (255,255,255)
BLACK = (0,0,0)


def draw_background():
    for y in range(HEIGHT):
        color = int(20 + (y/HEIGHT)*120)
        pygame.draw.line(screen,(color,color,180),(0,y),(WIDTH,y))


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


line_index=0
word_index=0
last_update=time.time()

running=True

while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    draw_background()

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

        for row in wrapped:

            text_surface=font.render(row,True,WHITE)
            rect=text_surface.get_rect(center=(WIDTH//2,y))

            screen.blit(text_surface,rect)
            y+=font.get_height()+10

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
