from CasterClass import *

tools = Tools()
cast = Caster()


def main():
    if tools.get_line():
        cast.castering('192.168.100.12', 2101)


if __name__ == '__main__':
    main()
