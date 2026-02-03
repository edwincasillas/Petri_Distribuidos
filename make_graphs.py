import graphviz
import os

output_directory = "red_generada"

def directorio():
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

def dibujar_grafo_precedencia(bef, start_symbol, end_symbol, imagen="Grafo de Precedencia"):
    """
    Docstring for dibuja_RP
    
    :param seq: Dicionario de listas
    :param imagen: Nombre de la imagen de sailida
    """
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
    dot.node(start_symbol, shape='doublecircle', color='darkgreen', 
            style='filled', fillcolor='lightgreen')
    dot.node(end_symbol, shape='doublecircle', color='darkgreen', 
            style='filled', fillcolor='lightgreen')
    
    dot.render(imagen, view=True, format='png', directory=output_directory, cleanup=True)
    print(f"Grafo guardado en '{output_directory}'!")
