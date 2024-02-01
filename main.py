# Stack Overflow Skyscraper
# Tiny Tower clone by Michael Vlamis

import pygame 
import random
import time
import os
import numpy as np

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

font = pygame.font.Font("pixeloid.ttf", 20)
smallfont = pygame.font.Font("pixeloid.ttf", 15)

money = 100
coinspersecond = 0
lastMoney = 0
tick = 0
delayCounter = 0

menuOpen = False
showFloorButtons = False
showCitizenList = False
citizenListPurpose = ""
floorToEmploy = None
selectedCitizen = None
showNewCitizen = False
showArrows = False
sortList = "home"
floorMenu = -1
showConfirmEvictMenu = False

popupText = ""
popupLine1 = ""
popupLine2 = ""
popupLine3 = ""
popupLine4 = ""

fading = False
fadeAmount = 0

elevatorOpen = False
unassignedCitizen = None
selectedFloor = None
citizenInElevator = None

tutorialState = 0
tutorialEndTimer = 0

firstNames = open("FirstNames.txt", "r").read().split("\n")
lastNames = open("LastNames.txt", "r").read().split("\n")
residentialNames = open("ResidentialFloors.txt", "r").read().split("\n")

newFloorPrice = 100

# image variables
floorImages = [
    pygame.image.load("images/residential/res1.png"),
    pygame.image.load("images/residential/res2.png"),
    pygame.image.load("images/residential/res3.png"),
    pygame.image.load("images/residential/res4.png"),
]

commercialFloorImages = [
    pygame.image.load("images/commerical/commerical1.png"),
    pygame.image.load("images/commerical/commerical2.png"),
    pygame.image.load("images/commerical/commerical3.png"),
    pygame.image.load("images/commerical/commerical4.png"),
    pygame.image.load("images/commerical/commerical5.png"),
    pygame.image.load("images/commerical/commerical6.png"),
    pygame.image.load("images/commerical/commerical7.png"),
    pygame.image.load("images/commerical/commerical8.png"),
    pygame.image.load("images/commerical/commerical9.png"),
    pygame.image.load("images/commerical/commerical10.png"),
]

commercialFloorTypes = []

lobbyImages = [
    pygame.image.load("images/lobby/wallpaper.png"),
    pygame.image.load("images/lobby/door.png"),
    pygame.image.load("images/lobby/couch.png"),
    pygame.image.load("images/lobby/bulletin.png"),
    pygame.image.load("images/lobby/plant.png"),
    pygame.image.load("images/lobby/lights.png"),
]


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

for image in range(len(lobbyImages)):
    # resize images
    lobbyImages[image] = lobbyImages[image].convert_alpha()
    lobbyImages[image] = pygame.transform.scale(lobbyImages[image], (300, 100))
    # allow per pixel alpha
    lobbyImages[image].set_colorkey((255, 255, 255))

elevatorImage = pygame.image.load("images/elevator.png")
elevatorImage = pygame.transform.scale(elevatorImage, (300, 100))

elevatorOpenImage = pygame.image.load("images/elevator open.png")
elevatorOpenImage = pygame.transform.scale(elevatorOpenImage, (300, 100))

def rgb_to_hsv(rgb): # stolen with love from https://stackoverflow.com/questions/7274221/changing-image-hue-with-python-pil
    # Translated from source of colorsys.rgb_to_hsv
    # r,g,b should be a numpy arrays with values between 0 and 255
    # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    # in case an RGBA array was passed, just copy the A channel
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv

def hsv_to_rgb(hsv):
    # Translated from source of colorsys.hsv_to_rgb
    # h,s should be a numpy arrays with values between 0.0 and 1.0
    # v should be a numpy array with values between 0.0 and 255.0
    # hsv_to_rgb returns an array of uints between 0 and 255.
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype('uint8')
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype('uint8')

def jobSort(list):
    """sort citizens by job floor"""
    sortedList = []
    for i in range(len(list)):
        sortedList.append(list[i])
        for j in range(len(sortedList)):
            if sortedList[j].jobFloor > sortedList[i].jobFloor:
                sortedList[i], sortedList[j] = sortedList[j], sortedList[i]

    return sortedList

def alphaSort(list):
    """sort citizens in alphabetical order"""
    sortedList = []
    for i in range(len(list)):
        sortedList.append(list[i])
        for j in range(len(sortedList)):
            if sortedList[j].name > sortedList[i].name:
                sortedList[i], sortedList[j] = sortedList[j], sortedList[i]

    return sortedList

