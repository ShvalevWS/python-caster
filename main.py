from CasterClass import *

tools = Tools()
cast = Caster()


def main():
    if tools.get_line():
        cast.castering('127.0.0.1', 2101)


if __name__ == '__main__':
    main()
