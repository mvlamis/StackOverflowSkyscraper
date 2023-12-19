# Stack Overflow Skyscraper
# Tiny Tower clone by Michael Vlamis

import pygame 
import random
import time
import os

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
citizenX = 10

font = pygame.font.Font("pixeloid.ttf", 20)
smallfont = pygame.font.Font("pixeloid.ttf", 15)

money = 100000
tick = 0

menuOpen = False
showFloorButtons = False
showCitizenList = False
showNewCitizen = True
sortList = "default"
floorMenu = -1

firstNames = open("FirstNames.txt", "r").read().split("\n")
lastNames = open("LastNames.txt", "r").read().split("\n")
residentialNames = open("ResidentialFloors.txt", "r").read().split("\n")

# image variables
floorImages = [
    pygame.image.load("images/residential/res1.png"),
    pygame.image.load("images/residential/res2.png"),
]

for image in range(len(floorImages)):
    # resize images
    floorImages[image] = floorImages[image].convert()
    floorImgRect = floorImages[image].get_rect()
    floorImages[image] = pygame.transform.scale(floorImages[image], (300, 100))

elevatorImage = pygame.image.load("images/elevator.png")
elevatorImage = pygame.transform.scale(elevatorImage, (300, 100))

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

class smallText:
    def __init__(self, x, y, text, color = (0, 0, 0)):
        self.x = x 
        self.y = y
        self.text = text
        self.color = color

    def draw(self, root):
        text = smallfont.render(self.text, True, self.color)
        root.blit(text, (self.x, self.y))

    def is_clicked(self, pos):
        pass

class Image:
    def __init__(self, x, y, image):
        self.x = x 
        self.y = y
        self.image = image
        root.blit(self.image, (self.x, self.y))

# game classes
class Product:
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = image
        
class Floor:
    def __init__(self, floor_number, image = None, title = None):
        self.floor_number = floor_number
        self.floor_color = (255, 255, 255)
        self.floor_width = display_width - 50
        self.floor_height = 100
        self.floor_x = 25
        self.floor_y = 500 - (self.floor_height * self.floor_number)
        self.image = image
        self.title = title

    def is_clicked(self, pos):
        if pos[0] > self.floor_x and pos[0] < self.floor_x + self.floor_width:
            if pos[1] > self.floor_y and pos[1] < self.floor_y + self.floor_height:
                return True
        return False

class ResidentialFloor(Floor):
    def __init__(self, floor_number, image = None, title = None):
        super().__init__(floor_number, image, title)
        self.floor_color = (255, 0, 0)
        self.occupants = []
        self.title = title + " Apts."

class CommercialFloor(Floor):
    RESTOCKING_PRICE = 100
    def __init__(self, floor_number, products = [None, None, None], stock = [0, 0, 0]):
        super().__init__(floor_number)
        self.floor_color = (0, 255, 0)
        self.employees = []
        self.products = products
        self.stock = stock

    def restock(self, product):
        global money
        if money >= CommercialFloor.RESTOCKING_PRICE:
            money -= CommercialFloor.RESTOCKING_PRICE
            self.stock[self.products.index(product)] += 10

class LobbyFloor(Floor):
    def __init__(self, floor_number):
        super().__init__(floor_number)
        self.floor_color = (0, 0, 255)
        self.title = "Lobby"

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

    def flip(self):
        self.clothesImage = pygame.transform.flip(self.clothesImage, True, False)
        self.hairImage = pygame.transform.flip(self.hairImage, True, False)
        self.eyesImage = pygame.transform.flip(self.eyesImage, True, False)
        self.skinImage = pygame.transform.flip(self.skinImage, True, False)


class Citizen:
    def __init__(self, name, jobFloor, homeFloor, appearance = None):
        self.name = name
        self.jobFloor = jobFloor
        self.homeFloor = homeFloor
        self.appearance = appearance
        self.xPos = 10
        self.speed = 0
        self.flipped = False

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

# get all images in products folder
products = []
for file in os.listdir("images/products"):
    if file.endswith(".png"):
        # get product info
        name = file.split(" ")[0]
        price = file.split(" ")[1].split(".")[0]
        image = pygame.image.load("images/products/" + file).convert_alpha()
        products.append(Product(name, price, image))

Floors = [LobbyFloor(0), ResidentialFloor(1, floorImages[0], "Canterbury"), CommercialFloor(2, [products[0], products[1], products[2]])]
Citizens = [Citizen("Michael", 2, 1, CitizenAppearance("clothes7", "hair9", "eyes1", "skin7")), 
            Citizen("George", 2, 1, CitizenAppearance("clothes1", "hair1", "eyes2", "skin1")),
            ]

