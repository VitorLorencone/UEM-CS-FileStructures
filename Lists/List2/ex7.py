import sys

def main() -> None:
    PATHFILE = 'Lists/List2/Files/Out6.bin'

    try:
        file = open(PATHFILE, 'rb')
        
        while c := file.read(4):
            print(int.from_bytes(c))
    
    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()