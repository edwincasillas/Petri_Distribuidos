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