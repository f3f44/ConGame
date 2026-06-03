world = {}
run = True
transition = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sell = 0
sel = (0, 0, 0)

def Start_game(level, mode='player'):
    import keyboard as k
    import copy, time, random, json
    from colorama import init
    
    global world
    world = level
    
    init()
    
    def paint_str(col, text):
        return f"\033[38;2;{col[0]};{col[1]};{col[2]}m{text}\033[0m"
    
    def add_obj(pos, Type='solid', sprite=(2, 6), color=(255, 255, 255), activator=(0, 0, 1), reverse=False):
        global world
        world[str((pos[0], pos[1], sell))] = {
            'beh': Type, 
            'sprite': sprite, 
            'color': color,
            'reverse': reverse,
            'active': True,
            'power': str(activator)
        }
    
    def remove_obj(pos):
        global world
        world.pop(str((pos[0], pos[1], 0)), None)
    
    def save(name='tutorial'):
        with open(fr'levels\{name}.json', 'w') as f:
            json.dump(world, f, indent=4)
        print(f"\033[H\033[J Уровень сохранен как levels\\{name}.json! \n")
        time.sleep(1)
    
    class Player:
        def __init__(self, start=[0, 0, 0]):
            self.pos = start
            self.Noclip = False
        def move(self, Dir=(0, 0)):
            new_x = self.pos[0] + Dir[0]
            new_y = self.pos[1] + Dir[1]
            if not (0 <= new_x < 16 and 0 <= new_y < 16):
                return
            if self.Noclip:
                self.pos[0] = new_x
                self.pos[1] = new_y
                return
            tar_l0 = str((new_x, new_y, 0))
            if tar_l0 not in world or world[tar_l0]['beh'] not in ['solid', 'push']:
                self.pos[0] = new_x
                self.pos[1] = new_y
                return
            if world[tar_l0]['beh'] == 'solid':
                return
            if world[tar_l0]['beh'] == 'push':
                next_x = new_x + Dir[0]
                next_y = new_y + Dir[1]
                if not (0 <= next_x < 16 and 0 <= next_y < 16):
                    return
                back_l0 = str((next_x, next_y, 0))
                back_l1 = str((next_x, next_y, 1))
                if back_l0 not in world or world[back_l0]['beh'] == 'deco':
                    world[back_l0] = world.pop(tar_l0)
                    self.pos[0] = new_x
                    self.pos[1] = new_y
        def upd(self):
            global run
            pos = str(tuple(self.pos))
            if pos in world and not self.Noclip:
                if world[pos]['beh'] == 'win':
                    run = False
        def noclip(self):
            self.Noclip = not self.Noclip
    
    player = Player()
    
    def toggle_l():
        global sell
        sell = 1 - sell
    
    def select():
        global sel
        sel = (player.pos[0], player.pos[1], sell)
    
    def link():
        global world
        t = world.pop(str((player.pos[0], player.pos[1], sell)), None)
        t['power'] = str(tuple(sel))
        world[str((player.pos[0], player.pos[1], sell))] = t
    
    if mode == 'editor':
        player.Noclip = True
        
        k.add_hotkey('1', lambda: add_obj((player.pos[0], player.pos[1], sell), Type='solid', sprite=(2, 6), color=(175, 175, 175)))
        k.add_hotkey('2', lambda: add_obj((player.pos[0], player.pos[1], sell), Type='push', sprite=(3, 3), color=(200, 200, 200)))
        k.add_hotkey('3', lambda: add_obj((player.pos[0], player.pos[1], sell), Type='win', sprite=(5, 5), color=(255, 150, 0)))
        k.add_hotkey('4', lambda: add_obj((player.pos[0], player.pos[1], sell), Type='button', sprite=(6, 6), color=(0, 150, 255)))
        k.add_hotkey('5', lambda: add_obj((player.pos[0], player.pos[1], sell), Type='deco', sprite=(4, 4), color=(0, 200, 0)))
        k.add_hotkey('0', lambda: remove_obj((player.pos[0], player.pos[1], sell)))
        k.add_hotkey('o', toggle_l)
        k.add_hotkey('l', select)
        k.add_hotkey('k', link)
        k.add_hotkey('ctrl+s', lambda: save('tutorial'))
    
    k.add_hotkey('w', player.move, args=((0, -1),))
    k.add_hotkey('s', player.move, args=((0, 1),))
    k.add_hotkey('a', player.move, args=((-1, 0),))
    k.add_hotkey('d', player.move, args=((1, 0),))
    
    atlas = ['i', '.', '■', '●', '"', '!', '□']
    
    def update():
        global world
        for key, o in world.items():
            pos = json.loads(key.replace("(", "[").replace(")", "]"))
            bx, by, blayer = pos[0], pos[1], pos[2]
            if o['beh'] == 'button':
                top_layer_key = str((bx, by, 0))
                box_on_top = top_layer_key in world and world[top_layer_key]['beh'] == 'push'
                player_on_top = (player.pos[0] == bx and player.pos[1] == by)
                if box_on_top or player_on_top:
                    o['active'] = True
                else:
                    o['active'] = False
            else:
                power_key = o.get('power')
                if power_key in world:
                    if world[power_key].get('active'):
                        o['active'] = True
                    else:
                        o['active'] = False
    
    def updtrans():
        global transition
        for j, i in enumerate(transition):
            if i == 0 and random.randint(0, 4) == 0:
                transition[j] += 1
            elif i != 0:
                transition[j] += 1
    
    while run:
        if k.is_pressed('esc'):
            break
        
        render = f'\033[H'
        
        if mode != 'editor':
            player.upd()
        
        update()
        
        for y in range(16):
            for x in range(16):
                world_key = world.get(str((x, y, 0))) or world.get(str((x, y, 1))) or None
                
                if player.pos[0] == x and player.pos[1] == y:
                    render += atlas[0]
                elif world_key != None:
                    target = world_key
                    if target.get('active', True):
                        if type(target['sprite'][0]) == int:
                            render += paint_str(target['color'], atlas[target['sprite'][0]])
                        else:
                            render += paint_str(target['color'], target['sprite'][0])
                    else:
                        if type(target['sprite'][1]) == int:
                            render += paint_str(target['color'], atlas[target['sprite'][1]])
                        else:
                            render += paint_str(target['color'], target['sprite'][1])
                else:
                    render += '.'
                render += ' '
            render += '\n'
            
        if mode == 'editor':
            render += f"\n[ РЕДАКТОР ] X:{player.pos[0]} Y:{player.pos[1]} Sel_L:{sell}\n"
            render += f"\nStanding on: {world.get(str((player.pos[0], player.pos[1], sell))) or 'Nothing'}"
            render += f"\nSelected: {sel}"
            
        print(render)
        time.sleep(0.05)
        
    if mode == 'editor':
        k.unhook_all()
        print("\033[H\033[JРедактор закрыт.")
        return

    for i in range(16):
        for j in range(16):
            if str((j, i, 0)) not in world and str((j, i, 1)) not in world:
                add_obj((j, i), 'solid', (1, 1))
    pfp = copy.copy(player.pos)
    while min(transition) <= 16:
        render = f'\033[H'
        updtrans()
        for y in range(16):
            for x in range(16):
                if pfp == [x, y-transition[x], 0]:
                    render += atlas[0]
                elif str((x, y-transition[x], 0)) in world or str((x, y-transition[x], 1)) in world:
                    target = world.get(str((x, y-transition[x], 0))) or world.get(str((x, y-transition[x], 1)))
                    if target.get('active', True):
                        if type(target['sprite'][0]) == int:
                            render += paint_str(target['color'], atlas[target['sprite'][0]])
                        else:
                            render += paint_str(target['color'], target['sprite'][0])
                    else:
                        if type(target['sprite'][1]) == int:
                            render += paint_str(target['color'], atlas[target['sprite'][1]])
                        else:
                            render += paint_str(target['color'], target['sprite'][1])
                else:
                    render += ' '
                render += ' '
            render += '\n'
        print(render)
        time.sleep(0.1)
    print('\033[HУровень\nПройден!')
    k.unhook_all()
