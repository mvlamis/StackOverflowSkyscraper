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
timer = 0

display_width = 350
display_height = 600

scrollY = 0
citizenX = 10

font = pygame.font.Font("pixeloid.ttf", 20)
smallfont = pygame.font.Font("pixeloid.ttf", 15)

money = 0
tick = 0

menuOpen = False
showFloorButtons = False
showCitizenList = False
showNewCitizen = False
sortList = "home"
floorMenu = -1
popupText = ""

firstNames = open("FirstNames.txt", "r").read().split("\n")
lastNames = open("LastNames.txt", "r").read().split("\n")
residentialNames = open("ResidentialFloors.txt", "r").read().split("\n")

newFloorPrice = 0
floorPrices = open("NewFloorPrices.txt", "r").read().split("\n")

# image variables
floorImages = [
    pygame.image.load("images/residential/res1.png"),
    pygame.image.load("images/residential/res2.png"),
]

commercialFloorImages = [
    pygame.image.load("images/commerical/com1.png"),
    pygame.image.load("images/commerical/com2.png"),
    pygame.image.load("images/commerical/com3.png"),
    pygame.image.load("images/commerical/com4.png"),
    pygame.image.load("images/commerical/com5.png"),
    pygame.image.load("images/commerical/com6.png"),
    pygame.image.load("images/commerical/com7.png"),
    pygame.image.load("images/commerical/com8.png"),
    pygame.image.load("images/commerical/com9.png"),
    pygame.image.load("images/commerical/com10.png"),
]

commercialFloorTypes = []


for image in range(len(floorImages)):
    # resize images
    floorImages[image] = floorImages[image].convert()
    floorImgRect = floorImages[image].get_rect()
    floorImages[image] = pygame.transform.scale(floorImages[image], (300, 100))

for image in range(len(commercialFloorImages)):
    # resize images
    commercialFloorImages[image] = commercialFloorImages[image].convert()
    commercialFloorImgRect = commercialFloorImages[image].get_rect()
    commercialFloorImages[image] = pygame.transform.scale(commercialFloorImages[image], (300, 100))

elevatorImage = pygame.image.load("images/elevator.png")
elevatorImage = pygame.transform.scale(elevatorImage, (300, 100))

def jobSort(list):
    # sort citizens by job floor
    sortedList = []
    for i in range(len(list)):
        sortedList.append(list[i])
        for j in range(len(sortedList)):
            if sortedList[j].jobFloor > sortedList[i].jobFloor:
                sortedList[i], sortedList[j] = sortedList[j], sortedList[i]

    return sortedList

def alphaSort(list):
    # sort citizen names alphabetically
    sortedList = []
    for i in range(len(list)):
        sortedList.append(list[i])
        for j in range(len(sortedList)):
            if sortedList[j].name > sortedList[i].name:
                sortedList[i], sortedList[j] = sortedList[j], sortedList[i]

    return sortedList

def homeSort(list):
    # sort citizens by home floor
    sortedList = []
    for i in range(len(list)):
        sortedList.append(list[i])
        for j in range(len(sortedList)):
            if sortedList[j].homeFloor > sortedList[i].homeFloor:
                sortedList[i], sortedList[j] = sortedList[j], sortedList[i]

    return sortedList

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

