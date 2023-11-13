# Stack Overflow Skyscraper
# Tiny Tower clone by Michael Vlamis

import pygame 
import random
import time

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

font = pygame.font.Font("pixeloid.ttf", 20)

money = 100000

menuOpen = False
showFloorButtons = False
floorMenu = -1

firstNames = open("FirstNames.txt", "r").read().split("\n")
lastNames = open("LastNames.txt", "r").read().split("\n")

# image variables
floorImages = [
    pygame.image.load("images/residential/res1.png"),
]
for image in range(len(floorImages)):
    # resize images
    floorImages[image] = floorImages[image].convert()
    floorImgRect = floorImages[image].get_rect()
    floorImages[image] = pygame.transform.scale(floorImages[image], (300, 100))

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
    
class Menu:
    def __init__(self, x, y, bgImage, buttons):
        self.x = x 
        self.y = y
        self.bgImage = bgImage
        self.buttons = buttons

    def draw(self, root):
        root.blit(self.bgImage, (self.x, self.y))
        for button in self.buttons:
            button.draw(root)

class Text:
    def __init__(self, x, y, text, color = (0, 0, 0)):
        self.x = x 
        self.y = y
        self.text = text
        self.color = color

    def draw(self, root):
        text = font.render(self.text, True, self.color)
        root.blit(text, (self.x, self.y))

    def is_clicked(self, pos):
        pass



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

    def is_clicked(self, pos):
        if pos[0] > self.floor_x and pos[0] < self.floor_x + self.floor_width:
            if pos[1] > self.floor_y and pos[1] < self.floor_y + self.floor_height:
                return True
        return False

class ResidentialFloor(Floor):
    def __init__(self, floor_number, image = None):
        super().__init__(floor_number, image)
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

class CitizenAppearance:
    CitizenSize = 30
    def __init__(self, clothes, hair, eyes, skin):
        self.clothes = clothes
        self.hair = hair
        self.eyes = eyes
        self.skin = skin

        self.clothesImage = pygame.image.load("images/clothes/" + self.clothes + ".png").convert_alpha()
        self.hairImage = pygame.image.load("images/hair/" + self.hair + ".png").convert_alpha()
        self.eyesImage = pygame.image.load("images/eyes/" + self.eyes + ".png").convert_alpha()
        self.skinImage = pygame.image.load("images/skin/" + self.skin + ".png").convert_alpha()

        # resize images
        self.clothesImage = pygame.transform.scale(self.clothesImage, (CitizenAppearance.CitizenSize, CitizenAppearance.CitizenSize))
        self.hairImage = pygame.transform.scale(self.hairImage, (CitizenAppearance.CitizenSize, CitizenAppearance.CitizenSize))
        self.eyesImage = pygame.transform.scale(self.eyesImage, (CitizenAppearance.CitizenSize, CitizenAppearance.CitizenSize))
        self.skinImage = pygame.transform.scale(self.skinImage, (CitizenAppearance.CitizenSize, CitizenAppearance.CitizenSize))


class Citizen:
    def __init__(self, name, jobFloor, homeFloor, appearance = None):
        self.name = name
        self.jobFloor = jobFloor
        self.homeFloor = homeFloor
        self.appearance = appearance

    def draw(self, root, x = 0, y = 0):
        root.blit(self.appearance.skinImage, (x, y))
        root.blit(self.appearance.clothesImage, (x, y))
        root.blit(self.appearance.hairImage, (x, y))
        root.blit(self.appearance.eyesImage, (x, y))

def randomizeCitizen(homeFloor, jobFloor):
    clothes = random.choice(["clothes1", "clothes2", "clothes3", "clothes4", "clothes5", "clothes6", "clothes7", "clothes8", "clothes9", "clothes10"])
    hair = random.choice(["hair1"])
    eyes = random.choice(["eyes1", "eyes2", "eyes3", "eyes4"])
    skin = random.choice(["skin1", "skin2", "skin3", "skin4", "skin5", "skin6", "skin7", "skin8"])

    appearance = CitizenAppearance(clothes, hair, eyes, skin)

    name = random.choice(firstNames) + " " + random.choice(lastNames)

    return Citizen(name, homeFloor, jobFloor, appearance)

