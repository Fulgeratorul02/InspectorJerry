import pygame as py
import copy

py.init()
py.font.init()
py.mixer.init()
py.mixer.set_num_channels(2048)

Game_font=py.font.SysFont("Arial", 50)

displayHeight=900
displayWidth=1600

display=py.display.set_mode((displayWidth, displayHeight))
py.display.set_caption("Inspector Jerry")
py.display.set_icon(py.image.load("Box.png"))
display.fill((0,0,0))

sound_v=0.3
box_destroy_wav=py.mixer.Sound("Sounds/hitHurt.ogg")
box_destroy_wav.set_volume(sound_v)
powerUp_change_wav=py.mixer.Sound("Sounds/powerUp.ogg")
powerUp_change_wav.set_volume(sound_v)
pickUp_wav=py.mixer.Sound("Sounds/pickupCoin.ogg")
pickUp_wav.set_volume(sound_v)
move_wav=py.mixer.Sound("Sounds/jump.ogg")
move_wav.set_volume(sound_v)
button_wav=py.mixer.Sound("Sounds/blipSelect.ogg")
button_wav.set_volume(sound_v)
finish_wav=py.mixer.Sound("Sounds/random.ogg")
finish_wav.set_volume(sound_v)
boxDown_wav=py.mixer.Sound("Sounds/boxDown.ogg")
boxDown_wav.set_volume(sound_v)

grid_size=75

actualBackGround=py.transform.smoothscale(
    py.image.load("Improved_assets/Background.png").convert_alpha(), (1600, 900))
menuBackGround=py.transform.smoothscale(
    py.image.load("Improved_assets/Menu BackGround.png").convert_alpha(), (1600, 900))

backGroundPink=py.transform.smoothscale(
    py.image.load("Improved_assets/Jelly_Space_Pink.png").convert_alpha(), (grid_size, grid_size))
backGroundGreen=py.transform.smoothscale(
    py.image.load("Improved_assets/Jelly_Space_Green.png").convert_alpha(), (grid_size, grid_size))
backGroundBlue=py.transform.smoothscale(
    py.image.load("Improved_assets/Jelly_Space_Blue.png").convert_alpha(), (grid_size, grid_size))
selectedBackGround=backGroundPink

playerX=100
playerY=100
player=py.Rect(playerX,playerY,grid_size,grid_size)
player_image=py.transform.smoothscale(
    py.image.load("Improved_assets/Jelly_Player.png").convert_alpha(), (grid_size, grid_size))

pushableX=500
pushableY=500
pushable=py.Rect(pushableX, pushableY, grid_size, grid_size)
box_image=py.transform.smoothscale(
    py.image.load("Improved_assets/Shipping_Box.png").convert_alpha(), (grid_size, grid_size))

spaceX=0
spaceY=0
space=py.Rect(spaceX, spaceY, grid_size, grid_size)
wall_image_blue=py.transform.smoothscale(
    py.image.load("Improved_assets/Jelly_Spikes_Blue.png"), (grid_size, grid_size))
wall_image_pink=py.transform.smoothscale(
    py.image.load("Improved_assets/Jelly_Spikes_Pink.png").convert_alpha(), (grid_size, grid_size))
wall_image_green=py.transform.smoothscale(
    py.image.load("Improved_assets/Jelly_Spikes_Green.png").convert_alpha(), (grid_size, grid_size))
sword_image=py.transform.smoothscale(
    py.image.load("Improved_assets/Power_Up.png").convert_alpha(), (grid_size, grid_size))

finishX=0
finishY=0
finish=py.Rect(finishX, finishY, grid_size, grid_size)
finish_image=py.transform.smoothscale(
    py.image.load("Improved_assets/Finish_Iten.png").convert_alpha(), (grid_size, grid_size))

powerGX=0
powerGY=0
powerG=py.Rect(powerGX, powerGY, 600, 100)
powerG1_image=py.transform.smoothscale(
    py.image.load("Improved_assets/Power_G1.png").convert_alpha(), (600, 100))
powerG2_image=py.transform.smoothscale(
    py.image.load("Improved_assets/Power_G2.png").convert_alpha(), (600, 100))
powerG_show=0

