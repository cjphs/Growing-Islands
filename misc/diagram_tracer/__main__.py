import pygame
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)

pygame.init()
 
size = (600, 600)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Tessellation tracer")
pygame.mouse.set_visible(False)
 
clock = pygame.time.Clock()

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, x, y):
        return ((self.x - x)**2 + (self.y - y)**2)**.5

points = []
regions = []

current_region = []

mouse_x = 0
mouse_y = 0

fps = 60
point_click_distance = 15

fname = "fields3"

input_image = pygame.image.load(f"./misc/diagram_tracer/{fname}.png")
 
def save_diagram(points, regions, fname="diagram.txt"):
    file = open(f"./misc/diagram_tracer/{fname}.txt", "w")

    for p in points:
        file.write(f"{(p.x - 50)/500} {(p.y - 50)/500}\n")

    for r in regions:
        for p in r:
            file.write(f"{points.index(p)} ")
        file.write("\n")

    file.close()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:

            # Create new point
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                x,y = pos[0], pos[1]
                points.append(Point(x, y))

            # Add line connections
            if event.button == 3:
                pos = pygame.mouse.get_pos()
                
                for point in points:
                    if point.distance(pos[0], pos[1]) > point_click_distance:
                        continue

                    if point in current_region[1:]:
                        continue

                    # Point is same as first point?
                    if len(current_region) > 1 and point == current_region[0]:
                        regions.append(current_region)
                        current_region = []
                        break

                    current_region.append(point)
            
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                save_diagram(points, regions, fname)
                print(f"Diagram saved to ./misc/diagram_tracer/{fname}.txt")
 
    screen.fill(WHITE)

    screen.blit(input_image, (50, 50))

    for point in points:
        col = BLACK
        if point.distance(mouse_x, mouse_y) < point_click_distance:
            col = GREEN
        pygame.draw.circle(screen, col, [point.x, point.y], 5)

    for r in regions:
        p = []
        center_x = 0
        center_y = 0
        for i in range(len(r)):
            j = (i+1) % len(r)
            pygame.draw.line(screen, BLACK, [r[i].x, r[i].y], [r[j].x, r[j].y], 2)

            p.append((r[i].x, r[i].y))

        poly_surf = pygame.Surface(size, pygame.SRCALPHA)
        poly_surf.set_alpha(64)
        pygame.draw.polygon(poly_surf, RED, tuple(p))
        screen.blit(poly_surf, (0, 0))
        

    if len(current_region) > 0:
        for i in range(len(current_region) - 1):
            pygame.draw.line(screen, RED, [current_region[i].x, current_region[i].y], [current_region[i+1].x, current_region[i+1].y], 2)
        
        pygame.draw.line(screen, YELLOW, [current_region[-1].x, current_region[-1].y], [mouse_x, mouse_y], 2)

    pygame.draw.circle(screen, BLACK, [mouse_x, mouse_y], 5, 3)
    pygame.draw.circle(screen, BLACK, [mouse_x, mouse_y], point_click_distance, 1)

    pygame.display.flip()
    clock.tick(fps)
 
pygame.quit()