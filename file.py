def read_file(file_path):
    """
    Leer archivo de texto con el formato de trazas siguientes:
        TR1: A B C B C D
        TR2: A E F G D
        TR3: A F E G D
    """
    traces = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    trace_counter = 1
    for line in lines:
        line = line.strip()
        if not line or line.startswith('NTR:'): # "NTR: 3" -dato opcional- 
            continue
        
        if ':' in line:
            parts = line.split(':')
            trace_name = parts[0].strip()
            events_str = parts[1].strip()
        else: # “TRi” puede ser omitido
            trace_name = f"TR{trace_counter}"
            events_str = line
            trace_counter += 1
        
        events = events_str.split()
        traces.append((trace_name, events))
    
    return traces