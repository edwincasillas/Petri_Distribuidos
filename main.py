import file
import generate_sets
import make_graphs

START_SYMBOL = "START"
END_SYMBOL = "END"

def main():
    input_file = "archivo_ejemplo.txt"

    lambda_ = file.read_file(input_file)
    print(lambda_)

    # Punto 1
    bef = generate_sets.generate_bef(lambda_, START_SYMBOL, END_SYMBOL)
    print(bef)

    # Punto 2
    make_graphs.dibujar_grafo_precedencia(bef, START_SYMBOL, END_SYMBOL)

    # Punto 3
    po, conc = generate_sets.generate_po(bef, START_SYMBOL, END_SYMBOL)
    print(po)
    print(conc)
    make_graphs.dibujar_grafo_precedencia(po, START_SYMBOL, END_SYMBOL, "grafo de PO")

    # Punto 4
    q, sigma, delta, q0, f = generate_sets.generate_afn(bef, START_SYMBOL, END_SYMBOL)
    print(q)
    print(sigma)
    print(delta)
    print(q0)
    print(f)
    #make_graphs.dibujar_grafo_precedencia(po, START_SYMBOL, END_SYMBOL, "grafo de PO")

if __name__ == "__main__":
    main()