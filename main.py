from CasterClass import *

tools = Tools()
cast = Caster()

def main():
    if tools.get_line() == True:
        cast.castering('192.168.88.237', 2101)

if __name__ == '__main__':
    main()