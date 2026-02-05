def generate_bef(lambda_, start_symbol, end_symbol):
    """
    Generar la relación de precedencia BEF(λ) ⊆ (Σ x Σ) x {oi}
    """
    bef = []
    
    for trace_name, events in lambda_:
        # Primer evento
        if events:
            bef.append(((start_symbol, events[0]), trace_name))
        # Eventos consecutivos
        for i in range(len(events) - 1):
            event = ((events[i], events[i + 1]), trace_name)
            if event not in bef:
                bef.append(event)
        # Ultimo evento
        if events:
            bef.append(((events[-1], end_symbol), trace_name))
    
    return bef

def generate_po(bef, start_symbol, end_symbol):
    """
    Generar la relación de orden parcial PO(λ) = BEF(λ) / Conc
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
    po = []
    for events in bef:
        (a, b), trace_name = events
        if a != start_symbol and b != end_symbol and a != end_symbol and b != start_symbol:
            key = (a, b)
            if key not in conc:
                po.append(events)
        else:
            # Agregar primer y ultimo evento de las trazas
            po.append(events)
    
    # "Desdoblar" ciclos
    po_wo_loops = []
    ori_paths = {}
    first_ori_paths = {}

    for (a, b), trace_name in po:
        if trace_name not in ori_paths:
            ori_paths[trace_name] = set()
            first_ori_paths[trace_name] = {}
        
        new_b = b
        if b in ori_paths[trace_name]:
            new_b = f"{b}'"
        po_wo_loops.append(((a, new_b), trace_name))
        ori_paths[trace_name].add(a)

        if b not in first_ori_paths[trace_name]:
            first_ori_paths[trace_name][b] = a
    
    return po_wo_loops, conc

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
    new_bef = []
    finals = []
    for (a, b), c in bef:
        if b == end_symbol:
            finals.append(f"({a}, {c})")
        else:
            new_bef.append(((a, b), c))
    
    # Agregar transicion con consumo de simbolo
    for (a, b), trace in new_bef:
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
    
    return q, sigma, delta, q0, f, new_bef, finals

def zip_afn(bef, finals, start_symbol, end_symbol):
    trace_name = []
    events = []
    trace_event = []
    for (a, b), c in bef:
        if c not in trace_name:
            if trace_name:
                events.append(trace_event)
            trace_event = []
            trace_name.append(c)
        trace_event.append(((a, b), c))
    events.append(trace_event)

    max_ = max([len(event) for event in events])

    # Encontrar prefijos y sufijos comunes
    prefixes = find_pre_su_fixes(max_, trace_name, events)
    events = [list(reversed(sublist)) for sublist in events]
    sufixes = find_pre_su_fixes(max_, trace_name, events)

    # Crear AFN compacto
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

    # Mapeo de nuevos estado
    mapping = {}
    cont = 1
    # Recorrer cada diccionario
    for dic in prefixes:
        for clave, valores in dic.items():
            # Extraer el destino (segunda letra)
            origin = clave.split(', ')[1].rstrip(')')
            # Para cada TR en la lista, asignar el mismo Xn
            for tr in valores:
                clave_resultado = f'({origin}, {tr})'
                mapping[clave_resultado] = f'({origin}, X{cont})'
            # Incrementar Xn para el siguiente nivel
            cont += 1
    cont = 1
    for dic in sufixes:
        for clave, valores in dic.items():
            # Extraer el origen (primera letra)
            origin = clave.split(', ')[0].lstrip('(')
            # Para cada traza en la lista, asignar el mismo Yn
            for tr in valores:
                clave_resultado = f'({origin}, {tr})'
                mapping[clave_resultado] = f'({origin}, Y{cont})'
            # Incrementar Yn para el siguiente nivel
            cont += 1

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
        if origin in mapping:
            origin = mapping[origin]
        if dest in mapping:
            dest = mapping[dest]
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

def find_pre_su_fixes(max_, trace_name, events):
    # Encontrar prefijos/sufijos comunes
    fixes = []
    actual_fixes = {"START": trace_name}
    for i in range(max_):
        aux = {}
        for a, b in actual_fixes.items():
            indexes = []
            for x in b:
                indexes.append(trace_name.index(x))
            # Nuevos simbolos posibles del prefix/sufix
            for x in indexes:
                (a2, b2), c2 = events[x][i]
                aux[f"({a2}, {b2})"] = []
            # Encontrar nuevas continuaciones de prefijos/sufijos
            for x in indexes:
                (a2, b2), c2 = events[x][i]
                if f"({a2}, {b2})" in aux.keys():
                    aux[f"({a2}, {b2})"].append(c2)
            aux = {k: v for k, v in aux.items() if len(v) > 1}
        if not aux:
            break
        actual_fixes = aux
        fixes.append(actual_fixes)
    return fixes