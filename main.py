# Tiny Tower clone

import pygame 

# pygame initialization
pygame.init()
root = pygame.display.set_mode((350, 600))

# game variables
FPS = 60
clock = pygame.time.Clock()

display_width = 350
display_height = 600

scrollY = 0

# game classes
class Floor:
    def __init__(self, floor_number):
        self.floor_number = floor_number
        self.floor_color = (255, 255, 255)
        self.floor_width = display_width - 50
        self.floor_height = 100
        self.floor_x = 25
        self.floor_y = 500 - (self.floor_height * self.floor_number)

class ResidentialFloor(Floor):
    def __init__(self, floor_number):
        super().__init__(floor_number)
        self.floor_color = (255, 0, 0)

class CommercialFloor(Floor):
    def __init__(self, floor_number):
        super().__init__(floor_number)
        self.floor_color = (0, 255, 0)

class LobbyFloor(Floor):
    def __init__(self, floor_number):
        super().__init__(floor_number)
        self.floor_color = (0, 0, 255)

Floors = [LobbyFloor(0)]

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            scrollY += 20
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            scrollY -= 20
            if scrollY < 0:
                scrollY = 0
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Floors.append(ResidentialFloor(len(Floors)))

    # draw background
    root.fill((0, 0, 0))

    # draw floors based on scrollY
    for floor in Floors:
        pygame.draw.rect(root, floor.floor_color, (floor.floor_x, floor.floor_y + scrollY, floor.floor_width, floor.floor_height))




    # update display
    pygame.display.update()
    clock.tick(FPS)