def homeSort(list):
    """sort citizens by home floor"""
    sortedList = []
    for i in range(len(list)):
        sortedList.append(list[i])
        for j in range(len(sortedList)):
            if sortedList[j].homeFloor > sortedList[i].homeFloor:
                sortedList[i], sortedList[j] = sortedList[j], sortedList[i]

    return sortedList

def splitText():
    """split text into lines that fit into popup menu"""
    global popupLine1
    global popupLine2
    global popupLine3
    global popupLine4
    global popupText
    global font

    target = 210

    # separate text into words
    if popupText != "":
        words = popupText.split(" ")
    else:
        popupLine1 = ""
        popupLine2 = ""
        popupLine3 = ""
        popupLine4 = ""
        return
    
    # split words into lines
    lines = []
    current_line = ""
    testSurface = pygame.Surface((target, 1000))
    testSurface.fill((0, 0, 0))
    testSurface.set_alpha(0)
    
    for word in words:
        testLineRect = font.render(current_line + word + " ", True, (0, 0, 0)).get_rect()
        if testLineRect.width <= target:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    lines.append(current_line.strip())

    # assign lines to popupLine variables
    popupLine1 = lines[0] if len(lines) >= 1 else ""
    popupLine2 = lines[1] if len(lines) >= 2 else ""
    popupLine3 = lines[2] if len(lines) >= 3 else ""
    popupLine4 = lines[3] if len(lines) >= 4 else ""


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

    def fadeIn(self, root):
        global fadeAmount

        if self.bgImage != None:
            self.bgImage.set_alpha(fadeAmount)
            root.blit(self.bgImage, (self.x, self.y))
        else:
            pygame.draw.rect(root, self.color, (self.x, self.y, self.width, self.height))
            text = font.render(self.text, True, (0, 0, 0))
            text.set_alpha(fadeAmount)
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

    def fadeIn(self, root):
        global fading
        global fadeAmount

        if not fading:
            if fadeAmount < 255:
                fading = True
                fadeAmount += 17
                self.bgImage.set_alpha(fadeAmount)
                root.blit(self.bgImage, (self.x, self.y))
                for button in self.buttons:
                    button.fadeIn(root)

            fading = False

        if fadeAmount >= 255:
            self.draw(root)

class Text:
    def __init__(self, x, y, text, color = (0, 0, 0)):
        self.x = x 
        self.y = y
        self.text = text
        self.color = color

    def draw(self, root):
        text = font.render(self.text, True, self.color)
        root.blit(text, (self.x, self.y))

    def fadeIn(self, root):
        global fadeAmount

        text = font.render(self.text, True, self.color)
        text.set_alpha(fadeAmount)
        root.blit(text, (self.x, self.y))

    def is_clicked(self, pos):
        pass

class smallText(Text):
    def __init__(self, x, y, text, color = (0, 0, 0)):
        super().__init__(x, y, text, color)

    def draw(self, root):
        text = smallfont.render(self.text, True, self.color)
        root.blit(text, (self.x, self.y))

    def fadeIn(self, root):
        global fadeAmount

        if fadeAmount < 255:
            text = smallfont.render(self.text, True, self.color)
            text.set_alpha(fadeAmount)
            root.blit(text, (self.x, self.y))
    
class Image:
    def __init__(self, x, y, image):
        self.x = x 
        self.y = y
        self.image = image
        root.blit(self.image, (self.x, self.y))

