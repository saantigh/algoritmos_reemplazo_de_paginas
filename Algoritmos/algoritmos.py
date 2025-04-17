class Algoritmos:

    def fifo(self, referencia, marcos):
        """
        referencia: lista con las páginas solicitadas (ej: [1,2,3,4,1,...])
        marcos: número de marcos disponibles
        """
        # Inicializamos la estructura de marcos (cada fila es un marco fijo)
        frames = [-1] * marcos  # -1 indica marco vacío

        # Matriz: 'marcos' filas, len(referencia) columnas
        # Cada columna representará el estado de frames luego de cada referencia
        matriz = [[None] * len(referencia) for _ in range(marcos)]

        # Para registrar los fallos de página ('*' o '')
        fallos_col = [''] * len(referencia)  
        contador_fallos = 0

        # 'pointer' para saber qué marco reemplazar (ciclo FIFO)
        pointer = 0  

        for i, pagina in enumerate(referencia):
            # Si la página ya está en frames, no hay fallo
            if pagina in frames:
                # No aumenta contador de fallos
                fallos_col[i] = ''
            else:
                # Fallo de página
                contador_fallos += 1
                fallos_col[i] = '*'
                # Reemplazamos la página que entró primero (FIFO)
                frames[pointer] = pagina  
                # Avanzamos el pointer de forma circular
                pointer = (pointer + 1) % marcos

            # Guardamos el estado actual de los marcos en la columna i
            for fila in range(marcos):
                matriz[fila][i] = frames[fila] if frames[fila] != -1 else ''

        return matriz, fallos_col, contador_fallos
    

    def lru(self, referencia, marcos):
        """
        referencia: lista con las páginas solicitadas, ej: [1,2,3,4,1,2,5...]
        marcos: número de marcos disponibles

        Retorna:
          - matriz: estado de cada marco luego de cada referencia
          - fallos_col: lista con '' o '*' según ocurra o no un fallo
          - total_fallos: número total de fallos de página
        """

        # frames[i] = página cargada en el marco i (inicialmente -1 o vacía)
        frames = [-1] * marcos
        
        # Para registrar el uso reciente: usage[i] = índice de la última referencia
        usage = [-1] * marcos

        # Matriz con marcos filas x len(referencia) columnas
        matriz = [[None]*len(referencia) for _ in range(marcos)]
        fallos_col = [''] * len(referencia)  # '*' si hay fallo, '' si no
        total_fallos = 0

        for t, pagina in enumerate(referencia):
            if pagina in frames:
                # No hay fallo de página
                fallos_col[t] = ''
                # Actualizamos la última referencia de la página
                idx = frames.index(pagina)
                usage[idx] = t
            else:
                # Hay fallo de página
                total_fallos += 1
                fallos_col[t] = '*'

                if -1 in frames:
                    # Aún hay marcos libres
                    free_index = frames.index(-1)
                    frames[free_index] = pagina
                    usage[free_index] = t
                else:
                    # Reemplazamos la página menos recientemente usada
                    # => la que tenga la última referencia más pequeña
                    lru_index = usage.index(min(usage))
                    frames[lru_index] = pagina
                    usage[lru_index] = t

            # Actualizar la matriz para esta columna
            for fila in range(marcos):
                # Si el marco está vacío (=-1), ponemos ''
                matriz[fila][t] = '' if frames[fila] == -1 else frames[fila]

        return matriz, fallos_col, total_fallos
    
    def optimo(self, referencia, marcos):
        """
        referencia: lista con las páginas solicitadas (ej: [6,1,7,1,2,5,...])
        marcos: número de marcos disponibles

        Retorna:
         - matriz: estado de los marcos luego de cada referencia (marcos filas x len(referencia) columnas)
         - fallos_col: lista con '*' o '' si hay fallo o no
         - total_fallos: número total de fallos de página
        """

        # frames[f] = página en el marco f (inicialmente -1 o vacío)
        frames = [-1] * marcos

        # Para llevar control de cuándo se insertó cada página en cada marco (por FIFO en caso de que varias no aparezcan).
        insertion_time = [-1] * marcos

        # Matriz (marcos filas x len(referencia) columnas)
        matriz = [[None]*len(referencia) for _ in range(marcos)]
        fallos_col = [''] * len(referencia)
        total_fallos = 0

        def next_occurrence(page, start_index):
            """
            Retorna el índice de la próxima vez que 'page' aparece en 'referencia'
            a partir de 'start_index'. Si no aparece más, retorna None.
            """
            for idx in range(start_index, len(referencia)):
                if referencia[idx] == page:
                    return idx
            return None  # No aparece de nuevo

        for i, pagina in enumerate(referencia):
            if pagina in frames:
                # No hay fallo de página
                fallos_col[i] = ''
            else:
                # Ocurre fallo
                total_fallos += 1
                fallos_col[i] = '*'

                # Ver si hay espacio libre
                if -1 in frames:
                    # Asignar a primer marco libre
                    free_index = frames.index(-1)
                    frames[free_index] = pagina
                    insertion_time[free_index] = i  # Registramos que se insertó en el tiempo i
                else:
                    # Reemplazo Óptimo:
                    # 1. Verificar si hay páginas que no aparezcan de nuevo
                    # 2. Si varias no aparecen, reemplazar la que se insertó primero (FIFO).
                    # 3. Si todas aparecen, reemplazar la más lejana.
                    max_distance = -1
                    replace_index = None

                    # Guardamos temporalmente las que no aparecen más adelante
                    pages_not_used = []

                    for f in range(marcos):
                        dist = next_occurrence(frames[f], i+1)
                        if dist is None:
                            # No se usará más adelante
                            pages_not_used.append(f)
                        else:
                            # Se usará en el futuro
                            if dist > max_distance:
                                max_distance = dist
                                replace_index = f

                    if pages_not_used:
                        # Si hay varias páginas no usadas, usamos la que entró primero
                        if len(pages_not_used) == 1:
                            # Solo una no aparece más
                            replace_index = pages_not_used[0]
                        else:
                            # Múltiples no aparecerán => FIFO entre ellas
                            # Escogemos la de insertion_time más antiguo
                            oldest_time = float('inf')
                            for f in pages_not_used:
                                if insertion_time[f] < oldest_time:
                                    oldest_time = insertion_time[f]
                                    replace_index = f

                    # Reemplazamos en frames[replace_index]
                    frames[replace_index] = pagina
                    insertion_time[replace_index] = i  # Actualizamos inserción

            # Actualizar la matriz para esta columna
            for fila in range(marcos):
                matriz[fila][i] = '' if frames[fila] == -1 else frames[fila]

        return matriz, fallos_col, total_fallos
    

    #def fifo_mejorado(self, referencia, num_marcos):
        """
        Simula el algoritmo FIFO mejorado (segunda oportunidad) para reemplazo de páginas
        usando una cadena de referencias y un número fijo de marcos.
        
        Parámetros:
           referencia: lista de páginas (ej.: [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0])
           num_marcos: número de marcos de memoria.
        
        Retorna:
           - matriz: lista de listas (una por cada marco), donde cada columna muestra el estado 
                     del marco tras cada referencia. Si el marco tiene el bit de oportunidad activo, 
                     se indica con un asterisco adyacente (por ejemplo, "7*").
           - fallos: lista de strings, '*' si se produjo un fallo de página, '' si no.
           - total_fallos: total de fallos de página.
        """
        """
        # Inicializamos los marcos y sus bits (None = vacío)
        frames = [None] * num_marcos
        bits = [False] * num_marcos  # False significa sin oportunidad, True significa con oportunidad
        
        # Puntero FIFO que indica el marco candidato para reemplazo
        pointer = 0  

        n = len(referencia)
        # Matriz para registrar el estado de los marcos en cada referencia (filas fijas)
        matriz = [[None for _ in range(n)] for _ in range(num_marcos)]
        fallos = [''] * n
        total_fallos = 0

        for i, pagina in enumerate(referencia):
            if pagina in frames:
                # Caso hit: la página ya se encuentra en memoria.
                fallos[i] = ''
                idx = frames.index(pagina)
                # Se asigna el bit de oportunidad al marco correspondiente.
                bits[idx] = True
            else:
                # Fallo de página
                total_fallos += 1
                fallos[i] = '*'
                if None in frames:
                    # Hay un marco libre
                    free_idx = frames.index(None)
                    frames[free_idx] = pagina
                    bits[free_idx] = False
                else:
                    # No hay marco libre: se utiliza FIFO mejorado
                    # Se recorre la lista a partir del puntero:
                    while bits[pointer]:
                        # Si el marco tiene bit de oportunidad, se lo quita y se avanza
                        bits[pointer] = False
                        pointer = (pointer + 1) % num_marcos
                    # Ahora, en frames[pointer] el bit está en False, se reemplaza esa página
                    frames[pointer] = pagina
                    # La nueva página entra sin bit de oportunidad (ya que no ha sido referenciada previamente)
                    bits[pointer] = False
                    pointer = (pointer + 1) % num_marcos

            # Actualizar la matriz para la columna actual
            for f in range(num_marcos):
                if frames[f] is None:
                    matriz[f][i] = ''
                else:
                    # Se muestra el valor, agregando '*' si el bit está activo
                    if bits[f]:
                        matriz[f][i] = f"{frames[f]}*"
                    else:
                        matriz[f][i] = str(frames[f])
        
        return matriz, fallos, total_fallos"""

    def fifo_mejorado(self, referencia, num_marcos):
        """
        Simula el algoritmo FIFO mejorado (segunda oportunidad) para reemplazo de páginas.
        
        Parámetros:
           referencia: lista de páginas referenciadas, e.g. [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0]
           num_marcos: número de marcos disponibles.
        
        Retorna:
           - matrix: matriz de (num_marcos+1) filas x len(referencia) columnas, donde las primeras
                     num_marcos filas corresponden al estado de cada marco y la última fila indica,
                     con '*' o '', si hubo fallo en esa referencia.
           - total_fallos: número total de fallos de página.
        """
        n = len(referencia)
        
        # Inicializamos los marcos: cada marco es un diccionario con 'page' y 'bit'.
        # None indica que el marco está vacío.
        frames = [{'page': None, 'bit': False} for _ in range(num_marcos)]
        
        # Puntero FIFO para recorrer los marcos.
        pointer = 0
        
        # Crear la matriz de salida: (num_marcos + 1) filas, n columnas.
        # Las filas 0..num_marcos-1 son los marcos fijos; la fila num_marcos (última) es para marcar fallos.
        matrix = [['' for _ in range(n)] for _ in range(num_marcos + 1)]
        
        # Lista para registrar fallo de página por columna ( '*' en caso de fallo, '' en caso contrario).
        fallos = [''] * n
        total_fallos = 0

        def copiar_columna_anterior(col):
            if col == 0:
                return
            for fila in range(num_marcos + 1):
                matrix[fila][col] = matrix[fila][col - 1]

        def volcar_estado_en_columna(col):
            """Volca el estado actual de los frames en la columna 'col' de la matriz."""
            for f in range(num_marcos):
                if frames[f]['page'] is None:
                    matrix[f][col] = ''
                else:
                    # Si el bit está activo, se muestra con asterisco; si no, sin asterisco.
                    matrix[f][col] = f"{frames[f]['page']}{'*' if frames[f]['bit'] else ''}"
            # La fila de fallos ya se llenó cuando se produjo el fallo.

        # Procesar cada referencia, de la columna 0 a n-1.
        for i, page in enumerate(referencia):
            copiar_columna_anterior(i)
            # Inicialmente, no se marca fallo en esta columna.
            matrix[num_marcos][i] = ''

            pages_in_frames = [fr['page'] for fr in frames]
            if page in pages_in_frames:
                # Caso HIT: la página ya está en memoria.
                # Según tu requerimiento, si la página ya está, se debe asignar (o reasignar) el bit a ese marco.
                idx = pages_in_frames.index(page)
                # Según el comportamiento deseado, removemos cualquier bit en otros marcos y asignamos solo al marco referenciado.
                for fr in frames:
                    fr['bit'] = False
                frames[idx]['bit'] = True
                fallos[i] = ''
            else:
                # Caso FALLA de página.
                total_fallos += 1
                fallos[i] = '*'
                # Si hay algún marco vacío, lo usamos
                free_found = False
                for f in range(num_marcos):
                    if frames[f]['page'] is None:
                        frames[f]['page'] = page
                        frames[f]['bit'] = False
                        free_found = True
                        break
                if not free_found:
                    # No hay marco libre: usar FIFO mejorado (segunda oportunidad).
                    # Recorremos los marcos a partir de 'pointer' hasta encontrar uno sin bit.
                    replaced = False
                    while not replaced:
                        # Si el marco apuntado tiene bit True, lo limpiamos y avanzamos.
                        if frames[pointer]['bit']:
                            frames[pointer]['bit'] = False
                            pointer = (pointer + 1) % num_marcos
                        else:
                            # Este marco no tiene bit, se reemplaza.
                            frames[pointer]['page'] = page
                            frames[pointer]['bit'] = False
                            pointer = (pointer + 1) % num_marcos
                            replaced = True
            # Finalmente, actualizamos la columna i con el estado final de frames.
            volcar_estado_en_columna(i)
        
        # Colocar la fila de fallos en la matriz:
        matrix[num_marcos] = fallos[:]
        
        return matrix, total_fallos


# ------------------ EJEMPLO DE USO ------------------
if __name__ == "__main__":
    referencia = [7 ,0 ,1 ,2 ,0 ,3 ,0 ,4 ,2 ,3 ,0 ,3 ,2 ,1 ,2 ,0 ]
    num_marcos = 3


    alg = Algoritmos()
    matrix, total_fallos = alg.fifo_mejorado(referencia, num_marcos)

    print("Cadena de referencia:", referencia)
    print(f"Marcos: {num_marcos}\n")

    cols = len(referencia)
    rows = num_marcos + 1  # la ultima fila es de fallos

    for r in range(rows):
        print(matrix[r])
    print("\nTotal de fallos:", total_fallos)
