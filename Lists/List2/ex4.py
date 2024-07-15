def main() -> None:
    PATHFILE:str = 'Lists/List2/'
    NAME:str = 'ex1.py'

    try:
        source = open(PATHFILE + NAME, "r")
        output = open(PATHFILE + 'Files/' + 'outputEx4.py', 'w')

        for i in source.readlines():
            if i[0] != '#':
                output.writelines(i)

        source.close()
        output.close()

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()