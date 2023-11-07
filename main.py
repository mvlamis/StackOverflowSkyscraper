# Stack Overflow Skyscraper
# Tiny Tower clone by Michael Vlamis

import pygame 

# pygame initialization
pygame.init()
root = pygame.display.set_mode((350, 600))
pygame.display.set_caption("Stack Overflow Skyscraper")

# game variables
FPS = 60
clock = pygame.time.Clock()

display_width = 350
display_height = 600

scrollY = 0

font = pygame.font.SysFont("Arial", 20)
        
# game variables
money = 100000

showFloorButtons = False

# ui classes 
class Button:
    def __init__(self, x, y, width, height, color = None, text = None, bgImage = None):
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.bgImage = bgImage

    def draw(self, root):
        text = font.render(self.text, True, (0, 0, 0))
        if self.bgImage != None:
            root.blit(self.bgImage, (self.x, self.y))
        else:
            pygame.draw.rect(root, self.color, (self.x, self.y, self.width, self.height))
            root.blit(text, (self.x + 10, self.y + 10))

    def is_clicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


buttons = [
    Button(0, 0, display_width, 50, (200, 200, 200), "Menu", pygame.image.load("images/topbar.png")),
    Button(290, 0, 50, 50, color = None, text = "+", bgImage=pygame.image.load("images/plus.png")),
]

floorButtons = [
    Button(75, 200, 200, 50, (255, 0, 0), "Residential"),
    Button(75, 260, 200, 50, (0, 255, 0), "Commercial"),
    Button(75, 140, 50, 50, (255, 255, 255), "X")
]

# game classes
class Floor:
    def __init__(self, floor_number, image = None):
        self.floor_number = floor_number
        self.floor_color = (255, 255, 255)
        self.floor_width = display_width - 50
        self.floor_height = 100
        self.floor_x = 25
        self.floor_y = 500 - (self.floor_height * self.floor_number)
        self.image = image

class ResidentialFloor(Floor):
    def __init__(self, floor_number):
        super().__init__(floor_number)
        self.floor_color = (255, 0, 0)
        self.occupants = []

class CommercialFloor(Floor):
    def __init__(self, floor_number):
        super().__init__(floor_number)
        self.floor_color = (0, 255, 0)
        self.employees = []

class LobbyFloor(Floor):
    def __init__(self, floor_number):
        super().__init__(floor_number)
        self.floor_color = (0, 0, 255)

class Citizen:
    def __init__(self, name, jobFloor, homeFloor):
        self.name = name
        self.jobFloor = jobFloor
        self.homeFloor = homeFloor

Floors = [LobbyFloor(0), ResidentialFloor(1), CommercialFloor(2)]
Citizens = [Citizen("Michael", 1, 2)]

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scrollY += 20
            if event.button == 5:
                scrollY -= 20
                if scrollY < 0:
                    scrollY = 0

            if event.button == 1:
                pos = pygame.mouse.get_pos()
                for button in range(len(buttons)):
                    if buttons[button].is_clicked(pos):
                        if button == 1:
                            showFloorButtons = True
                
                if showFloorButtons:
                    for button in range(len(floorButtons)):
                        if floorButtons[button].is_clicked(pos):
                            if button == 0:
                                Floors.append(ResidentialFloor(len(Floors)))
                            if button == 1:
                                Floors.append(CommercialFloor(len(Floors)))
                            if button == 2:
                                showFloorButtons = False
                            showFloorButtons = False

    # blit background image based on scrollY
    root.fill((255, 255, 255))
    root.blit(pygame.image.load("images/Background-day.jpeg"), (0, scrollY / 10 - 4150))


    # draw floors based on scrollY
    for floor in Floors:
        pygame.draw.rect(root, floor.floor_color, (floor.floor_x, floor.floor_y + scrollY, floor.floor_width, floor.floor_height))
        if floor.image != None:
            root.blit(floor.image, (floor.floor_x, floor.floor_y + scrollY))


        # draw floor number
        text = font.render(str(floor.floor_number), True, (0, 0, 0))
        root.blit(text, (floor.floor_x + 10, floor.floor_y + scrollY + 10))

        # draw citizens
        if isinstance(floor, ResidentialFloor):
            for occupant in floor.occupants:
                pygame.draw.rect(root, (255, 255, 255), (floor.floor_x + 10, floor.floor_y + scrollY + 50, 80, 40))
                text = font.render(occupant.name, True, (0, 0, 0))
                root.blit(text, (floor.floor_x + 20, floor.floor_y + scrollY + 60))


    # draw buttons
    for button in buttons:
        button.draw(root)

    if showFloorButtons:
        root.blit(pygame.image.load("images/boxwindow.png"), (50, 110))
        for button in floorButtons:
            button.draw(root)

    # add test citizen to first residential floor
    if len(Floors) > 1:
        Floors[1].occupants.append(Citizens[0])

    # menu bar items
    root.blit(pygame.image.load("images/coin.png"), (10, 12))
    text = font.render(str(money), True, (255, 255, 255))
    root.blit(text, (35, 10))


    # draw scroll bar
    pygame.draw.rect(root, (200, 200, 200), (display_width - 5, (-scrollY / 10 + display_height - 50), 10, 50))

    # update display
    pygame.display.update()
    clock.tick(FPS)