titleX=800
titleY=200
title=py.Rect(titleX, titleY, 800, 200)
title_image=py.transform.smoothscale(
    py.image.load("Improved_assets/Title.png").convert_alpha(), (800, 200))

thanksX=0
thanksY=0
thanks=py.Rect(thanksX, thanksY, 1000, 800)
thanks_image=py.transform.smoothscale(
    py.image.load("Improved_assets/Thanks.png").convert_alpha(), (1200, 400))

charX=800
charY=450
char=py.Rect(charX, charY, 75, 75)
char_image=py.transform.smoothscale(
    py.image.load("Improved_assets/Jelly_Player.png").convert_alpha(), (175, 175))
char_rotate=0

char_cage_image=py.transform.smoothscale(
    py.image.load("Improved_assets/char_cage.png").convert_alpha(), (1600, 900))

buttonX=300
buttonY=700
button=py.Rect(buttonX, buttonY, 100, 600)
button_image_pressed_menu=py.transform.smoothscale(
    py.image.load("Improved_assets/button_pressed_menu.png").convert_alpha(), (600, 200))
button_image_unpressed_menu=py.transform.smoothscale(
    py.image.load("Improved_assets/button_unpressed_menu.png").convert_alpha(), (600, 200))
button_image_pressed_start=py.transform.smoothscale(
    py.image.load("Improved_assets/button_pressed_start.png").convert_alpha(), (600, 200))
button_image_unpressed_start=py.transform.smoothscale(
    py.image.load("Improved_assets/button_unpressed_start.png").convert_alpha(), (600, 200))

button_unpressed=py.transform.smoothscale(
    py.image.load("Improved_assets/button_unpressed.png").convert_alpha(), (150, 150))


#0-empty, 1-walls, 2-player, 3-box, 4-sword power up, 5-finish square, 6-empty jumpable space;

map_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],           #playing map
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,3,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,5,0,1],
            [1,0,2,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,4,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]]

Test1_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],           #test level
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,3,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,2,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,4,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]]

empty_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,0,0,0,0,0,0,0,0,0,0,1],
              [1,0,0,0,0,0,0,0,0,0,0,1],
              [1,0,0,0,0,0,0,0,0,0,0,1],
              [1,0,0,0,0,0,0,0,0,0,0,1],
              [1,0,0,0,0,0,0,0,0,0,0,1],
              [1,0,0,0,0,0,0,0,0,0,0,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level11_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,1,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,1,1,1,1,1,0,1],
            [1,0,1,0,1,0,0,0,0,1,0,1],
            [1,0,1,0,1,0,1,1,0,3,0,1],
            [1,0,1,0,1,0,1,1,0,3,0,1],
            [1,0,0,0,1,5,1,0,0,3,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]]

Level12_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,1,1,1,1,1,0,3,3,0,1],
            [1,3,0,0,0,0,1,3,0,0,3,1],
            [1,0,3,1,0,1,1,0,0,0,3,1],
            [1,3,0,1,0,1,1,0,0,3,0,1],
            [1,1,0,1,3,5,1,0,3,0,0,1],
            [1,2,3,0,0,1,1,3,3,3,3,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]]

Level13_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,0,0,0,3,1,1,1,1],
            [1,1,1,1,3,3,0,0,1,1,1,1],
            [1,1,1,1,0,3,0,0,0,0,5,1],
            [1,2,0,0,3,0,0,3,1,1,1,1],
            [1,1,1,1,0,3,3,0,1,1,1,1],
            [1,1,1,1,0,3,0,0,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]]

Level14_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,0,0,3,0,0,0,0,0,1,0,1],
              [1,0,0,3,0,3,0,1,0,0,0,1],
              [1,0,1,3,1,3,1,1,3,0,3,1],
              [1,5,1,3,3,3,3,1,0,3,0,1],
              [1,1,1,0,0,3,0,0,1,0,1,1],
              [1,2,0,3,0,3,0,0,0,0,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level15_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,0,1,0,1,1,0,0,3,0,5,1],
              [1,0,0,3,3,1,3,0,3,0,1,1],
              [1,3,3,0,0,1,0,1,0,3,0,1],
              [1,0,0,3,0,0,0,1,1,3,1,1],
              [1,1,0,1,1,3,1,2,1,0,5,1],
              [1,0,0,0,3,0,0,0,1,0,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level21_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,1,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,1,1,1,1,1,0,1],
            [1,0,1,0,1,0,0,0,0,1,0,1],
            [1,0,1,4,1,0,1,1,0,1,0,1],
            [1,0,1,0,1,0,1,1,0,3,0,1],
            [1,0,0,0,1,5,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1]]

