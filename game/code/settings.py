import pyautogui

WIDTH, HEIGHT = pyautogui.size()
FPS      = 60
TILESIZE = 64

PLAYER_IMG = 'game/graphics/Factions/Knights/Troops/Warrior/Blue/Warrior_Blue.png'
WORLD_TMX = 'game/data/World.tmx'

#? UI
PLAYER_BOX_SIZE = HEIGHT*0.06

EXP_BAR_HEIGHT = HEIGHT*0.01;
EXP_BAR_WIDTH = WIDTH*0.2

BAR_HEIGHT = HEIGHT*0.02

HEALTH_BAR_WIDTH = WIDTH*0.15
ENERGY_BAR_WIDTH = WIDTH*0.075

ITEM_BOX_SIZE = HEIGHT*0.08

PADDING_Y = HEIGHT*0.005
PADDING_X = WIDTH*0.005

UI_FONT = "game/graphics/Font/LycheeSoda.ttf"
UI_FONT_SIZE = 32

#? General Color
TEXT_COLOR = "#EEEEEE"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"

#? UI Colors
EXP_COLOR = "green"
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"


#! Enemies
monster_data = {
    "goblin_barrel" : {"health": 100, "exp": 100, "damage": 20, "attack_type": "barrel", "speed": 3, "resistance": 3, "attack_radius": 80, "notice_radius": 360} 
} 

LAYERS = {
    "sea" : 0,
    "foam" : 1,
    "sand" : 2,
# ground layer 0
    "grass_0" : 3,
    "shadows_0" : 4,
    "rock_0" : 4,
# ground layer 1
    "grass_1" : 5,
    "shadows_1" : 6,
    "rock_1" : 7,
# ground layer 2
    "grass_2" : 8,
# decos
    "bridge" : 9,
    "main" : 10
}