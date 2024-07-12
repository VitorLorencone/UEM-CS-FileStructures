def main() -> None:
    PATHNAME:str = "Practice/Files/People2.bin"
    BYTESIZE = 2
    try: 
        file = open(PATHNAME, "ab")
    except:
        file = open(PATHNAME, "wb")
    
    try:
        while buffer := input("Escreva o Sobrenome: "):
            buffer += '|' + input("Escreva o Nome: ")
            buffer += '|' + input("Escreva o Endereço: ")
            buffer += '|' + input("Escreva a Cidade: ")
            buffer += '|' + input("Escreva o Estado: ")
            buffer += '|' + input("Escreva o CEP: ") + '|'
            
            bufferBytes:bytes = buffer.encode()
            size:bytes = len(bufferBytes).to_bytes(BYTESIZE)

            file.write(size)
            file.write(bufferBytes)

        file.close()

    except OSError as e:
        print(e)
        file.close()

if __name__ == '__main__':
    main()