Level22_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,2,1,0,0,0,3,0,0,3,0,1],
              [1,4,1,3,3,3,0,3,3,0,3,1],
              [1,4,1,0,0,3,0,0,3,3,4,1],
              [1,0,3,0,1,0,3,0,0,3,0,1],
              [1,1,1,3,1,1,1,1,1,1,1,1],
              [1,4,3,0,0,0,0,3,0,0,5,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level23_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,2,4,1,0,0,0,1,6,0,5,1],
              [1,4,4,1,0,1,0,6,6,6,6,1],
              [1,4,0,1,6,4,6,4,1,0,6,1],
              [1,0,6,1,0,1,0,0,1,6,4,1],
              [1,6,0,1,0,1,0,6,0,0,4,1],
              [1,0,0,0,0,1,1,0,6,0,0,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level24_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,6,0,6,4,4,1,0,0,0,1],
                [1,6,1,1,4,4,0,1,6,1,6,1],
                [1,0,1,4,4,1,6,3,0,1,0,1],
                [1,4,1,6,1,2,4,1,6,1,6,1],
                [1,4,1,0,0,1,1,1,0,1,0,1],
                [1,4,0,6,0,6,0,6,0,1,5,1],
                [1,1,1,1,1,1,1,1,1,1,1,1]]