class ColourPicker: # with thanks to https://stackoverflow.com/questions/73517832/how-to-make-an-color-picker-in-pygame
    COLOUR_PICKER_WIDTH = 210
    COLOUR_PICKER_HEIGHT = 30
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ColourPicker.COLOUR_PICKER_WIDTH, ColourPicker.COLOUR_PICKER_HEIGHT)
        self.image = pygame.Surface((ColourPicker.COLOUR_PICKER_WIDTH, ColourPicker.COLOUR_PICKER_HEIGHT))
        self.image.fill((159, 156, 211))
        self.pickerRadius = ColourPicker.COLOUR_PICKER_HEIGHT // 2
        self.pickerWidth = self.rect.width - self.pickerRadius * 2
        for i in range(self.pickerWidth):
            colour = pygame.Color(0)
            colour.hsla = (int(360*i/self.pickerWidth), 100, 50, 100)
            pygame.draw.rect(self.image, colour, (i+self.pickerRadius, ColourPicker.COLOUR_PICKER_HEIGHT//3, 1, ColourPicker.COLOUR_PICKER_HEIGHT//3))
        self.pos = 0

    def get_colour(self):
        colour = pygame.Color(0)
        colour.hsla = (int(self.pos * 360), 100, 50, 100)
        return colour
    
    def update(self):
        global lobbyImages
        mouseButtons = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        if mouseButtons[0] and self.rect.collidepoint(mousePos):
            self.pos = (mousePos[0] - self.rect.left - self.pickerRadius) / self.pickerWidth
            self.pos = max(0, min(1, self.pos))

    def draw(self, root):
        root.blit(self.image, self.rect)
        pygame.draw.circle(root, self.get_colour(), (self.rect.left + self.pickerRadius + int(self.pos * self.pickerWidth), self.rect.centery), self.pickerRadius)

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
        global popupText
        global menuOpen
        global tutorialState
        global tutorialEndTimer

        if tutorialState == 4:
            tutorialState = 5
            tutorialEndTimer = pygame.time.get_ticks()

        if product == self.products[0]:
            productPrice = 40
        if product == self.products[1]:
            productPrice = 80
        if product == self.products[2]:
            productPrice = 120
            
        if money >= productPrice:
            if self.stock[self.products.index(product)] == 0:
                self.stock[self.products.index(product)] = 144 * (1 + self.products.index(product))
                money -= int(productPrice)
        else:
            popupText = "Not enough money!"
            menuOpen = True

    def sell(self):
        global money
        global timer

        for floor in Floors:
            if isinstance(floor, CommercialFloor):
                for i in range(len(floor.stock)):
                    if floor.stock[i] > 0:
                        if i == 0 and timer % 300 == 0: # sell every 5 seconds
                            money += 12
                            floor.stock[i] -= 1
                        if i == 1 and timer % 600 == 0: # sell every 10 seconds
                            money += 12
                            floor.stock[i] -= 1 
                        if i == 2 and timer % 900 == 0: # sell every 15 seconds
                            money += 12
                            floor.stock[i] -= 1
        timer += 1

class LobbyFloor(Floor):
    def __init__(self, floor_number):
        super().__init__(floor_number)
        self.floor_color = (0, 0, 255)
        self.title = "Lobby"
        
        # create image for lobby floor
        self.image = pygame.Surface((self.floor_width, self.floor_height))
        self.image.fill((0, 0, 255))
        for image in range(len(lobbyImages)):
            self.image.blit(lobbyImages[image], (0, 0))
            # create colour pickers for each lobby image and store in 2d list with image
            lobbyImages[image] = [lobbyImages[image], ColourPicker(70, 270 + (image * 40))]

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

def randomizeCitizen(homeFloor):
    clothes = random.choice(["clothes1", "clothes2", "clothes3", "clothes4", "clothes5", "clothes6", "clothes7", "clothes8", "clothes9", "clothes10"])
    hair = random.choice(["hair1", "hair2", "hair3", "hair4", "hair5", "hair6", "hair7", "hair8", "hair9", "hair10", "hair11", "hair12", "hair13", "hair14", "hair15", "hair16", "hair17"])
    eyes = random.choice(["eyes1", "eyes2", "eyes3", "eyes4"])
    skin = random.choice(["skin1", "skin2", "skin3", "skin4", "skin5", "skin6", "skin7", "skin8"])

    appearance = CitizenAppearance(clothes, hair, eyes, skin)

    name = random.choice(firstNames) + " " + random.choice(lastNames)

    return Citizen(name, 0, homeFloor, appearance)

def shiftHue(surface, hue):
    # with thanks to https://stackoverflow.com/questions/7274221/changing-image-hue-with-python-pil
    arr = pygame.surfarray.pixels3d(surface)
    hsv = rgb_to_hsv(arr)
    hsv[..., 0] = hue
    rgb = hsv_to_rgb(hsv)
    return pygame.surfarray.make_surface(rgb)


def CitizenPicker():
    global showCitizenList
    global menuOpen
    global selectedCitizen
    global citizenListPurpose
    global floorToEmploy
    global popupText
    global citizenProperties
    
    # opens a list of citizens and returns a citizen object from user selection
    sortedList = []
    if sortList == "job":
        sortedList = Citizens
    elif sortList == "alphabetical":
        sortedList = alphaSort(Citizens)
    elif sortList == "home":
        sortedList = homeSort(Citizens)

    citizenListMenu.fadeIn(root)

    for i in range(len(sortedList)):
        pygame.draw.rect(root, (255, 255, 255), (10, 100 + (i * 50), 330, 50))
        pygame.draw.rect(root, (0, 0, 0), (10, 100 + (i * 50), 330, 50), 4)

        sortedList[i].draw(root, 15, 110 + (i * 50))

        text = font.render(sortedList[i].name, True, (0, 0, 0))
        root.blit(text, (70, 110 + (i * 50)))

        root.blit(pygame.image.load("images/houseicon.png"), (260, 110 + (i * 50)))
        text = smallfont.render(str(sortedList[i].homeFloor), True, (0, 0, 0))
        root.blit(text, (290, 110 + (i * 50)))

        root.blit(pygame.image.load("images/workicon.png"), (260, 125 + (i * 50)))
        text = smallfont.render(str(sortedList[i].jobFloor), True, (0, 0, 0))
        root.blit(text, (290, 125 + (i * 50)))

        # make each citizen item clickable with a button
        if Button(10, 100 + (i * 50), 330, 50).is_clicked(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if citizenListPurpose == "manage":
                showCitizenList = False
                menuOpen = False
                citizenListPurpose = ""
                citizenProperties = sortedList[i]
            if citizenListPurpose == "employ":
                # check if citizen is already employed
                if sortedList[i].jobFloor != 0:
                    popupText = sortedList[i].name + " is already employed!"
                    showCitizenList = False
                    menuOpen = False
                    citizenListPurpose = ""
                else:
                    selectedCitizen = sortedList[i]
                    showCitizenList = False
                    menuOpen = False
                    citizenListPurpose = ""
                    # unassign previous employee
                    if floorToEmploy.employee != None:
                        floorToEmploy.employee.jobFloor = 0
                        floorToEmploy.employee = None
                    floorToEmploy.employee = selectedCitizen
                    selectedCitizen.jobFloor = floorToEmploy.floor_number
                    floorToEmploy = None
                    popupText = selectedCitizen.name + " has been hired!"

    if sortList == "job":
        root.blit(pygame.image.load("images/jobbuttonpushed.png"), (177.5, 47.5))
    elif sortList == "alphabetical":
        root.blit(pygame.image.load("images/alphabetbuttonpushed.png"), (227.5, 47.5))
    elif sortList == "home":
        root.blit(pygame.image.load("images/housebuttonpushed.png"), (277.5, 47.5))

Floors = [LobbyFloor(0)]
Citizens = []
citizenProperties = Citizen("placeholder", 0, 0, CitizenAppearance("clothes1", "hair1", "eyes1", "skin1"))

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
        Button(150, 180, 50, 50, bgImage=pygame.image.load("images/placeholderbox.png"))
    ])

    citizenListMenu = Menu(0, 0, pygame.image.load("images/purplebg.png"), [
        Button(10, 50, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png")),
        Text(70, 55, "Sort by:", (255, 255, 255)),
        Button(177.5, 47.5, 30, 30, (255, 255, 255), bgImage=pygame.image.load("images/jobbutton.png")),
        Button(227.5, 47.5, 30, 30, (255, 255, 255), bgImage=pygame.image.load("images/alphabetbutton.png")),
        Button(277.5, 47.5, 30, 30, (255, 255, 255), bgImage=pygame.image.load("images/housebutton.png")),
    ])
    
    popupMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Text(75, 140, popupLine1, (255, 255, 255)),
        Text(75, 160, popupLine2, (255, 255, 255)),
        Text(75, 180, popupLine3, (255, 255, 255)),
        Text(75, 200, popupLine4, (255, 255, 255)),
        Button(100, 260, 150, 50, (0, 255, 0), bgImage=pygame.image.load("images/okbutton.png")),
    ])

    floorArrowsMenu = Menu(50, 120, pygame.image.load("images/buttonholder.png"), [
        Button(69, 137, 98, 83, (255, 255, 255), bgImage=pygame.image.load("images/uparrow.png")),
        Button(179, 137, 98, 83, (255, 255, 255), bgImage=pygame.image.load("images/downarrow.png")),
        Button(100, 250, 150, 50, (255, 255, 255), bgImage=pygame.image.load("images/okbutton.png")),
    ])

    citizenPropertiesMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        Button(75, 140, 35, 35, (255, 255, 255), bgImage=pygame.image.load("images/closebutton.png")),
        Text(130, 145, citizenProperties.name, (255, 255, 255)),
        Button(100, 260, 50, 50, (255, 0, 0), bgImage=pygame.image.load("images/evict.png")),
        Button(200, 260, 50, 50, (255, 0, 0), bgImage=pygame.image.load("images/relocate.png")),
    ])

    confirmEvictMenu = Menu(50, 110, pygame.image.load("images/boxwindow.png"), [
        smallText(75, 140, "Evict " + citizenProperties.name + "?", (255, 255, 255)),
        Button(100, 260, 50, 50, (0, 255, 0), bgImage=pygame.image.load("images/yes.png")),
        Button(200, 260, 50, 50, (255, 0, 0), bgImage=pygame.image.load("images/no.png")),
    ])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONUP:
            if not showArrows:
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
                            citizenListPurpose = "manage"
                            showCitizenList = True
                            break
                            
                if showFloorButtons:
                    for button in range(len(newFloorMenu.buttons)):
                        if newFloorMenu.buttons[button].is_clicked(pos):
                            if button == 0:
                                if money >= newFloorPrice:
                                    Floors.append(ResidentialFloor(len(Floors), random.choice(floorImages), random.choice(residentialNames)))
                                    money -= newFloorPrice
                                    # set new floor price to 1.2x the cost of the last floor
                                    newFloorPrice = int(newFloorPrice * 1.2)
                                    showFloorButtons = False
                                    menuOpen = False
                                    if tutorialState == 1:
                                        tutorialState = 2
                                else:
                                    showFloorButtons = False
                                    popupText = "Not enough money!"
                            if button == 1:
                                if tutorialState != 1:
                                    if money >= newFloorPrice:
                                        randomFloorType = random.choice(commercialFloorTypes)
                                        randomFloorType = randomFloorType[0]
                                        Floors.append(CommercialFloor(len(Floors), randomFloorType))
                                        money -= newFloorPrice
                                        # set new floor price to 1.2x the cost of the last floor
                                        newFloorPrice = int(newFloorPrice * 1.2)
                                        showFloorButtons = False
                                        menuOpen = False
                                    else:
                                        menuOpen = True
                                        popupText = "Not enough money!"
                                        showFloorButtons = False
                                else:
                                    popupText = "Finish the tutorial first!"
                                    showFloorButtons = False
                            if button == 2:
                                showFloorButtons = False
                                menuOpen = False
                        
                    break
                            
                if popupText != "":
                    menuOpen = True
                    if popupMenu.buttons[4].is_clicked(pos):
                        popupText = ""
                        menuOpen = False
                        break

                if showNewCitizen and not showArrows:
                    if newCitizenMenu.buttons[0].is_clicked(pos) and not menuOpen:
                        showArrows = True
                        menuOpen = True
                        selectedFloor = 0
                        citizenInElevator = randomizeCitizen(selectedFloor)
                        break

                if showArrows:
                    if floorArrowsMenu.buttons[0].is_clicked(pos): # up arrow
                        if selectedFloor < len(Floors) - 1:
                            selectedFloor += 1
                            scrollY = (Floors[selectedFloor].floor_height + BAR_HEIGHT)* Floors[selectedFloor].floor_number
                    if floorArrowsMenu.buttons[1].is_clicked(pos): # down arrow
                        if selectedFloor > 0:
                            selectedFloor -= 1
                            scrollY = (Floors[selectedFloor].floor_height + BAR_HEIGHT)* Floors[selectedFloor].floor_number
                        
                    if floorArrowsMenu.buttons[2].is_clicked(pos):
                        if isinstance(Floors[selectedFloor], CommercialFloor):
                            popupText = "Citizens can't live on commercial floors!"
                            # put citizen back on home floor if they have one
                            if citizenInElevator.homeFloor != 0:
                                Floors[citizenInElevator.homeFloor].occupants.append(citizenInElevator)
                                Citizens.append(citizenInElevator)
                                citizenInElevator = None

                        if selectedFloor != 0 and isinstance(Floors[selectedFloor], ResidentialFloor):
                            if len(Floors[selectedFloor].occupants) < 3:
                                Floors[selectedFloor].occupants.append(citizenInElevator) # add citizen to floor
                                Citizens.append(Floors[selectedFloor].occupants[-1])
                                # set citizen's home floor to selected floor
                                Floors[selectedFloor].occupants[-1].homeFloor = selectedFloor
                                popupText = Floors[selectedFloor].occupants[-1].name + " has moved in!"
                                citizenInElevator = None
                            else:
                                popupText = "This floor is full!"
                                if citizenInElevator.homeFloor != 0:
                                    Floors[citizenInElevator.homeFloor].occupants.append(citizenInElevator)
                                    Citizens.append(citizenInElevator)
                                citizenInElevator = None
                        
                        if selectedFloor == 0:
                            popupText = "Citizens can't live on the lobby floor!"
                            if citizenInElevator.homeFloor != 0:
                                Floors[citizenInElevator.homeFloor].occupants.append(citizenInElevator)
                                Citizens.append(citizenInElevator)
                                
                            citizenInElevator = None
                        
                        showArrows = False
                        showNewCitizen = False
                        selectedFloor = None
                        break

                # floor management menu
                for floor in Floors:
                    if floor.is_clicked(scrollpos) and not menuOpen:
                        delayCounter = pygame.time.get_ticks()
                        floorMenu = floor.floor_number
                        menuOpen = True
                        break

                if floorMenu != -1 and delayCounter + 50 < pygame.time.get_ticks():
                    for button in range(len(manageFloorMenu.buttons)):
                        if manageFloorMenu.buttons[button].is_clicked(pos):
                            if button == 0:
                                floorMenu = -1
                                menuOpen = False

                            if isinstance(Floors[floorMenu], ResidentialFloor):
                                if button == 2:
                                    # show citizen properties if placeholder box not empty
                                    if len(Floors[floorMenu].occupants) > 0:
                                        menuOpen = False
                                        delayCounter = pygame.time.get_ticks()
                                        citizenProperties = Floors[floorMenu].occupants[0]
                                        floorMenu = -1
                                        break

                                if button == 3:
                                    if len(Floors[floorMenu].occupants) > 1:
                                        menuOpen = False
                                        delayCounter = pygame.time.get_ticks()
                                        citizenProperties = Floors[floorMenu].occupants[1]
                                        floorMenu = -1
                                        break

                                if button == 4:
                                    if len(Floors[floorMenu].occupants) > 2:
                                        menuOpen = False
                                        delayCounter = pygame.time.get_ticks()
                                        citizenProperties = Floors[floorMenu].occupants[2]
                                        floorMenu = -1
                                        break

                            if isinstance(Floors[floorMenu], CommercialFloor):
                                if button == 2:
                                    if Floors[floorMenu].employee != None:
                                        Floors[floorMenu].restock(Floors[floorMenu].products[0])
                                    else:
                                        popupText = "You can't restock a floor without an employee!"
                                        menuOpen = True
                                if button == 3:
                                    if Floors[floorMenu].employee != None:
                                        Floors[floorMenu].restock(Floors[floorMenu].products[1])
                                    else:
                                        popupText = "You can't restock a floor without an employee!"
                                        menuOpen = True
                                if button == 4:
                                    if Floors[floorMenu].employee != None:
                                        Floors[floorMenu].restock(Floors[floorMenu].products[2])
                                        menuOpen = True
                                    else:
                                        popupText = "You can't restock a floor without an employee!"
                                if button == 5: # pick citizen to work here
                                    showCitizenList = True
                                    menuOpen = True
                                    citizenListPurpose = "employ"
                                    floorToEmploy = Floors[floorMenu]   

                                if tutorialState == 3:
                                    tutorialState = 4

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

                # citizen properties menu
                if citizenProperties.name != "placeholder" and delayCounter + 50 < pygame.time.get_ticks():
                    for button in range(len(citizenPropertiesMenu.buttons)):
                        if citizenPropertiesMenu.buttons[button].is_clicked(pos) and floorMenu == -1 and not showConfirmEvictMenu:
                            if button == 0:
                                citizenProperties = Citizen("placeholder", 0, 0, CitizenAppearance("clothes1", "hair1", "eyes1", "skin1"))
                                menuOpen = False
                            if button == 2:
                                # evict citizen
                                menuOpen = True
                                showCitizenList = False
                                delayCounter = pygame.time.get_ticks()
                                showConfirmEvictMenu = True
                                break
                                
                            if button == 3:
                                # open arrows menu and select floor to relocate to
                                showArrows = True
                                menuOpen = True
                                selectedFloor = 0
                                citizenInElevator = citizenProperties # store citizen in elevator temporarily
                                Floors[citizenProperties.homeFloor].occupants.remove(citizenProperties)
                                Citizens.remove(citizenProperties)
                                citizenProperties = Citizen("placeholder", 0, 0, CitizenAppearance("clothes1", "hair1", "eyes1", "skin1"))
                                break

                # confirm evict menu
                if confirmEvictMenu.bgImage.get_alpha() == 255 and delayCounter + 50 < pygame.time.get_ticks() and showConfirmEvictMenu:
                    for button in range(len(confirmEvictMenu.buttons)):
                        if confirmEvictMenu.buttons[button].is_clicked(pos):
                            if button == 1:
                                Floors[citizenProperties.homeFloor].occupants.remove(citizenProperties)
                                Citizens.remove(citizenProperties)
                                citizenProperties = Citizen("placeholder", 0, 0, CitizenAppearance("clothes1", "hair1", "eyes1", "skin1"))
                                menuOpen = False
                                showConfirmEvictMenu = False
                            if button == 2:
                                menuOpen = False
                                showConfirmEvictMenu = False
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
            if isinstance(floor, LobbyFloor):
                for image in range(len(lobbyImages)):
                    root.blit(lobbyImages[image][0], (floor.floor_x, floor.floor_y + scrollY))
                    

        root.blit(elevatorImage, (floor.floor_x, floor.floor_y + scrollY))

        # draw floor title bar above floor
        if selectedFloor != floor.floor_number:
            pygame.draw.rect(root, (0, 0, 0), (floor.floor_x, floor.floor_y + scrollY - BAR_HEIGHT, floor.floor_width, BAR_HEIGHT))
        else:
            pygame.draw.rect(root, (0, 255, 0), (floor.floor_x, floor.floor_y + scrollY - BAR_HEIGHT, floor.floor_width, BAR_HEIGHT))

        # draw mini square stock bar for each product on right of floor title bar, horizontally
        if isinstance(floor, CommercialFloor):
            for product in range(len(floor.products)):
                pygame.draw.rect(root, (255, 255, 255), (floor.floor_x + floor.floor_width - 20 - (product * 15), floor.floor_y + scrollY - BAR_HEIGHT + 7, 10, 10))
                pygame.draw.rect(root, (0, 255, 0), (floor.floor_x + floor.floor_width - 20 - (product * 15), floor.floor_y + scrollY - BAR_HEIGHT + 7, (floor.stock[product]/(144 * (product + 1)) * 10), 10))
                

        # draw floor number
        text = smallfont.render(str(floor.floor_number) + "  " + str(floor.title), True, (255, 255, 255))
        root.blit(text, (floor.floor_x + 10, floor.floor_y + scrollY + 3 - BAR_HEIGHT))

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
    if floorMenu != -1 and delayCounter + 50 < pygame.time.get_ticks():
        manageFloorMenu.draw(root)
        menuOpen = True
        if isinstance(Floors[floorMenu], CommercialFloor):
            Image(90, 240, pygame.image.load("images/products/" + Floors[floorMenu].products[0].name + ".png"))
            smallText(100, 310, str(Floors[floorMenu].stock[0]), (0, 0, 0)).draw(root)
            pygame.draw.rect(root, (255, 255, 255), (90, 300, 50, 10))
            pygame.draw.rect(root, (0, 255, 0), (90, 300, (Floors[floorMenu].stock[0]/144*50), 10))

            Image(150, 240, pygame.image.load("images/products/" + Floors[floorMenu].products[1].name + ".png"))
            smallText(160, 310, str(Floors[floorMenu].stock[1]), (0, 0, 0)).draw(root)
            pygame.draw.rect(root, (255, 255, 255), (150, 300, 50, 10))
            pygame.draw.rect(root, (0, 255, 0), (150, 300, (Floors[floorMenu].stock[1]/288*50), 10))

            Image(210, 240, pygame.image.load("images/products/" + Floors[floorMenu].products[2].name + ".png"))
            smallText(220, 310, str(Floors[floorMenu].stock[2]), (0, 0, 0)).draw(root)
            pygame.draw.rect(root, (255, 255, 255), (210, 300, 50, 10))
            pygame.draw.rect(root, (0, 255, 0), (210, 300, (Floors[floorMenu].stock[2]/432*50), 10))
            
            if Floors[floorMenu].employee != None:
                Floors[floorMenu].employee.draw(root, 160, 190)

            if tutorialState == 3:
                pygame.draw.rect(root, (255, 255, 255), (50, 390, 250, 65))
                pygame.draw.rect(root, (0, 0, 0), (50, 390, 250, 65), 4)
                smallText(60, 400, "Hire a citizen to work here by", (0, 0, 0)).draw(root)
                smallText(60, 420, "clicking the empty button.", (0, 0, 0)).draw(root)

            if tutorialState == 4:
                pygame.draw.rect(root, (255, 255, 255), (50, 390, 250, 65))
                pygame.draw.rect(root, (0, 0, 0), (50, 390, 250, 65), 4)
                smallText(60, 400, "Restock the floor by clicking", (0, 0, 0)).draw(root)
                smallText(60, 420, "the product buttons.", (0, 0, 0)).draw(root)

        if isinstance(Floors[floorMenu], ResidentialFloor):
            for i in range(len(Floors[floorMenu].occupants)):
                # place citizen images in each box 
                Floors[floorMenu].occupants[i].draw(root, 100 + (CitizenAppearance.CitizenSize * i * 2), 250)

            # hide empty button for commercial employee with cropped background
            root.blit(pygame.image.load("images/boxwindow.png"), (150, 180), (100, 70, 50, 50))
                

        if isinstance(Floors[floorMenu], LobbyFloor):
            root.blit(pygame.image.load("images/longwindow.png"), (51, 179))
            Text(75, 180, "Tower Stats", (255, 255, 255)).draw(root)
            smallText(75, 210, "Floors: " + str(len(Floors)), (255, 255, 255)).draw(root)
            smallText(75, 230, "Residents: " + str(len(Citizens)), (255, 255, 255)).draw(root)
            smallText(75, 250, "¢/sec: " + str(round(coinspersecond, 2)), (255, 255, 255)).draw(root)
            
            for picker in range(len(lobbyImages)):
                lobbyImages[picker][1].update()
                lobbyImages[picker][1].draw(root)
                
                # set image colour to picker colour
                lobbyImages[picker][0] = shiftHue(lobbyImages[picker][0], lobbyImages[picker][1].get_colour().hsva[0])
                lobbyImages[picker][0].set_colorkey((255, 255, 255))
                
    # draw popup
    if popupText != "":
        popupMenu.draw(root)
                
    # draw buttons
    for button in buttons:
        button.draw(root)

    if showNewCitizen:
        if tutorialState == 2:
            popupText = "There's a new citizen waiting! Click the elevator to move them in."
            tutorialState = 3
        silhouette = pygame.image.load("images/silhouette.png")
        silhouette = pygame.transform.scale(silhouette, (CitizenAppearance.CitizenSize, CitizenAppearance.CitizenSize))

        newCitizenMenu = Menu(25, 500 + scrollY, elevatorOpenImage, [
            Button(65, 550 + scrollY, CitizenAppearance.CitizenSize, CitizenAppearance.CitizenSize, bgImage=silhouette),
        ])

        newCitizenMenu.draw(root)
        
    if showCitizenList:
        CitizenPicker()

    if showArrows:
        floorArrowsMenu.draw(root)

    if citizenProperties.name != "placeholder" and delayCounter + 50 < pygame.time.get_ticks():
        menuOpen = True
        citizenPropertiesMenu.fadeIn(root)
        citizenProperties.draw(root, 160, 200)

    # menu bar items
    root.blit(pygame.image.load("images/coin.png"), (10, 12))
    text = font.render(str(round(money)), True, (255, 255, 255))
    root.blit(text, (35, 10))

    # draw scroll bar
    pygame.draw.rect(root, (200, 200, 200), (display_width - 5, (-scrollY / 10 + display_height - 50), 10, 50))

    if not menuOpen: # allow fading
        fading = False
        fadeAmount = 0

    if showFloorButtons:
        newFloorMenu.fadeIn(root)
        if tutorialState == 1:
            pygame.draw.rect(root, (255, 255, 255), (50, 390, 250, 65))
            pygame.draw.rect(root, (0, 0, 0), (50, 390, 250, 65), 4)
            smallText(60, 400, "Add a new residential floor", (0, 0, 0)).draw(root)
            smallText(60, 420, "to start bringing in citizens.", (0, 0, 0)).draw(root)



    if showConfirmEvictMenu and delayCounter + 50 < pygame.time.get_ticks():
        confirmEvictMenu.fadeIn(root)

    if tutorialState == 0:
        popupText = "Welcome! Click the + button to add a new floor."
        tutorialState = 1

    if tutorialState == 5 and tutorialEndTimer + 1000 < pygame.time.get_ticks():
        popupText = "Tip: Click on the lobby to customize its appearance."
        tutorialState = None

    # --- economy ---
    # collect rent every 2.5 seconds
    if tick % 150 == 0:
        for citizen in Citizens:
            money += 10

    # Always Be Closing
    for floor in Floors:
        if isinstance(floor, CommercialFloor) and floor.employee != None:
            floor.sell()

    # every 10 seconds, generate a new citizen
    if tick % 600 == 0 and tick != 0 and citizenInElevator == None and tutorialState != 1 and tutorialState != 0:
        showNewCitizen = True
        citizenInElevator = None
 
    profitFromCommercialPerSecond = 0
    for floor in Floors:
        if isinstance(floor, CommercialFloor):
            if floor.employee != None:
                for i in range(len(floor.stock)):
                    if i == 0:
                        if floor.stock[i] > 0:
                            # 12 coins / 5 seconds
                            profitFromCommercialPerSecond += 2.4
                    if i == 1:
                        if floor.stock[i] > 0:
                            # 12 coins / 10 seconds
                            profitFromCommercialPerSecond += 1.2
                    if i == 2:
                        if floor.stock[i] > 0:
                            # 12 coins / 15 seconds
                            profitFromCommercialPerSecond += 0.8
                    
    coinspersecond = 4 * len(Citizens) + profitFromCommercialPerSecond

    splitText()

    # update display
    pygame.display.update()
    clock.tick(FPS)
    tick += 1