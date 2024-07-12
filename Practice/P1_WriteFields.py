def main() -> None:
    PATHFILE = "Practice/Files/People.txt"
    try:
        file = open(PATHFILE, "a")
    except:
        file = open(PATHFILE, "w")

    try:
        while surname := input("Digite o Sobrenome: "):
            name:str = input("Digite o Nome: ")
            address:str = input("Digite o Endereço: ")
            city:str = input("Digite a Cidade: ")
            state:str = input("Digite o Estado: ")
            cep:str = input("Digite o CEP: ")

            file.write(surname + '|')
            file.write(name + '|')
            file.write(address + '|')
            file.write(city + '|')
            file.write(state + '|')
            file.write(cep + '|')
        file.close()
        
    except OSError as e:
        print(e)
        file.close()

if __name__ == '__main__':
    main()