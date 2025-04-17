# Controller/simulador_procesos.py

from PyQt5.QtWidgets import QMessageBox
from Algoritmos import algoritmo_round_robin
from Algoritmos import algoritmo_FIFO
from Algoritmos import algoritmo_SJF

class SimuladorProcesos:
    def __init__(self, tabla, combo_alg, combo_quantum):
        """
        Parámetros:
          tabla: QTableWidget con los datos de procesos (columna 0: Ráfaga, columna 1: Llegada)
          combo_alg: QComboBox con la selección de algoritmo
          combo_quantum: QComboBox o QSpinBox para el quantum (se usa solo en Round Robin)
        """
        self.tabla = tabla
        self.combo_alg = combo_alg
        self.combo_quantum = combo_quantum

    def simular(self, parent):
        """
        Ejecuta la simulación según los datos en la tabla y el algoritmo seleccionado.
        Retorna una tupla con:
          (intervals, tiempo_sistema, tiempo_espera, promedio_tiempo_sistema, promedio_tiempo_espera)
        O muestra un mensaje de error y retorna None.
        """
        num_filas = self.tabla.rowCount()
        processes = []
        
        for i in range(num_filas):
            # Suponiendo que la columna 0 es Ráfaga y la columna 1 es Tiempo de Llegada
            item_burst = self.tabla.item(i, 0)
            item_arrival = self.tabla.item(i, 1)
            if item_burst is None or item_arrival is None or item_burst.text().strip() == "" or item_arrival.text().strip() == "":
                QMessageBox.warning(parent, "Error", f"Falta llenar datos en la fila {i+1}.")
                return None
            try:
                burst = float(item_burst.text().strip())
                arrival = float(item_arrival.text().strip())
            except ValueError:
                QMessageBox.warning(parent, "Error", f"Los valores de la fila {i+1} deben ser numéricos.")
                return None
            
            processes.append({
                "id": f"P{i+1}",
                "burst": burst,
                "arrival": arrival
            })
        
        algoritmo = self.combo_alg.currentText().strip().upper()
        
        if algoritmo == "FIFO":
            intervalos,tiempo_sistema,tiempo_espera = algoritmo_FIFO.fifo_intervals(processes)
            promedio_tiempo_sistema= sum(tiempo_sistema.values()) / len(tiempo_sistema)
            promedio_tiempo_espera = sum(tiempo_espera.values()) / len(tiempo_espera)
            return intervalos,tiempo_sistema,tiempo_espera,promedio_tiempo_sistema,promedio_tiempo_espera
        
        elif algoritmo == "SJF":
            intervalos,tiempo_sistema,tiempo_espera = algoritmo_SJF.sjf_intervals(processes)
            promedio_tiempo_sistema = sum(tiempo_sistema.values()) / len(tiempo_sistema)
            promedio_tiempo_espera = sum(tiempo_espera.values()) / len(tiempo_espera)
            return intervalos,tiempo_sistema,tiempo_espera,promedio_tiempo_sistema,promedio_tiempo_espera

        elif algoritmo == "ROUND ROBIN":
            try:
                quantum = int(self.combo_quantum.currentText().strip())
            except ValueError:
                QMessageBox.warning(parent, "Error", "El quantum debe ser un número entero válido.")
                return None
            intervals, tiempo_sistema, tiempo_espera = algoritmo_round_robin.round_robin_variant(processes, quantum)
            promedio_tiempo_sistema = sum(tiempo_sistema.values()) / len(tiempo_sistema)
            promedio_tiempo_espera = sum(tiempo_espera.values()) / len(tiempo_espera)
            return intervals, tiempo_sistema, tiempo_espera, promedio_tiempo_sistema, promedio_tiempo_espera
        else:
            QMessageBox.warning(parent, "Error", "Algoritmo no reconocido.")
            return None
