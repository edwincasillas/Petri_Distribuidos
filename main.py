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
    print("BEF")
    print(bef)

    # Punto 2
    make_graphs.dibujar_grafo_precedencia(bef, START_SYMBOL, END_SYMBOL)

    # Punto 3
    po, conc = generate_sets.generate_po(bef, START_SYMBOL, END_SYMBOL)
    print("PO")
    print("PO: ", po)
    print("Conc: ",conc)
    make_graphs.dibujar_grafo_precedencia(po, START_SYMBOL, END_SYMBOL, "grafo de PO")

    # Punto 4
    q, sigma, delta, q0, f = generate_sets.generate_afn(bef, START_SYMBOL, END_SYMBOL)
    print("AFN")
    print("q: ", q)
    print("sigma: ", sigma)
    print("delta: ", delta)
    print("q0: ", q0)
    print("f: ", f)
    make_graphs.dibujar_afn(q, sigma, delta, q0, f)

    q, delta = generate_sets.zip_afn(q, sigma, delta, q0, f)
    print("AFN compacto")
    print("q: ", q)
    print("sigma: ", sigma)
    print("delta: ", delta)
    print("q0: ", q0)
    print("f: ", f)
    make_graphs.dibujar_afn(q, sigma, delta, q0, f, "AFN compacto")

if __name__ == "__main__":
    main()