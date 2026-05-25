import keyboard as k
import copy, time, random
from colorama import init

init()

def paint_str(col, text):
    return f"\033[38;2;{col[0]};{col[1]};{col[2]}m{text}\033[0m"
world = {}

def add_obj(pos, t='solid', s=1, c=(255, 255, 255)):
    global world
    world[str(pos)] = {
        'beh': t, 
        'sprite': s, 
        'color': c
    }

class Player:
    def __init__(self, start=[0, 0]):
        self.pos = start
        self.inv = []
    def down(self):
        tar = str((self.pos[0], self.pos[1]+1))
        if tar not in world or world[tar]['beh'] == 'deco':
            self.pos[1] += 1
        elif world[tar]['beh'] != 'solid':
            tar2 = str((self.pos[0], self.pos[1]+2))
            if world[tar]['beh'] == 'push' and (tar2 not in world or world[tar2]['beh'] == 'deco'):
                targ = copy.deepcopy(world[tar])
                world.pop(tar, None)
                world[tar2] = targ
                self.pos[1] += 1
            elif world[tar]['beh'] != 'push':
                self.pos[1] += 1
    def up(self):
        tar = str((self.pos[0], self.pos[1]-1))
        if tar not in world or world[tar]['beh'] == 'deco':
            self.pos[1] -= 1
        elif world[tar]['beh'] != 'solid':
            tar2 = str((self.pos[0], self.pos[1]-2))
            if world[tar]['beh'] == 'push' and (tar2 not in world or world[tar2]['beh'] == 'deco'):
                targ = copy.deepcopy(world[tar])
                world.pop(tar, None)
                world[tar2] = targ
                self.pos[1] -= 1
            elif world[tar]['beh'] != 'push':
                self.pos[1] -= 1
    def right(self):
        tar = str((self.pos[0]+1, self.pos[1]))
        if tar not in world or world[tar]['beh'] == 'deco':
            self.pos[0] += 1
        elif world[tar]['beh'] != 'solid':
            tar2 = str((self.pos[0]+2, self.pos[1]))
            if world[tar]['beh'] == 'push' and (tar2 not in world or world[tar2]['beh'] == 'deco'):
                targ = copy.deepcopy(world[tar])
                world.pop(tar, None)
                world[tar2] = targ
                self.pos[0] += 1
            elif world[tar]['beh'] != 'push':
                self.pos[0] += 1
    def left(self):
        tar = str((self.pos[0]-1, self.pos[1]))
        if tar not in world or world[tar]['beh'] == 'deco':
            self.pos[0] -= 1
        elif world[tar]['beh'] != 'solid':
            tar2 = str((self.pos[0]-2, self.pos[1]))
            if world[tar]['beh'] == 'push' and (tar2 not in world or world[tar2]['beh'] == 'deco'):
                targ = copy.deepcopy(world[tar])
                world.pop(tar, None)
                world[tar2] = targ
                self.pos[0] -= 1
            elif world[tar]['beh'] != 'push':
                self.pos[0] -= 1
    def upd(self):
        global run
        pos = str(tuple(self.pos))
        if pos in world:
            if world[pos]['beh'] == 'win':
                run = False
player = Player()
k.add_hotkey('w', player.up)
k.add_hotkey('s', player.down)
k.add_hotkey('a', player.left)
k.add_hotkey('d', player.right)
atlas = ['i', '.', '■', '▣', '"', '!']

transition = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
worldt = copy.deepcopy(world)
def updtrans():
    global transition, worldt
    for j, i in enumerate(transition):
        if i == 0 and random.randint(0, 4) == 0:
            transition[j] += 1
        elif i != 0:
            transition[j] += 1

run = True
while run:
    render = f'\033[H'
    player.upd()
    for y in range(16):
        for x in range(16):
            if player.pos == [x, y]:
                render += atlas[0]
            elif str((x, y)) in world:
                target = world[str((x, y))]
                if type(target['sprite']) == int:
                    render += paint_str(target['color'], atlas[target['sprite']])
                else:
                    render += paint_str(target['color'], target['sprite'])
            else:
                render += '.'
            render += ' '
        render += '\n'
    print(render)
    time.sleep(0.01)
for i in range(16):
    for j in range(16):
        if str((j, i)) not in world:
            add_obj((j, i), 'solid', 1)
pfp = copy.copy(player.pos)
while min(transition) <= 16:
    render = f'\033[H'
    updtrans()
    for y in range(16):
        for x in range(16):
            if pfp == [x, y-transition[x]]:
                render += atlas[0]
            elif str((x, y-transition[x])) in world:
                target = world[str((x, y-transition[x]))]
                if type(target['sprite']) == int:
                    render += paint_str(target['color'], atlas[target['sprite']])
                else:
                    render += paint_str(target['color'], target['sprite'])
            else:
                render += ' '
            render += ' '
        render += '\n'
    print(render)
    time.sleep(0.1)
print('\033[HCongradulations,\nYou\nWon!')