Level25_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,1,2,3,0,6,0,5,1,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level31_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,2,6,6,6,0,6,0,6,6,5,1],
              [1,4,6,0,0,0,0,0,6,6,6,1],
              [1,4,6,6,0,6,6,0,6,6,0,1],
              [1,4,6,6,0,6,6,0,6,6,0,1],
              [1,4,6,6,3,6,0,0,0,0,0,1],
              [1,0,0,0,0,6,6,6,0,6,0,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level32_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,0,4,0,1,0,4,6,0,6,5,1],
              [1,3,0,0,1,6,1,4,0,6,0,1],
              [1,0,1,3,1,4,1,1,1,1,1,1],
              [1,0,3,0,6,2,6,0,4,4,0,1],
              [1,6,1,1,1,1,1,3,0,0,3,1],
              [1,0,6,0,0,5,1,0,3,3,0,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level33_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,2,4,0,0,0,0,0,0,0,0,1],
              [1,6,6,6,6,6,6,6,6,6,0,1],
              [1,0,0,6,0,6,0,6,5,6,0,1],
              [1,0,6,0,6,0,3,0,6,6,0,1],
              [1,0,6,6,6,6,6,6,6,6,0,1],
              [1,0,0,0,0,0,0,0,0,0,0,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level34_matrix=[[1,1,1,1,1,1,1,1,1,1,1,1],
              [1,2,1,5,3,4,6,0,3,0,1,1],
              [1,4,1,0,1,0,0,3,0,6,3,1],
              [1,3,1,3,1,0,3,0,1,3,0,1],
              [1,6,1,0,3,6,0,1,0,3,0,1],
              [1,3,1,1,1,1,1,1,1,1,3,1],
              [1,6,3,6,3,6,3,6,3,6,0,1],
              [1,1,1,1,1,1,1,1,1,1,1,1]]

Level35_matrix=[[1,1,1,1,1],
                [1,2,0,5,1],
                [1,1,1,1,1]]

spacingX=(displayWidth-len(map_matrix[1])*grid_size)//2
spacingY=(displayHeight-len(map_matrix)*grid_size)//2

game_run = True
powerUp_ctr = 0
powerUp_use = 0

class button:
    def __init__(self, x, y, unpressed_image, chapter, number):
        self.x=x
        self.y=y
        self.image=unpressed_image
        self.rect=self.image.get_rect()
        self.rect.topleft = (x, y)
        self.chapter=chapter
        self.number=number
        self.clicked=False

    def draw(self):
        leveled=False
        n=Game_font.render(self.number, True, (0, 0, 0))
        nRect=n.get_rect()
        nRect.center=(self.x+75, self.y+75)
        if self.rect.collidepoint(py.mouse.get_pos()[0], py.mouse.get_pos()[1]):
            if py.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                leveled=True
            if py.mouse.get_pressed()[0] == 0:
                self.clicked=False

        display.blit(self.image, (self.rect.x, self.rect.y))
        display.blit(n, nRect)

        return leveled

b11=button(350, 75, button_unpressed, 1, "1")
b12=button(600, 75, button_unpressed, 1, "2")
b13=button(850, 75, button_unpressed, 1, "3")
b14=button(1100, 75, button_unpressed, 1, "4")
b15=button(1350, 75, button_unpressed, 1, "5")

b21=button(350, 375, button_unpressed, 2, "1")
b22=button(600, 375, button_unpressed, 2, "2")
b23=button(850, 375, button_unpressed, 2, "3")
b24=button(1100, 375, button_unpressed, 2, "4")
b25=button(1350, 375, button_unpressed, 2, "5")

b31=button(350, 675, button_unpressed, 3, "1")
b32=button(600, 675, button_unpressed, 3, "2")
b33=button(850, 675, button_unpressed, 3, "3")
b34=button(1100, 675, button_unpressed, 3, "4")
b35=button(1350, 675, button_unpressed, 3, "5")

def playerMove(player, key):
    global showed_screen
    global powerUp_use
    i=(player.y-spacingY)//grid_size
    j=(player.x-spacingX)//grid_size
    if powerUp_use==0:
        if key == py.K_d:
            if map_matrix[i][j+1] == 0:
                map_matrix[i][j], map_matrix[i][j+1] = 0, map_matrix[i][j]
                py.mixer.Sound.play(move_wav)
            if map_matrix[i][j+1] == 3:
                if map_matrix[i][j+2]==0:
                    map_matrix[i][j+2]=3
                    map_matrix[i][j+1]=2
                    map_matrix[i][j]=0
                    py.mixer.Sound.play(move_wav)
                if map_matrix[i][j+2]==6:
                    map_matrix[i][j+2]=0
                    map_matrix[i][j+1]=2
                    map_matrix[i][j]=0
                    py.mixer.Sound.play(boxDown_wav)
            if map_matrix[i][j+1] == 4:
                map_matrix[i][j], map_matrix[i][j + 1] = 0, map_matrix[i][j]
                py.mixer.Sound.play(pickUp_wav)
                return 1
            if map_matrix[i][j+1] == 5:
                map_matrix[i][j], map_matrix[i][j + 1] = 0, map_matrix[i][j]
                showed_screen=1
                py.mixer.Sound.play(finish_wav)

        if key == py.K_a:
            if map_matrix[i][j - 1] == 0:
                map_matrix[i][j], map_matrix[i][j - 1] = 0, map_matrix[i][j]
                py.mixer.Sound.play(move_wav)
            if map_matrix[i][j - 1] == 3:
                if map_matrix[i][j - 2] == 0:
                    map_matrix[i][j - 2] = 3
                    map_matrix[i][j - 1] = 2
                    map_matrix[i][j] = 0
                    py.mixer.Sound.play(move_wav)
                if map_matrix[i][j - 2] == 6:
                    map_matrix[i][j - 2] = 0
                    map_matrix[i][j - 1] = 2
                    map_matrix[i][j] = 0
                    py.mixer.Sound.play(boxDown_wav)
            if map_matrix[i][j - 1] == 4:
                map_matrix[i][j], map_matrix[i][j - 1] = 0, map_matrix[i][j]
                py.mixer.Sound.play(pickUp_wav)
                return 1
            if map_matrix[i][j-1] == 5:
                map_matrix[i][j], map_matrix[i][j - 1] = 0, map_matrix[i][j]
                showed_screen=1
                py.mixer.Sound.play(finish_wav)

        if key == py.K_s:
            if map_matrix[i+1][j] == 0:
                map_matrix[i][j], map_matrix[i+1][j] = 0, map_matrix[i][j]
                py.mixer.Sound.play(move_wav)
            if map_matrix[i+1][j] == 3:
                if map_matrix[i+2][j] == 0:
                    map_matrix[i+2][j] = 3
                    map_matrix[i+1][j] = 2
                    map_matrix[i][j] = 0
                    py.mixer.Sound.play(move_wav)
                if map_matrix[i+2][j] == 6:
                    map_matrix[i+2][j] = 0
                    map_matrix[i+1][j] = 2
                    map_matrix[i][j] = 0
                    py.mixer.Sound.play(boxDown_wav)
            if map_matrix[i+1][j] == 4:
                map_matrix[i][j], map_matrix[i+1][j] = 0, map_matrix[i][j]
                py.mixer.Sound.play(pickUp_wav)
                return 1
            if map_matrix[i+1][j] == 5:
                map_matrix[i][j], map_matrix[i+1][j] = 0, map_matrix[i][j]
                showed_screen=1
                py.mixer.Sound.play(finish_wav)

        if key == py.K_w:
            if map_matrix[i - 1][j] == 0:
                map_matrix[i][j], map_matrix[i-1][j] = 0, map_matrix[i][j]
                py.mixer.Sound.play(move_wav)
            if map_matrix[i - 1][j] == 3:
                if map_matrix[i - 2][j] == 0:
                    map_matrix[i - 2][j] = 3
                    map_matrix[i - 1][j] = 2
                    map_matrix[i][j] = 0
                    py.mixer.Sound.play(move_wav)
                if map_matrix[i - 2][j] == 6:
                    map_matrix[i - 2][j] = 0
                    map_matrix[i - 1][j] = 2
                    map_matrix[i][j] = 0
                    py.mixer.Sound.play(boxDown_wav)
            if map_matrix[i - 1][j] == 4:
                map_matrix[i][j], map_matrix[i-1][j] = 0, map_matrix[i][j]
                py.mixer.Sound.play(pickUp_wav)
                return 1
            if map_matrix[i-1][j] == 5:
                map_matrix[i][j], map_matrix[i-1][j] = 0, map_matrix[i][j]
                showed_screen=1
                py.mixer.Sound.play(finish_wav)
    else:
        if key == py.K_d:
            if map_matrix[i][j+1]!=1:
                if map_matrix[i][j+2]==0:
                    map_matrix[i][j]=0
                    map_matrix[i][j+2]=2
                    if map_matrix[i][j+1]==3:
                        py.mixer.Sound.play(box_destroy_wav)
                        map_matrix[i][j+1]=0
                    powerUp_use=1-powerUp_use
                    return -1
        if key == py.K_a:
            if map_matrix[i][j-1]!=1:
                if map_matrix[i][j-2]==0:
                    map_matrix[i][j]=0
                    map_matrix[i][j-2]=2
                    if map_matrix[i][j-1]==3:
                        py.mixer.Sound.play(box_destroy_wav)
                        map_matrix[i][j-1]=0
                    powerUp_use = 1 - powerUp_use
                    return -1
        if key == py.K_s:
            if map_matrix[i+1][j]!=1:
                if map_matrix[i+2][j]==0:
                    map_matrix[i][j]=0
                    map_matrix[i+2][j]=2
                    if map_matrix[i+1][j]==3:
                        py.mixer.Sound.play(box_destroy_wav)
                        map_matrix[i+1][j]=0
                    powerUp_use = 1 - powerUp_use
                    return -1
        if key == py.K_w:
            if map_matrix[i-1][j]!=1:
                if map_matrix[i-2][j]==0:
                    map_matrix[i][j]=0
                    map_matrix[i-2][j]=2
                    if map_matrix[i-1][j]==3:
                        py.mixer.Sound.play(box_destroy_wav)
                        map_matrix[i-1][j]=0
                    powerUp_use = 1 - powerUp_use
                    return -1
    return 0

def title_screen():
    global selected_level
    global game_run
    global char_rotate
    global char_image
    global showed_screen
    global map_matrix

    display.fill((125, 0, 255))
    display.blit(actualBackGround, py.Rect(0, 0, 1600, 900))

    titleX=400
    titleY=50
    title=py.Rect(titleX, titleY, 800, 200)
    display.blit(title_image, title)

    charX = 675
    charY = 325
    char = py.Rect(charX, charY, 75, 75)
    char_rotate -=0.5
    char_im=py.transform.rotate(char_image, char_rotate)

    display.blit(char_cage_image, py.Rect(0, 0, 1600, 900))
    display.blit(char_im, char)

    button1X=100
    button1Y=600
    button1=py.Rect(button1X, button1Y, 600, 200)
    if button1.collidepoint(py.mouse.get_pos()[0], py.mouse.get_pos()[1]):
        display.blit(button_image_pressed_start, button1)
    else:
        display.blit(button_image_unpressed_start, button1)

    button1X = 890
    button1Y = 600
    button2 = py.Rect(button1X, button1Y, 600, 200)
    if button2.collidepoint(py.mouse.get_pos()[0], py.mouse.get_pos()[1]):
        display.blit(button_image_pressed_menu, button2)
    else:
        display.blit(button_image_unpressed_menu, button2)

    for e in py.event.get():
        if e.type == py.QUIT:
            game_run = False
            py.quit()
            exit()
        if e.type == py.MOUSEBUTTONDOWN:
            if e.button == 1:
                if button1.collidepoint(py.mouse.get_pos()[0], py.mouse.get_pos()[1]):
                    selected_level=Level11_matrix
                    map_matrix = copy.deepcopy(selected_level)
                    showed_screen=2
                    py.mixer.Sound.play(button_wav)
                if button2.collidepoint(py.mouse.get_pos()[0], py.mouse.get_pos()[1]):
                    showed_screen=1
                    py.mixer.Sound.play(button_wav)


    py.display.update()
    py.time.Clock().tick(60)

def level_select():
    global selected_level
    global game_run
    global showed_screen
    global map_matrix
    global color_pallete

    display.fill((125, 0, 255))
    display.blit(menuBackGround, py.Rect(0, 0, 1600, 900))

    #chapter 1
    if b11.draw():
        selected_level = Level11_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete=[backGroundPink, backGroundBlue, wall_image_pink]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b12.draw():
        selected_level = Level12_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundPink, backGroundBlue, wall_image_pink]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b13.draw():
        selected_level = Level13_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundPink, backGroundBlue, wall_image_pink]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b14.draw():
        selected_level = Level14_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundPink, backGroundBlue, wall_image_pink]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b15.draw():
        selected_level = Level15_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundPink, backGroundBlue, wall_image_pink]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    #chapter 2
    if b21.draw():
        selected_level = Level21_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundBlue, backGroundGreen, wall_image_blue]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b22.draw():
        selected_level = Level22_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundBlue, backGroundGreen, wall_image_blue]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b23.draw():
        selected_level = Level23_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundBlue, backGroundGreen, wall_image_blue]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b24.draw():
        selected_level = Level24_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundBlue, backGroundGreen, wall_image_blue]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b25.draw():
        selected_level = Level25_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundBlue, backGroundGreen, wall_image_blue]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2

    #chapter 3
    if b31.draw():
        selected_level = Level31_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundGreen, backGroundPink, wall_image_green]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b32.draw():
        selected_level = Level32_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundGreen, backGroundPink, wall_image_green]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b33.draw():
        selected_level = Level33_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundGreen, backGroundPink, wall_image_green]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b34.draw():
        selected_level = Level34_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundGreen, backGroundPink, wall_image_green]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2
    if b35.draw():
        selected_level = Level35_matrix
        map_matrix = copy.deepcopy(selected_level)
        color_pallete = [backGroundGreen, backGroundPink, wall_image_green]
        py.mixer.Sound.play(button_wav)
        showed_screen = 2

    for e in py.event.get():
        if e.type == py.QUIT:
            game_run = False
            py.quit()
            exit()
        if e.type == py.KEYDOWN:
            if e.key == py.K_ESCAPE:
                showed_screen=0

    py.display.update()
    py.time.Clock().tick(60)

