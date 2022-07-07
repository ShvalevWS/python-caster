from CasterClassGNGGA  import *

tools = Tools()
cast = Caster()


def main():
    tools.send_rtk2go_req()
    if tools.get_line() == True:
            cast.castering('192.168.43.29', 2101)


if __name__ == '__main__':
    main()
