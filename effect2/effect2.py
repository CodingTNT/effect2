import pygame
import random
import math

pygame.init()


infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h  
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) 
pygame.display.set_caption("Cyberpunk Particle Effect")

keyword = "PYTHON"
colours = ['#FF007F', '#00FFFF', '#FF9900', '#9900FF', '#00FF00'] 
denseness = 10  
mouse = {'x': -100, 'y': -100}
mouseOnScreen = False


parts = []

bgCanvas = pygame.Surface((WIDTH, HEIGHT))
bgCanvas.fill((0, 10, 30))  


def draw_gradient():
    for i in range(WIDTH):
        color = pygame.Color(0)
        color.hsva = ((i * 360 // WIDTH) % 360, 100, 50)  
        pygame.draw.line(bgCanvas, color, (i, 0), (i, HEIGHT))

draw_gradient()


font = pygame.font.SysFont('impact', int(min(WIDTH * 0.7, HEIGHT) // 3)) 
text = font.render(keyword, True, (255, 255, 255)) 
bgCanvas.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))

def initialize():
    global mouseOnScreen
    screen.fill((0, 0, 0)) 

    
    pygame.mouse.set_visible(False)


def get_coords():
    for height in range(0, HEIGHT, denseness):
        for width in range(0, WIDTH, denseness):
            color = bgCanvas.get_at((width, height))
            
            if color == (255, 255, 255, 255): 
                draw_circle(width, height)


def draw_circle(x, y):
    parts.append({
        'c': random.choice(colours),
        'x': x,
        'y': y,
        'x2': x,
        'y2': y,
        'r': False,
        'v': {'x': (random.random() * 8) * 2 - 8, 'y': (random.random() * 8) * 2 - 8},  # 粒子扩散速度
    })


def update():
    global mouseOnScreen
    screen.blit(bgCanvas, (0, 0))  
    for part in parts:
        dx = part['x'] - mouse['x']
        dy = part['y'] - mouse['y']
        sqrDist = math.sqrt(dx*dx + dy*dy)
        scale = max(min(30 - (sqrDist / 8), 30), 1)  

        pygame.draw.circle(screen, part['c'], (int(part['x']), int(part['y'])), int(4 * scale))


def mouse_move(e):
    global mouseOnScreen
    if e.type == pygame.MOUSEMOTION:
        mouseOnScreen = True
        mouse['x'], mouse['y'] = e.pos

def mouse_out(e):
    global mouseOnScreen
    mouseOnScreen = False
    mouse['x'] = -100
    mouse['y'] = -100

def clear():
    screen.fill((0, 10, 30))  

def main():
    running = True
    clock = pygame.time.Clock()
    
    initialize()
    get_coords()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_move(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_out(event)

        clear()
        update()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# 运行主程序
if __name__ == "__main__":
    main()