# from CommercialFloors.txt, get all floor types, images, and products
# store in multi dimensional commercialFloorTypes list
for line in open("CommercialFloors.txt", "r").read().split("\n"):
    if line != "Title, Image file, product 1, product 2, product 3": # ignore first line
        # Format: Title, Image file, product 1, product 2, product 3
        commercialFloorTypes.append(line.split(", "))

        # set image if it exists
        if os.path.exists("images/commerical/" + line.split(", ")[1]):
            commercialFloorImages.append(pygame.image.load("images/commerical/" + line.split(", ")[1]))

        # set products if they exist
        for i in range(2, len(line.split(", "))):
            productTitle = line.split(", ")[i]
            productTitle = productTitle.lower()
            if os.path.exists("images/products/" + productTitle + ".png"):
                commercialFloorTypes[-1][i] = Product(productTitle, productTitle.split(" ")[-1], pygame.image.load("images/products/" + productTitle + ".png"))
            else:
                commercialFloorTypes[-1][i] = Product("placeholder", "0", pygame.image.load("images/closebutton.png"))

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

    def __init__(self, floor_number, type):
        super().__init__(floor_number)
        self.floor_color = (0, 255, 0)
        self.employee = None
        self.products = [None, None, None]
        self.stock = [0, 0, 0]
    
        # get floor info from CommercialFloorTypes
        for i in range(len(commercialFloorTypes)):
            if commercialFloorTypes[i][0] == type:
                self.title = commercialFloorTypes[i][0]
                self.image = commercialFloorImages[i]
                self.products = [commercialFloorTypes[i][2], commercialFloorTypes[i][3], commercialFloorTypes[i][4]]
                break

    def restock(self, product):
        """Each Commercial floor sells three types of stock. The first stocked item sells for one coin each, the second for two and the third for three. 
        For each item, the base cost to stock the item is 60% of the amount of the item received."""
        global money

        if product == self.products[0]:
            productPrice = 40
        if product == self.products[1]:
            productPrice = 80
        if product == self.products[2]:
            productPrice = 120
            
        if money >= productPrice and self.stock[self.products.index(product)] == 0:
            self.stock[self.products.index(product)] = 144 * (1 + self.products.index(product))
            money -= int(productPrice)

    def sell(self):
        """Each stock is sold at a constant rate of 12 coins per minute. This means a fully stocked floor generates 36 coins per minute.
        A 1-coin item is sold every 5 seconds, a 2-coin item every 10 seconds and a 3-coin item every 15 seconds."""

        global money
        global timer

        for floor in Floors:
            if isinstance(floor, CommercialFloor):
                for i in range(len(floor.stock)):
                    if floor.stock[i] > 0:
                        if i == 0 and timer % 300 == 0:
                            money += 12
                            floor.stock[i] -= 1
                        if i == 1 and timer % 600 == 0:
                            money += 12
                            floor.stock[i] -= 1 
                        if i == 2 and timer % 900 == 0:
                            money += 12
                            floor.stock[i] -= 1
        timer += 1



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

def CitizenPicker():
    # opens a list of citizens and returns a citizen object from user selection
    sortedList = []
    if sortList == "job":
        sortedList = Citizens
    elif sortList == "alphabetical":
        sortedList = alphaSort(Citizens)
    elif sortList == "home":
        sortedList = homeSort(Citizens)

    citizenListMenu.draw(root)

    for i in range(len(sortedList)):
        pygame.draw.rect(root, (255, 255, 255), (10, 100 + (i * 50), 330, 50))
        pygame.draw.rect(root, (0, 0, 0), (10, 100 + (i * 50), 330, 50), 4)

        sortedList[i].draw(root, 15, 110 + (i * 50))

        text = font.render(sortedList[i].name, True, (0, 0, 0))
        root.blit(text, (70, 110 + (i * 50)))

        root.blit(pygame.image.load("images/houseicon.png"), (170, 118 + (i * 50)))
        text = smallfont.render(str(sortedList[i].homeFloor), True, (0, 0, 0))
        root.blit(text, (200, 118 + (i * 50)))

        root.blit(pygame.image.load("images/workicon.png"), (260, 118 + (i * 50)))
        text = smallfont.render(str(sortedList[i].jobFloor), True, (0, 0, 0))
        root.blit(text, (290, 118 + (i * 50)))


    if sortList == "job":
        root.blit(pygame.image.load("images/jobbuttonpushed.png"), (177.5, 47.5))
    elif sortList == "alphabetical":
        root.blit(pygame.image.load("images/alphabetbuttonpushed.png"), (227.5, 47.5))
    elif sortList == "home":
        root.blit(pygame.image.load("images/housebuttonpushed.png"), (277.5, 47.5))