# game loop
while True:
    # button declarations
    buttons = [
        Button(0, 0, display_width, 50, (200, 200, 200), "Menu", pygame.image.load("images/topbar.png")),
        Button(300, 0, 50, 50, color = None, text = "+", bgImage=pygame.image.load("images/plus.png")),
        Button(250, 0, 50, 50, color = (25,0,0), text = "list", bgImage=pygame.image.load("images/list.png")),
    ]

    # menu declarations
    newFloorMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Button(75, 200, 200, 50, (255, 0, 0), "Residential", pygame.image.load("images/orangebutton.png")),
        Button(75, 260, 200, 50, (0, 255, 0), "Commercial", pygame.image.load("images/greenbutton.png")),
        Button(75, 140, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png"))
    ])

    manageFloorMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Button(75, 140, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png")),
        Text(130, 145, "Floor " + str(floorMenu), (255, 255, 255)),
        Button(90, 240, 50, 50, (255, 0, 0), bgImage=pygame.image.load("images/placeholderbox.png")),
        Button(150, 240, 50, 50, (255, 0, 0), bgImage=pygame.image.load("images/placeholderbox.png")),
        Button(210, 240, 50, 50, (255, 0, 0), bgImage=pygame.image.load("images/placeholderbox.png")),
        Button(75, 200, 200, 30, (0, 255, 0), "Manage"),
    ])

    citizenListMenu = Menu(0, 0, pygame.image.load("images/purplebg.png"), [
        Button(10, 50, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png")),
        Text(70, 55, "Sort by:", (255, 255, 255)),
    ])

    newCitizenMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Text(75, 140, "New Citizen!", (255, 255, 255)),
        smallText(75, 160, "Name", (255, 255, 255)),
        Button(150, 200, 200, 30, (0, 255, 0), bgImage=pygame.image.load("images/placeholderbox.png")),
        Button(75, 275, 95, 30, (255, 0, 0), "Deny"),
        Button(180, 275, 95, 30, (0, 255, 0), "Lease"),
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
                scrollpos = pygame.mouse.get_pos() 
                scrollpos = (scrollpos[0], scrollpos[1] - scrollY)

                # top bar menu
                for button in range(len(buttons)):
                    if buttons[button].is_clicked(pos):
                        if button == 1 and not menuOpen:
                            showFloorButtons = True
                            menuOpen = True
                            break
                        if button == 2 and not menuOpen:
                            menuOpen = True
                            showCitizenList = True
                            break
                            
                            
                
                if showFloorButtons:
                    for button in range(len(newFloorMenu.buttons)):
                        if newFloorMenu.buttons[button].is_clicked(pos):
                            if button == 0:
                                Floors.append(ResidentialFloor(len(Floors), random.choice(floorImages), random.choice(residentialNames)))
                            if button == 1:
                                Floors.append(CommercialFloor(len(Floors), [random.choice(products), random.choice(products), random.choice(products)]))
                            if button == 2:
                                showFloorButtons = False
                            showFloorButtons = False
                            menuOpen = False
                    break
                            

                if showCitizenList:
                    if citizenListMenu.buttons[0].is_clicked(pos):
                        showCitizenList = False
                        menuOpen = False
                        break

                if showNewCitizen:
                    if newCitizenMenu.buttons[3].is_clicked(pos):
                        showNewCitizen = False
                        menuOpen = False
                    if newCitizenMenu.buttons[4].is_clicked(pos):
                        showNewCitizen = False
                        menuOpen = False
                        Citizens.append(randomizeCitizen(1, 2))
                    break

                # floor management menu
                for floor in Floors:
                    if floor.is_clicked(scrollpos) and not menuOpen:
                        floorMenu = floor.floor_number
                        menuOpen = True
                        break

                if floorMenu != -1:
                    for button in range(len(manageFloorMenu.buttons)):
                        if manageFloorMenu.buttons[button].is_clicked(pos):
                            if button == 0:
                                floorMenu = -1
                                menuOpen = False

                            if isinstance(Floors[floorMenu], CommercialFloor):
                                if button == 2:
                                    Floors[floorMenu].restock(Floors[floorMenu].products[0])
                                if button == 3:
                                    Floors[floorMenu].restock(Floors[floorMenu].products[1])
                                if button == 4:
                                    Floors[floorMenu].restock(Floors[floorMenu].products[2])

                            break
                                    

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

    BAR_HEIGHT = 25
    # draw floors based on scrollY
    for i in range(len(Floors)):
        floor = Floors[i]
        floor.floor_y = 500 - (floor.floor_height * floor.floor_number) - BAR_HEIGHT * i
        pygame.draw.rect(root, floor.floor_color, (floor.floor_x, floor.floor_y + scrollY, floor.floor_width, floor.floor_height))

        if floor.image != None:
            root.blit(floor.image, (floor.floor_x, floor.floor_y + scrollY))

        root.blit(elevatorImage, (floor.floor_x, floor.floor_y + scrollY))

        # draw floor title bar above floor
        pygame.draw.rect(root, (0, 0, 0), (floor.floor_x, floor.floor_y + scrollY - BAR_HEIGHT, floor.floor_width, BAR_HEIGHT))
        # draw floor number
        text = smallfont.render(str(floor.floor_number), True, (255, 255, 255))
        root.blit(text, (floor.floor_x + 10, floor.floor_y + scrollY + 3 - BAR_HEIGHT))
        # draw floor title
        if floor.title != None:
            text = smallfont.render(str(floor.title), True, (255, 255, 255))
            root.blit(text, (floor.floor_x + 30, floor.floor_y + scrollY + 3 - BAR_HEIGHT))

    # draw floor menu
    if floorMenu != -1:
        manageFloorMenu.draw(root)
        if isinstance(Floors[floorMenu], CommercialFloor):
            Image(90, 240, pygame.image.load("images/products/" + Floors[floorMenu].products[0].name + " " + Floors[floorMenu].products[0].price + ".png"))
            Text(100, 300, str(Floors[floorMenu].stock[0]), (0, 0, 0)).draw(root)
            Image(150, 240, pygame.image.load("images/products/" + Floors[floorMenu].products[1].name + " " + Floors[floorMenu].products[1].price + ".png"))
            Text(160, 300, str(Floors[floorMenu].stock[1]), (0, 0, 0)).draw(root)
            Image(210, 240, pygame.image.load("images/products/" + Floors[floorMenu].products[2].name + " " + Floors[floorMenu].products[2].price + ".png"))
            Text(220, 300, str(Floors[floorMenu].stock[2]), (0, 0, 0)).draw(root)
            Button(75, 200, 200, 30, (0, 255, 0), "Manage Employees").draw(root)
        
        if isinstance(Floors[floorMenu], ResidentialFloor):
            Button(75, 200, 200, 30, (0, 255, 0), "Manage Residents").draw(root)
            for i in range(len(Floors[floorMenu].occupants)):
                # place citizen images in each box 
                Floors[floorMenu].occupants[i].draw(root, 100 + (CitizenAppearance.CitizenSize * i * 2), 250)

                
    # draw buttons
    for button in buttons:
        button.draw(root)

    if showFloorButtons:
        newFloorMenu.draw(root)

    if showNewCitizen:
        newCitizenMenu.draw(root)

    if showCitizenList:
        sortedList = []
        if sortList == "default":
            sortedList = Citizens
        elif sortList == "alphabetical":
            sortedList = sorted(Citizens, key=lambda citizen: citizen.name)
        elif sortList == "home":
            sortedList = sorted(Citizens, key=lambda citizen: citizen.homeFloor)

        citizenListMenu.draw(root)

        for i in range(len(sortedList)):
            pygame.draw.rect(root, (255, 255, 255), (10, 100 + (i * 50), 330, 50))
            pygame.draw.rect(root, (0, 0, 0), (10, 100 + (i * 50), 330, 50), 4)

            sortedList[i].draw(root, 15, 110 + (i * 50))

            text = font.render(Citizens[i].name, True, (0, 0, 0))
            root.blit(text, (70, 110 + (i * 50)))

        if sortList == "default":
            pygame.draw.rect(root, (0, 255, 0), (177.5, 47.5, 35, 35))
        elif sortList == "alphabetical":
            pygame.draw.rect(root, (0, 255, 0), (227.5, 47.5, 35, 35))
        elif sortList == "home":
            pygame.draw.rect(root, (0, 255, 0), (277.5, 47.5, 35, 35))

        Button(180, 50, 30, 30, (255, 255, 255), "def").draw(root)
        Button(230, 50, 30, 30, (255, 255, 255), "a-z").draw(root)
        Button(280, 50, 30, 30, (255, 255, 255), "home").draw(root)

    # menu bar items
    root.blit(pygame.image.load("images/coin.png"), (10, 12))
    text = font.render(str(round(money)), True, (255, 255, 255))
    root.blit(text, (35, 10))

    # draw scroll bar
    pygame.draw.rect(root, (200, 200, 200), (display_width - 5, (-scrollY / 10 + display_height - 50), 10, 50))

    # --- game logic ---
    # citizen movement

    # draw citizens
    if not showCitizenList:
        for floor in Floors:
            if isinstance(floor, ResidentialFloor):
                for citizen in range(len(floor.occupants)):

                    # citizens move randomly
                    if tick % 100 == 0:
                        floor.occupants[citizen].speed = random.choice([-1, 0, 0, 1])

                    if floor.occupants[citizen].speed == 1 and floor.occupants[citizen].xPos < 200:
                        floor.occupants[citizen].xPos += 0.5
                    elif floor.occupants[citizen].speed == -1 and floor.occupants[citizen].xPos > 0:
                        floor.occupants[citizen].xPos -= 0.5

                    
                    if floor.occupants[citizen].speed == -1 and not floor.occupants[citizen].flipped:
                        floor.occupants[citizen].appearance.flip()
                        floor.occupants[citizen].flipped = True
                    elif floor.occupants[citizen].speed == 1 and floor.occupants[citizen].flipped:
                        floor.occupants[citizen].appearance.flip()
                        floor.occupants[citizen].flipped = False
                        
                    floor.occupants[citizen].draw(root, floor.floor_x + floor.occupants[citizen].xPos + (CitizenAppearance.CitizenSize * citizen), floor.floor_y + scrollY + 90 - CitizenAppearance.CitizenSize)


    # --- economy ---
    # collect rent every 150 ticks
    if tick % 150 == 0:
        for citizen in Citizens:
            money += 10

    # update display
    pygame.display.update()
    clock.tick(FPS)
    tick += 1
