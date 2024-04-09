import math
import pygame
file = True
try:
    settings_file = open("settings.txt", "r")
    settings = settings_file.read()
    settings_file.close()
    settings = settings.split("\n")
    WIDTH = int(settings[0].split("width=")[1])
    HEIGHT = int(settings[1].split("height=")[1])
    fullscreen = int(settings[2].split("fullscreen=")[1])
    player_pos = list(map(float, (settings[3].split("player_pos=")[1]).split("|")[1].split()))
    player_angle = list(map(float, (settings[4].split("player_angle=")[1]).split("|")[1].split()))
    for i in range(3):
        player_angle[i] = math.radians(player_angle[i])
    player_speed = float(settings[5].split("player_speed=")[1])
    player_delta_angle = math.radians(float(settings[6].split("player_delta_angle=")[1]))
    FOV = math.radians(float(settings[7].split("FOV=")[1]))
    far_plane = float(settings[8].split("far_plane=")[1])
    guros = float(settings[9].split("guros=")[1])
    guros_k0 = float(settings[10].split("guros_k0=")[1])



    HALF_FOV = FOV / 2
    Font_koeff = WIDTH / 1000

    HALF_WIDTH = WIDTH // 2
    HALF_HEIGHT = HEIGHT // 2

    DIST = 1 / math.tan(HALF_FOV)
    screen_koef = WIDTH / HEIGHT
    HALF_FOV_H_modf = math.atan(screen_koef / DIST)

    near_plane = DIST/50

    accuracy = 10**-12

    cut_planes = (
        [[0, 1, 0], -near_plane],
        [[0, -1, 0], far_plane],
        [[math.cos(HALF_FOV_H_modf), math.sin(HALF_FOV_H_modf), 0], 0],
        [[-math.cos(HALF_FOV_H_modf), math.sin(HALF_FOV_H_modf), 0], 0],
        [[0, math.sin(HALF_FOV), math.cos(HALF_FOV)], 0],
        [[0, math.sin(HALF_FOV), -math.cos(HALF_FOV)], 0],
    )
    colours = (
        #RED  GRN BLUE
        (  0,   0,   0),  #  0 #Black
        (  0,   0, 255),  #  1 #Blue
        (  0, 255,   0),  #  2 #Green
        (  0, 255, 255),  #  3 #Ligth Blue
        (255,   0,   0),  #  4 #Red
        (255,   0, 255),  #  5 #Purple
        (255, 255,   0),  #  6 #Yellow
        (255, 255, 255),  #  7 #White
        (255, 200, 100),  #  8 #Soft Orange
        (100, 100, 100),  #  9 #Gray
        ( 50, 150,  74),  # 10 #Deep Blue
        (150, 150, 150),  # 11 #Light Gray
        (128,  64,  50),  # 12 #Brown
    )
except FileNotFoundError:
    file = False


player_slowing = player_speed
max_speed = 3000
player_max_speed = 3
BBOX = (
    (-0.15, -0.15, -1),
    (-0.15, -0.15,  1),
    (-0.15,  0.15, -1),
    (-0.15,  0.15,  1),
    ( 0.15, -0.15, -1),
    ( 0.15, -0.15,  1),
    ( 0.15,  0.15, -1),
    ( 0.15,  0.15,  1),
)
BBOX2 = (
    (-0.15, -0.15, -0.15),
    (-0.15, -0.15,  0.15),
    (-0.15,  0.15, -0.15),
    (-0.15,  0.15,  0.15),
    ( 0.15, -0.15, -0.15),
    ( 0.15, -0.15,  0.15),
    ( 0.15,  0.15, -0.15),
    ( 0.15,  0.15,  0.15),
)




