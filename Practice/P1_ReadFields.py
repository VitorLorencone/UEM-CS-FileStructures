def main() -> None:
    PATHNAME = "Practice/Files/People.txt"
    try:
        file = open(PATHNAME, "r")

        field:str = ""
        count = 1
        while char := file.read(1):
            if char != '|':
                field += char
            else:
                print(f'Campo #{count}: {field}')
                field = ""
                count += 1
        file.close()
        print("EOF")
    
    except OSError as e:
        print(e)
        file.close()

if __name__ == '__main__':
    main()

# Considerei melhor ler char por char porque imagino que se o arquivo for muito 
# grande, não dará para ser carregado inteiro para a memória