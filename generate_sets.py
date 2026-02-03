def generate_bef(lambda_, start_symbol, end_symbol):
    """
    Generar la relación de precedencia BEF(λ) ⊆ (Σ x Σ) x {oi}
    """
    bef = set()
    
    for trace_name, events in lambda_:
        # Primer evento
        if events:
            bef.add(((start_symbol, events[0]), trace_name))
        # Eventos consecutivos
        for i in range(len(events) - 1):
            bef.add(((events[i], events[i + 1]), trace_name))
        # Ultimo evento
        if events:
            bef.add(((events[-1], end_symbol), trace_name))
    
    return bef

def generate_po(bef, start_symbol, end_symbol):
    """
    Generar la relación de orden parcial PO(λ) = BEF(λ) \ Conc
        donde:
            Conc = {((a, b), oi), ((b, a), oj) ∈ BEF(λ) | oi ≠ oj }
    """
    conc = set()
    new_bef = {}
    for (a, b), trace_name in bef:
        # Ignorar primer y ultimo evento
        if a != start_symbol and b != end_symbol and a != end_symbol and b != start_symbol:
            key = (a, b)
            if key not in new_bef:
                new_bef[key] = set()
            new_bef[key].add(trace_name)
    
    # Encontrar Conc
    for (a, b), traces in new_bef.items():
        reverse_key = (b, a)
        if reverse_key in new_bef:
            traces_r = new_bef[reverse_key]
            if traces != traces_r:
                conc.add((a, b))
                conc.add((b, a))
    
    # Hacer PO(λ) = BEF(λ) \ Conc
    po = set()
    for events in bef:
        (a, b), trace_name = events
        if a != start_symbol and b != end_symbol and a != end_symbol and b != start_symbol:
            key = (a, b)
            if key not in conc:
                po.add(events)
        else:
            # Agregar primer y ultimo evento de las trazas
            po.add(events)
    
    return po, conc

def generate_afn(bef, start_symbol, end_symbol):
    q = set()
    sigma = set()
    delta = {}
    q0 = start_symbol
    f = set()

    q.add(q0)
    delta[q0] = {}
    
    f.add(end_symbol)
    q.add(end_symbol)
    delta[end_symbol] = {}

    # Eliminar transicion epsilon inutil
    new_bef = set()
    finals = []
    for ((a, b), c) in bef:
        if b == end_symbol:
            finals.append(f"({a}, {c})")
        else:
            new_bef.add(((a, b), c))
    bef = new_bef
    print(finals)
    
    # Agregar transicion con consumo de simbolo
    for (a, b), trace in bef:
        symbol = b
        sigma.add(symbol)
        
        # Determinar estado inicial
        if a == start_symbol:
            origin = a
        else:
            origin = f"({a}, {trace})"
        
        # Determinar estado destino
        dest = f"({b}, {trace})"
        if dest in finals:
            dest = end_symbol
        
        # Agregar estados a Q
        q.add(origin)
        q.add(dest)
        
        # Inicializar transiciones para origen
        if origin not in delta:
            delta[origin] = {}
        # Inicializar transiciones para destino
        if dest not in delta:
            delta[dest] = {}
        
        # Agregar transición no determinista
        if symbol not in delta[origin]:
            delta[origin][symbol] = set()
        delta[origin][symbol].add(dest)
    
    return q, sigma, delta, q0, f