from collections import deque
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
    
    """
    def fifo_mejorado(self, referencia, num_marcos):
        
        FIFO + segunda oportunidad (segunda vida):
          - Cada vez que un page hit, se limpia todo bit y se marca ese marco con bit=True.
          - Al fallar y no haber free frame, se elige victim siguiendo la FIFO original
            (insertion_time más antiguo), pero si victim.bit==True, lo resetea (bit=False)
            y pasa al siguiente más antiguo. Al final reemplaza el primer victim con bit=False.
        Retorna: (matriz, fallos_col, total_fallos)
        
        n = len(referencia)
        # Cada marco lleva: página, bit (segunda vida) y tiempo de inserción
        frames = [
            {'page': None, 'bit': False, 'insertion_time': float('inf')}
            for _ in range(num_marcos)
        ]

        # Preparo la matriz (num_marcos filas + 1 fila de fallos) x n columnas
        matrix     = [['' for _ in range(n)] for _ in range(num_marcos + 1)]
        fallos_col = [''] * n
        total_fallos = 0

        for i, page in enumerate(referencia):
            # Copio columna anterior (para simplificar el código de snapshot)
            if i > 0:
                for r in range(num_marcos + 1):
                    matrix[r][i] = matrix[r][i-1]

            if page in [fr['page'] for fr in frames]:
                # **HIT**: limpio todos los bits y doy segunda vida al que tocó
                idx = next(j for j,fr in enumerate(frames) if fr['page']==page)
                for fr in frames:
                    fr['bit'] = False
                frames[idx]['bit'] = True
                fallos_col[i] = ''
            else:
                # **MISS**
                total_fallos += 1
                fallos_col[i] = '*'

                # 1) ¿Hay marco libre?
                free_idx = next((j for j,fr in enumerate(frames) if fr['page'] is None), None)
                if free_idx is not None:
                    # lo meto en el hueco
                    frames[free_idx]['page'] = page
                    frames[free_idx]['bit'] = False
                    frames[free_idx]['insertion_time'] = i
                else:
                    # 2) FIFO puro ordenando por insertion_time
                    orden = sorted(range(num_marcos),
                                  key=lambda j: frames[j]['insertion_time'])
                    # 3) recorro FIFO: si bit==True reseteo bit y sigo, si bit==False evicto
                    for victim in orden:
                        if frames[victim]['bit']:
                            frames[victim]['bit'] = False
                            continue
                        # encontrado victim
                        frames[victim]['page'] = page
                        frames[victim]['bit'] = False
                        frames[victim]['insertion_time'] = i
                        break

            # **Snapshot** del estado de los marcos en la columna i
            for f in range(num_marcos):
                pg = frames[f]['page']
                if pg is None:
                    matrix[f][i] = ''
                else:
                    matrix[f][i] = f"{pg}{'*' if frames[f]['bit'] else ''}"

            # marco la fila de fallos
            matrix[num_marcos][i] = fallos_col[i]

        return matrix, fallos_col, total_fallos
    """

    def fifo_mejorado(self, referencia, num_marcos):
        """
        FIFO + segunda oportunidad (segunda vida):
        - Cada vez que un page hit, se limpia todo bit y se marca ese marco con bit=True.
        - Al fallar y no haber free frame, se elige victim siguiendo la FIFO original
            (insertion_time más antiguo), pero si victim.bit==True, lo resetea (bit=False)
            y pasa al siguiente más antiguo. Al final reemplaza el primer victim con bit=False.
        Retorna: (matriz, fallos_col, total_fallos)
        - matriz: num_marcos filas x len(referencia) columnas
        - fallos_col: lista de '*' o '' de longitud len(referencia)
        - total_fallos: entero
        """
        n = len(referencia)
        # Cada marco lleva: página, bit (segunda vida) y tiempo de inserción
        frames = [
            {'page': None, 'bit': False, 'insertion_time': float('inf')}
            for _ in range(num_marcos)
        ]

        # PREPARO la matriz únicamente para los estados de marcos:
        matrix     = [['' for _ in range(n)] for _ in range(num_marcos)]
        # FALLOS en una lista aparte:
        fallos_col = [''] * n
        total_fallos = 0

        for i, page in enumerate(referencia):
            # 1) HIT?
            pages_in_frames = [fr['page'] for fr in frames]
            if page in pages_in_frames:
                # Limpio todos los bits y doy segunda vida al marco tocado
                idx = pages_in_frames.index(page)
                for fr in frames:
                    fr['bit'] = False
                frames[idx]['bit'] = True
                fallos_col[i] = ''
            else:
                # MISS
                total_fallos += 1
                fallos_col[i] = '*'
                # ¿Marco libre?
                free_idx = next((j for j,fr in enumerate(frames) if fr['page'] is None), None)
                if free_idx is not None:
                    frames[free_idx]['page'] = page
                    frames[free_idx]['bit'] = False
                    frames[free_idx]['insertion_time'] = i
                else:
                    # FIFO puro por insertion_time
                    orden = sorted(range(num_marcos),
                                key=lambda j: frames[j]['insertion_time'])
                    # Buscamos victim sin bit; si lo tiene, lo limpiamos y seguimos
                    for victim in orden:
                        if frames[victim]['bit']:
                            frames[victim]['bit'] = False
                            continue
                        # reemplazamos aquí
                        frames[victim]['page'] = page
                        frames[victim]['bit'] = False
                        frames[victim]['insertion_time'] = i
                        break

            # 2) Snapshot del estado de los marcos en la columna i
            for f in range(num_marcos):
                pg = frames[f]['page']
                if pg is None:
                    matrix[f][i] = ''
                else:
                    matrix[f][i] = f"{pg}{'*' if frames[f]['bit'] else ''}"

            # 3) Devuelvo **sólo**:
            #    - matrix: estados de marcos (n filas x len columnas)
            #    - fallos_col: lista de '*' o ''
            #    - total_fallos: número

        return matrix, fallos_col, total_fallos




# ------------------ EJEMPLO DE USO ------------------
if __name__ == "__main__":
    referencia = [7 ,0 ,1 ,2 ,0 ,3 ,0 ,4 ,2 ,3 ,0 ,3 ,2 ,1 ,2 ,0 ]
    num_marcos = 3


    alg = Algoritmos()
    matrix,fallos,total_fallos = alg.fifo_mejorado(referencia, num_marcos)

    print("Cadena de referencia:", referencia)
    print(f"Marcos: {num_marcos}\n")

    cols = len(referencia)
    rows = num_marcos + 1  # la ultima fila es de fallos

    for r in range(rows):
        print(matrix[r])
    print("\nTotal de fallos:", total_fallos)