def play_level(selected_level, color_pallete):
    global powerUp_use
    global powerUp_ctr
    global powerG_show
    global game_run
    global map_matrix
    global showed_screen

    wall_image=color_pallete[2]
    display.fill((125, 0, 255))
    display.blit(actualBackGround, py.Rect(0, 0, 1600, 900))
    if powerUp_use==0:
        selectedBackGround=color_pallete[0]
    else:
        selectedBackGround=color_pallete[1]
    for i in range(len(map_matrix)):
        for j in range(len(map_matrix[i])):
            if map_matrix[i][j]==0:
                spaceX=j*grid_size+spacingX
                spaceY=i*grid_size+spacingY
                space = py.Rect(spaceX, spaceY, grid_size, grid_size)
                display.blit(selectedBackGround, space)
            if map_matrix[i][j]==1:
                pushableX=j*grid_size+spacingX
                pushableY=i*grid_size+spacingY
                pushable = py.Rect(pushableX, pushableY, grid_size, grid_size)
                display.blit(wall_image, pushable)
            if map_matrix[i][j]==2:
                spaceX = j * grid_size+spacingX
                spaceY = i * grid_size+spacingY
                space = py.Rect(spaceX, spaceY, grid_size, grid_size)
                display.blit(selectedBackGround, space)

                playerX=j*grid_size+spacingX
                playerY=i*grid_size+spacingY
                player = py.Rect(playerX, playerY, grid_size, grid_size)
                display.blit(player_image, player)
            if map_matrix[i][j]==3:
                spaceX = j * grid_size+spacingX
                spaceY = i * grid_size+spacingY
                space = py.Rect(spaceX, spaceY, grid_size, grid_size)
                display.blit(selectedBackGround, space)

                pushableX = j * grid_size+spacingX
                pushableY = i * grid_size+spacingY
                pushable = py.Rect(pushableX, pushableY, grid_size, grid_size)
                display.blit(box_image, pushable)
            if map_matrix[i][j]==4:
                spaceX = j * grid_size+spacingX
                spaceY = i * grid_size+spacingY
                space = py.Rect(spaceX, spaceY, grid_size, grid_size)
                display.blit(selectedBackGround, space)

                pushableX = j * grid_size+spacingX
                pushableY = i * grid_size+spacingY
                pushable = py.Rect(pushableX, pushableY, grid_size, grid_size)
                display.blit(sword_image, pushable)
            if map_matrix[i][j]==5:
                spaceX = j * grid_size+spacingX
                spaceY = i * grid_size+spacingY
                space = py.Rect(spaceX, spaceY, grid_size, grid_size)
                display.blit(selectedBackGround, space)

                finishX=j*grid_size+spacingX
                finishY=i*grid_size+spacingY
                finish = py.Rect(finishX, finishY, grid_size, grid_size)
                display.blit(finish_image, finish)
    if powerG_show%10>4:
        display.blit(powerG1_image, powerG)
    else:
        display.blit(powerG2_image, powerG)
    powerG_show+=1

    if selected_level==Level35_matrix:
        Title_image=py.transform.scale(title_image, (600, 150))
        display.blit(Title_image, py.Rect(850, 175, 600, 150))
        display.blit(thanks_image, py.Rect(75, 400, 800, 200))

    powerText = Game_font.render(str(powerUp_ctr), False, (0, 0, 0))
    display.blit(powerText, (530, 20))

    for e in py.event.get():
        if e.type == py.QUIT:
            game_run=False
            py.quit()
            exit()
        if e.type == py.KEYDOWN:
            powerUp_ctr += playerMove(player, e.key)
            if e.key == py.K_SPACE:
                py.mixer.Sound.play(powerUp_change_wav)
                powerUp_use=1-powerUp_use
                if powerUp_ctr<1:
                    powerUp_use=0
            if e.key == py.K_r:
                map_matrix=copy.deepcopy(selected_level)
                powerUp_ctr=0
            if e.key == py.K_ESCAPE:
                showed_screen=1
                powerUp_ctr=0


    if powerUp_ctr < 1:
        powerUp_use = 0     # don't remove

    py.display.update()
    py.time.Clock().tick(60)

showed_screen=0  #0-tile 1-menu 2-level
selected_level=map_matrix.copy()
color_pallete=[backGroundPink, backGroundGreen, wall_image_pink]

py.mixer.music.load("Sounds/Jelly_song.ogg")
py.mixer.music.play(-1)


while (game_run):
    if showed_screen==0:
        title_screen()
    elif showed_screen==1:
        level_select()
    elif showed_screen==2:
        play_level(selected_level, color_pallete)

py.quit()

input("Game complete")
