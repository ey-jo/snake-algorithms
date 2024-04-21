import pygame

class show:
    def get_space():
        return 180

    def show_stats(screen, x, content):
        size = 30
        font = pygame.font.SysFont('didot.ttc', size)
        vertical = 5

        screen.fill((0,0,0))
        for element in content:
            text = element[0]

            img = font.render(text, True, element[1])
            screen.blit(img, (x +5, vertical))
            vertical += size
    

    def draw_cycle(screen, x, y, CELL, color, path):

        dots = []
        for node in path:
            center = node[0] * CELL + CELL/2 + x, node[1] * CELL + CELL/2 + y

            #draw a dot in each cell
            pygame.draw.circle(screen, color, center, CELL/10)
            dots.append(center)

        #connect all dots with lines
        pygame.draw.lines(screen, color, True, dots)