Floors = [LobbyFloor(0), ResidentialFloor(1, floorImages[0]), CommercialFloor(2)]
Citizens = [Citizen("Michael", 2, 1, CitizenAppearance("clothes7", "hair9", "eyes1", "skin7")), 
            Citizen("George", 2, 1, CitizenAppearance("clothes1", "hair1", "eyes2", "skin1")),
            ]

# game loop
while True:

    # button declarations
    buttons = [
        Button(0, 0, display_width, 50, (200, 200, 200), "Menu", pygame.image.load("images/topbar.png")),
        Button(300, 0, 50, 50, color = None, text = "+", bgImage=pygame.image.load("images/plus.png")),
    ]

    # menu declarations
    newFloorMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Button(75, 200, 200, 50, (255, 0, 0), "Residential", pygame.image.load("images/orangebutton.png")),
        Button(75, 260, 200, 50, (0, 255, 0), "Commercial", pygame.image.load("images/greenbutton.png")),
        Button(75, 140, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png"))
    ])

    manageFloorMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Button(75, 140, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png")),
        Text(75, 200, "Manage Floor " + str(floorMenu), (255, 255, 255)),
    ])


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

                # top bar menu
                for button in range(len(buttons)):
                    if buttons[button].is_clicked(pos):
                        if button == 1 and not menuOpen:
                            showFloorButtons = True
                            menuOpen = True
                
                if showFloorButtons:
                    for button in range(len(newFloorMenu.buttons)):
                        if newFloorMenu.buttons[button].is_clicked(pos):
                            if button == 0:
                                Floors.append(ResidentialFloor(len(Floors)))
                            if button == 1:
                                Floors.append(CommercialFloor(len(Floors)))
                            if button == 2:
                                showFloorButtons = False
                            showFloorButtons = False
                            menuOpen = False

                # floor management menu
                for floor in Floors:
                    if floor.is_clicked(pos) and not menuOpen:
                        floorMenu = floor.floor_number
                        menuOpen = True

                if floorMenu != -1:
                    for button in range(len(manageFloorMenu.buttons)):
                        if manageFloorMenu.buttons[button].is_clicked(pos):
                            if button == 0:
                                floorMenu = -1
                                menuOpen = False

                    


    # blit background image based on scrollY
    root.fill((255, 255, 255))
    root.blit(pygame.image.load("images/Background-day.jpeg"), (0, scrollY / 10 - 4150))

    # allocate citizens to citizen floors
    for citizen in Citizens:
        for floor in Floors:
            if floor.floor_number == citizen.jobFloor and citizen not in floor.employees:
                floor.employees.append(citizen)
            if floor.floor_number == citizen.homeFloor and citizen not in floor.occupants:
                floor.occupants.append(citizen)

    # draw floors based on scrollY
    for floor in Floors:
        pygame.draw.rect(root, floor.floor_color, (floor.floor_x, floor.floor_y + scrollY, floor.floor_width, floor.floor_height))
        if floor.image != None:
            root.blit(floor.image, (floor.floor_x, floor.floor_y + scrollY))


        # draw floor number
        text = font.render(str(floor.floor_number), True, (0, 0, 0))
        root.blit(text, (floor.floor_x + 10, floor.floor_y + scrollY + 10))      

    # draw floor menu
    if floorMenu != -1:
        manageFloorMenu.draw(root)

    # draw buttons
    for button in buttons:
        button.draw(root)

    if showFloorButtons:
        newFloorMenu.draw(root)

    # menu bar items
    root.blit(pygame.image.load("images/coin.png"), (10, 12))
    text = font.render(str(money), True, (255, 255, 255))
    root.blit(text, (35, 10))

    # draw citizens
    for floor in Floors:
        if isinstance(floor, ResidentialFloor):
            for citizen in range(len(floor.occupants)):
                floor.occupants[citizen].draw(root, floor.floor_x + 10 + (CitizenAppearance.CitizenSize * citizen), floor.floor_y + scrollY + 90 - CitizenAppearance.CitizenSize)

    text = font.render(str(menuOpen), True, (255, 0, 0))
    root.blit(text, (0, 0))
    text = font.render(str(floorMenu), True, (255, 0, 0))
    root.blit(text, (0, 20))

    # draw scroll bar
    pygame.draw.rect(root, (200, 200, 200), (display_width - 5, (-scrollY / 10 + display_height - 50), 10, 50))
    
    # update display
    pygame.display.update()
    clock.tick(FPS)
