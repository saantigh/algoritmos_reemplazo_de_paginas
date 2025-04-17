def parse_pid(pid):
    # Asume que tus pids tienen el formato "P" seguido de un número, p.ej. "P1", "P10", etc.
    # Con lstrip("P") quitas la 'P' al inicio y luego conviertes el resto a int.
    return int(pid.lstrip("P"))

def dibujar_gantt(intervals, titulo="Diagrama de Gantt"):
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.canvas.manager.set_window_title("Diagrama de Gantt")

    # Encontrar el máximo tiempo
    max_time = 0
    for pid, intv in intervals.items():
        for (start, end) in intv:
            if end > max_time:
                max_time = end
    
    # Ordenar pids según su parte numérica (P1 < P2 < ... < P10)
    pids = sorted(intervals.keys(), key=parse_pid)

    color_list = [
        "#f94144","#f3722c","#f8961e","#f9c74f","#90be6d",
        "#43aa8b","#577590","#277da1","#4d908e","#b5179e",
        "#7209b7","#560bad","#480ca8","#3a0ca3","#3f37c9"
    ]

    for i, pid in enumerate(pids):
        intervals_pid = intervals[pid]
        color = color_list[i % len(color_list)]
        for (start, end) in intervals_pid:
            ax.barh(
                y=i,
                width=(end - start),
                left=start,
                height=0.4,
                color=color,
                edgecolor="black"
            )

    ax.set_yticks(range(len(pids)))
    ax.set_yticklabels(pids)

    # Por defecto, y=0 abajo y y aumenta hacia arriba, así P1 queda abajo y P10 arriba
    # ax.invert_yaxis()  # Descomenta si deseas invertir

    # Ajustar eje X para ver mejor los ticks
    ax.set_xlim(0, max_time + 1)
    ax.set_xticks(np.arange(0, max_time + 1, 1))

    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Procesos")
    ax.set_title(titulo)

    plt.tight_layout()
    plt.show()

