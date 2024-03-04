from src.constans.gameconst import *
from src.database.ContolBD import ControlDataBase
from src.game.entity import Mine, Block, Wall, Core, Turel, Wall_Ust
from src.game.bot import Bot

def open_file_map(name, x, y):
    var = name[1:3]
    if name[0] == 'f':  # фон
        return Block(var + 'fon', x, y, x, y, 'f', var)
    elif name[0] == 'r':  # руда
        return Block(var + 'rud', x, y, x, y, 'r', var, rud_group)
    elif name[0] == 's':  # стена
        return Wall(var, x, y, x, y, int(name[3:]))
    elif name[0] == 'y':  # ядро
        return Core(x, y, x, y, int(name[3:]), var)
    elif name[0] == 'm':  # бур
        return Mine(x, y, x, y, int(name[3:]), var)
    elif name[0] == 't':  # турель
        return Turel(x, y, x, y, int(name[3:]), var)
    elif name[0] == 'w':  # стена само построенная(персом)
        return Wall_Ust(x, y, x, y, int(name[3:]), var)


# Раскодирование файла с ботами
def open_file_bots(name, x0, y0):
    bot = Bot(float(name[name.index('#') + 1:name.index(':')]), float(name[name.index(':') + 1:]),
              x0, y0, int(name[:name.index('#')]))
    bot.z_rect(x0, y0)


# Загрузка уровня

def load_level(filename, x, y):
    ControlDataBase().del_world(filename)
    filename0 = "map/" + filename + 'map.txt'
    with open(filename0, 'r') as mapFile:
        level_map = [line.split() for line in mapFile]

    board0 = [[open_file_map(level_map[i][j], j, i) for j in range(len(level_map[i]))] for i in range(len(level_map))]
    os.remove(filename0)
    filename1 = "map/" + filename + 'play.txt'
    with open(filename1, 'r') as mapFile:
        level_map = [line for line in mapFile]

    [open_file_bots(level_map[i], x, y) for i in range(len(level_map))]
    os.remove(filename1)
    return board0