import sys

def main() -> None:
    PATHFILE = 'Lists/List2/Files/Out6.bin'

    try:
        out = open(PATHFILE, 'wb')
        
        c = sys.stdin.read(1)
        count = 0
        while count != 10:
            out.write(int(c).to_bytes(4))
            count += 1
            c = sys.stdin.read(1)
    
    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()