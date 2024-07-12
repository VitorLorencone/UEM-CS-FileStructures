def main() -> None:
    PATHNAME:str = "Practice/Files/People2.bin"
    BYTESIZE:int = 2
    
    try:
        file = open(PATHNAME, "rb")

        def ReadFields(size = 1) -> list[str]:
            buffer:bytes = file.read(size)
            fields:list[str] = buffer.decode().split('|')
            fields.pop()
            return fields

        count:int = 1
        while regSize := int.from_bytes(file.read(2)):
            fields = ReadFields(regSize)
            print(f"Registro #{count} (Tam = {regSize}):")
            for i in range(len(fields)):
                print(f"   Campo #{i+1}: {fields[i]}")
            print("")
            count += 1

        file.close()
    
    except OSError as e:
        print(e)
        file.close()

if __name__ == '__main__':
    main()