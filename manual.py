import pygame

class manual:
    def get_input(last):
        
        pushedKey = pygame.key.get_pressed()
        if pushedKey[pygame.K_UP]:
            input = [0, -1]
        elif pushedKey[pygame.K_DOWN]:
            input = [0, 1]
        elif pushedKey[pygame.K_LEFT]:
            input = [-1, 0]
        elif pushedKey[pygame.K_RIGHT]:
            input = [1, 0]
        else:
            input = last


        return input