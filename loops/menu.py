ch = 0
runm = True
choose = None
def Start_menu():
    import keyboard as k
    from colorama import init
    
    init()
    
    var = ['Играть', 'Выйти']
    
    def up():
        global ch
        ch = 1-ch
    def sel():
        global runm, choose
        runm = False
        choose = ch
    
    k.add_hotkey('w', up)
    k.add_hotkey('s', up)
    k.add_hotkey('up', up)
    k.add_hotkey('down', up)
    k.add_hotkey('enter', sel)
    
    while runm:
        print('\033[H\nConGame\nАльфа версия')
        for j, i in enumerate(var):
            if ch == j:
                print(f' {i}<')
            else:
                print(f'{i}  ')
        if choose != None:
            return choose