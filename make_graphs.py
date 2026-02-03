import graphviz
import os

output_directory = "red_generada"

def directorio():
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

def dibujar_grafo_precedencia(bef, start_symbol, end_symbol, imagen="Grafo de Precedencia"):
    directorio()

    dot = graphviz.Digraph('Grafo de Precedencia',
                           comment='Grafo de Precedencia',
                           strict=True,
                           graph_attr={'rankdir': 'LR', 'splines': 'true'})
    
    transiciones = {}
    
    for (origen, destino), transicion in bef:
        dot.node(name=origen, 
                 label=origen, 
                 shape='circle', 
                 color='green' if origen == start_symbol else 'black')
        
        dot.node(name=destino, 
                 label=destino, 
                 shape='circle',
                 color='red' if destino == end_symbol else 'black')
        
        # Crear transiciones
        key = (origen, destino)
        if key not in transiciones:
            transiciones[key] = []
        transiciones[key].append(transicion)
    
    # Agregar aristas con etiquetas
    for (origen, destino), _ in transiciones.items():
        dot.edge(origen, destino)
    
    # Nodos START y END 
    dot.node(name=start_symbol, 
             shape='doublecircle', color='darkgreen', 
             style='filled', fillcolor='lightgreen')
    dot.node(name=end_symbol, 
             shape='doublecircle', color='red', 
             style='filled', fillcolor='pink')
    
    dot.render(imagen, view=True, format='png', directory=output_directory, cleanup=True)
    print(f"Grafo guardado en '{output_directory}'!")

def dibuja_afn_simple(q, sigma, delta, q0, f, imagen="AFN"):
    directorio()

    dot = graphviz.Digraph('AFN',
                           comment='Autómata Finito No Determinista',
                           strict=True,
                           graph_attr={'rankdir': 'LR', 'splines': 'true'})
    
    # Nodo invisible para la flecha del estado inicial
    dot.node(name='inicio_invisible', label='', shape='point')
    
    # Estados
    for estado in sorted(q):
        if estado == q0:
            dot.node(name=estado, label=estado, 
                    shape='circle', color='darkgreen',
                    style='filled', fillcolor='lightgreen')
        elif estado in f:
            dot.node(name=estado, label=estado, 
                    shape='doublecircle', color='red',
                    style='filled', fillcolor='pink')
        else:
            dot.node(name=estado, label=estado, 
                    shape='circle', color='black')
    
    # Conectar nodo invisible al estado inicial
    dot.edge('inicio_invisible', q0)
    
    # Agregar transiciones agrupando símbolos
    for estado_origen, transiciones in delta.items():
        for simbolo, estados_destino in transiciones.items():
            for estado_destino in estados_destino:
                dot.edge(estado_origen, estado_destino, 
                        label=simbolo,
                        color='black')
    
    dot.render(imagen, view=True, format='png', directory=output_directory, cleanup=True)
    print(f"AFN guardado en '{output_directory}'!")