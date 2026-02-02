import file
import generate_sets

START_SYMBOL = "START"
END_SYMBOL = "END"

def main():
    input_file = "archivo_ejemplo.txt"

    lambda_ = file.read_file(input_file)
    print(lambda_)

    bef = generate_sets.generate_bef(lambda_, START_SYMBOL, END_SYMBOL)
    print(bef)

    po, conc = generate_sets.generate_po(bef, START_SYMBOL, END_SYMBOL)
    print(po)
    print(conc)

if __name__ == "__main__":
    main()