import keyboard as *
import copy
def paint_str(col, text):
    return f"\033[38;2;{col[0]};{col[1]};{col[2]}m{text}\033[0m"
world = 
class Player:
    def __init__(self, start=(0, 0)):
        self.pos = start
        self.inv = []
    def up(self):
        tar = str((self.pos[0], self.pos[1]+1))
        if tar not in world or world[tar]['beh'] == 'deco':
            self.pos[1] += 1
        elif world[tar]['beh'] != 'solid':
            if world[tar]['beh'] == 'push':
                targ = copy.deepcopy(world[tar])
                world.pop(tar, None)
                world[str((self.pos[0], self.pos[1]+2))] = targ
            self.pos[1] += 1
    def down(self):
        tar = str((self.pos[0], self.pos[1]-1))
        if tar not in world or world[tar]['beh'] == 'deco':
            self.pos[1] -= 1
        elif world[tar]['beh'] != 'solid':
            if world[tar]['beh'] == 'push':
                targ = copy.deepcopy(world[tar])
                world.pop(tar, None)
                world[str((self.pos[0], self.pos[1]-2))] = targ
            self.pos[1] -= 1
    def right(self):
        tar = str((self.pos[0]+1, self.pos[1]))
        if tar not in world or world[tar]['beh'] == 'deco':
            self.pos[0] += 1
        elif world[tar]['beh'] != 'solid':
            if world[tar]['beh'] == 'push':
                targ = copy.deepcopy(world[tar])
                world.pop(tar, None)
                world[str((self.pos[0]+2, self.pos[1]))] = targ
            self.pos[0] += 1
    def left(self):
        tar = str((self.pos[0]-1, self.pos[1]))
        if tar not in world or world[tar]['beh'] == 'deco':
            self.pos[0] -= 1
        elif world[tar]['beh'] != 'solid':
            if world[tar]['beh'] == 'push':
                targ = copy.deepcopy(world[tar])
                world.pop(tar, None)
                world[str((self.pos[0]-2, self.pos[1]))] = targ
            self.pos[0] -= 1
player = player()
add_hotkey('w', player.up)
add_hotkey('s', player.down)
add_hotkey('a', player.left)
add_hotkey('d', player.right)
atlas = ['i', '.', '■', '▣']

while True:
    render = ''
    for y in range(16):
        for x in range(16):
            if player.pos == (x, y):
                render += atlas[0]
            render += ' '