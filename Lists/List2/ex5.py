import sys

def main(arg = sys.argv[1]) -> None:
    PATHFILE = 'Lists/List2/Files/'
    NAME = sys.argv[2]

    try:
        source = open(PATHFILE+NAME, 'rb')
        output = open(PATHFILE+"Out.bin", 'wb')

        if arg == '-wl':
            prevc:bytes = b''
            while c := source.read(1):
                if c == b'\r':
                    prevc = c
                    continue
                if c == b'\n' and prevc == b'\r':
                    output.write(c)
                    prevc = c
                    continue
                elif prevc == b'\r':
                    output.write(prevc)
                prevc = c
                output.write(c)

        elif arg == '-lw':
            while c := source.read(1):
                if c == b'\n':
                    output.write(b'\r')
                    output.write(c)
                    continue
                output.write(c)
    
        source.close()
        output.close()

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()