Floors = [LobbyFloor(0), ResidentialFloor(1, floorImages[0], "Canterbury"), CommercialFloor(2, type="Grocery Store")]
Citizens = [Citizen("Michael", 2, 1, CitizenAppearance("clothes7", "hair9", "eyes1", "skin7")), 
            Citizen("George", 2, 1, CitizenAppearance("clothes1", "hair1", "eyes2", "skin1")),
            Citizen("Amy", 2, 3, CitizenAppearance("clothes2", "hair2", "eyes3", "skin2")),
            Citizen("Zorin", 2, 3, CitizenAppearance("clothes3", "hair3", "eyes4", "skin3")),
            ]

# game loop
while True:
    startTime = time.perf_counter()
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
        Button(75, 140, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png")),
        Text(130, 140, "New floor", (255, 255, 255)),
        Button(125, 170, 20, 20, bgImage=pygame.image.load("images/coin.png")),
        smallText(150, 170, str(newFloorPrice), (255, 255, 255)),
        
    ])

    manageFloorMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Button(75, 140, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png")),
        Text(130, 145, "Floor " + str(floorMenu), (255, 255, 255)),
        Button(90, 240, 50, 50, (255, 0, 0), bgImage=pygame.image.load("images/placeholderbox.png")),
        Button(150, 240, 50, 50, (255, 0, 0), bgImage=pygame.image.load("images/placeholderbox.png")),
        Button(210, 240, 50, 50, (255, 0, 0), bgImage=pygame.image.load("images/placeholderbox.png")),
    ])

    citizenListMenu = Menu(0, 0, pygame.image.load("images/purplebg.png"), [
        Button(10, 50, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png")),
        Text(70, 55, "Sort by:", (255, 255, 255)),
        Button(177.5, 47.5, 30, 30, (255, 255, 255), bgImage=pygame.image.load("images/jobbutton.png")),
        Button(227.5, 47.5, 30, 30, (255, 255, 255), bgImage=pygame.image.load("images/alphabetbutton.png")),
        Button(277.5, 47.5, 30, 30, (255, 255, 255), bgImage=pygame.image.load("images/housebutton.png")),
    ])

    newCitizenMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Text(75, 140, "New Citizen!", (255, 255, 255)),
        smallText(75, 160, "Name", (255, 255, 255)),
        Button(150, 200, 200, 30, (0, 255, 0), bgImage=pygame.image.load("images/placeholderbox.png")),
        Button(75, 275, 95, 30, (255, 0, 0), "Deny"),
        Button(180, 275, 95, 30, (0, 255, 0), "Lease"),
    ])
    
    popupMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Text(75, 140, popupText, (255, 255, 255)),
        Button(100, 260, 150, 50, (0, 255, 0), bgImage=pygame.image.load("images/okbutton.png")),
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
                                if money >= newFloorPrice:
                                    Floors.append(ResidentialFloor(len(Floors), random.choice(floorImages), random.choice(residentialNames)))
                                    money -= newFloorPrice
                                    newFloorPrice = int(floorPrices[len(Floors) - 1])
                                else:
                                    popupText = "Not enough money!"
                            if button == 1:
                                # get random commercial floor type
                                randomFloorType = random.choice(commercialFloorTypes)
                                randomFloorType = randomFloorType[0]
                                Floors.append(CommercialFloor(len(Floors), randomFloorType))
                            if button == 2:
                                showFloorButtons = False
                            showFloorButtons = False
                            menuOpen = False
                    break
                            
                if popupText != "":
                    if popupMenu.buttons[1].is_clicked(pos):
                        popupText = ""
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

                # citizen list menu
                if showCitizenList:
                    for button in range(len(citizenListMenu.buttons)):
                        if citizenListMenu.buttons[button].is_clicked(pos):
                            if button == 0:
                                showCitizenList = False
                                menuOpen = False
                            if button == 2:
                                sortList = "job"
                            if button == 3:
                                sortList = "alphabetical"
                            if button == 4:
                                sortList = "home"
                            break
                                    

    # blit background image based on scrollY
    root.fill((255, 255, 255))
    root.blit(pygame.image.load("images/Background-day.jpeg"), (0, scrollY / 10 - 4150))

    # allocate citizens to floors
    for citizen in Citizens:
        for floor in Floors:
            if isinstance(floor, ResidentialFloor):
                if floor.floor_number == citizen.homeFloor and citizen not in floor.occupants:
                    floor.occupants.append(citizen)
            if isinstance(floor, CommercialFloor):
                if floor.floor_number == citizen.jobFloor and floor.employee == None:
                    floor.employee = citizen

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
        text = smallfont.render(str(floor.floor_number) + "  " + str(floor.title), True, (255, 255, 255))
        root.blit(text, (floor.floor_x + 10, floor.floor_y + scrollY + 3 - BAR_HEIGHT))
        # # draw floor title
        # if floor.title != None:
        #     text = smallfont.render(str(floor.title), True, (255, 255, 255))
        #     root.blit(text, (floor.floor_x + 30, floor.floor_y + scrollY + 3 - BAR_HEIGHT))

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


    # draw floor menu
    if floorMenu != -1:
        manageFloorMenu.draw(root)
        if isinstance(Floors[floorMenu], CommercialFloor):
            Image(90, 240, pygame.image.load("images/products/" + Floors[floorMenu].products[0].name + ".png"))
            Text(100, 250, str(Floors[floorMenu].products[0].name), (0, 0, 0)).draw(root)
            smallText(100, 310, str(Floors[floorMenu].stock[0]), (0, 0, 0)).draw(root)
            pygame.draw.rect(root, (255, 255, 255), (90, 300, 50, 10))
            pygame.draw.rect(root, (0, 255, 0), (90, 300, (Floors[floorMenu].stock[0]/144*50), 10))

            Image(150, 240, pygame.image.load("images/products/" + Floors[floorMenu].products[1].name + ".png"))
            Text(150, 250, str(Floors[floorMenu].products[1].name), (0, 0, 0)).draw(root)
            smallText(160, 310, str(Floors[floorMenu].stock[1]), (0, 0, 0)).draw(root)
            pygame.draw.rect(root, (255, 255, 255), (150, 300, 50, 10))
            pygame.draw.rect(root, (0, 255, 0), (150, 300, (Floors[floorMenu].stock[1]/288*50), 10))

            Image(210, 240, pygame.image.load("images/products/" + Floors[floorMenu].products[2].name + ".png"))
            Text(210, 250, str(Floors[floorMenu].products[2].name), (0, 0, 0)).draw(root)
            smallText(220, 310, str(Floors[floorMenu].stock[2]), (0, 0, 0)).draw(root)
            pygame.draw.rect(root, (255, 255, 255), (210, 300, 50, 10))
            pygame.draw.rect(root, (0, 255, 0), (210, 300, (Floors[floorMenu].stock[2]/432*50), 10))

            Button(150, 180, 50, 50, bgImage=pygame.image.load("images/placeholderbox.png")).draw(root)

            if Floors[floorMenu].employee != None:
                Floors[floorMenu].employee.draw(root, 160, 190)

        if isinstance(Floors[floorMenu], ResidentialFloor):
            # Button(75, 200, 200, 30, (0, 255, 0), "Manage Residents").draw(root)
            for i in range(len(Floors[floorMenu].occupants)):
                # place citizen images in each box 
                Floors[floorMenu].occupants[i].draw(root, 100 + (CitizenAppearance.CitizenSize * i * 2), 250)

    # draw popup
    if popupText != "":
        popupMenu.draw(root)
                
    # draw buttons
    for button in buttons:
        button.draw(root)

    if showFloorButtons:
        newFloorMenu.draw(root)

    if showNewCitizen:
        newCitizenMenu.draw(root)

    if showCitizenList:
        CitizenPicker()

    # menu bar items
    root.blit(pygame.image.load("images/coin.png"), (10, 12))
    text = font.render(str(round(money)), True, (255, 255, 255))
    root.blit(text, (35, 10))

    # draw scroll bar
    pygame.draw.rect(root, (200, 200, 200), (display_width - 5, (-scrollY / 10 + display_height - 50), 10, 50))

    # --- economy ---
    # # collect rent every 150 ticks
    # if tick % 150 == 0:
    #     for citizen in Citizens:
    #         money += 10

    # Always Be Closing
    for floor in Floors:
        if isinstance(floor, CommercialFloor):
            floor.sell()


    # update display
    pygame.display.update()
    clock.tick(FPS)
    tick += 1