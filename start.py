from loops.game import *
from loops.menu import *
import sys, json, traceback

levels = []
lvlpaths = ['tutorial']
for i in lvlpaths:
    with open(fr'levels\{i}.json', 'r') as f:
        levels.append(json.load(f))
loop = 0
while True:
    if Start_menu():
        sys.exit()
    try:
        Start_game(levels[loop], 'edito')
    except Exception:
        print('Поздравляю\nВы прошли игру!\n\nЧестно...\nЭто самый уродливо выглядящий код,\nчто я когда либо писал...\n\n\nඞ')
        print(traceback.format_exc())
        break
    loop +=1