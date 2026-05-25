ch = 0
runm = True
def Start_menu():
    import keyboard as k
    from colorama import init
    
    init()
    
    var = ['Играть', 'Выйти']
    
    def up():
        global ch
        ch = 1-ch
    def sel():
        global runm
        runm = False
        if ch == 1:
            return True
        else:
            return False
    
    k.add_hotkey('w', up)
    k.add_hotkey('s', up)
    k.add_hotkey('up', up)
    k.add_hotkey('down', up)
    k.add_hotkey('enter', sel)
    
    while runm:
        print('\033[H')
        for j, i in enumerate(var):
            if ch == j:
                print(f' {i}<')
            else:
                print(f'{i}  ')