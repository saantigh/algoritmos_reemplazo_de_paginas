# Controller/controller_ventana_resultados.py

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from DesignWindows.ventana_resultados import Ui_MainWindow as Ui_VentanaResultados

class ControllerVentanaResultados(QMainWindow):
    def __init__(self, algoritmo, intervals, tiempo_espera, tiempo_sistema,
                 promedio_espera, promedio_sistema):
        """
        Recibe todos los datos calculados:
          - algoritmo: str (ej: "ROUND ROBIN", "FIFO", etc.)
          - intervals: dict {pid: [(inicio, fin), ...]}
          - tiempo_espera: dict {pid: valor}
          - tiempo_sistema: dict {pid: valor}
          - promedio_espera: float
          - promedio_sistema: float
        """
        super().__init__()
        self.ui = Ui_VentanaResultados()
        self.ui.setupUi(self)

        self.algoritmo = algoritmo
        self.intervals = intervals
        self.tiempo_espera = tiempo_espera
        self.tiempo_sistema = tiempo_sistema
        self.promedio_espera = promedio_espera
        self.promedio_sistema = promedio_sistema

        self.setupLabels()
        self.setupTables()
        self.connectSignals()

    def setupLabels(self):
        """
        Configura el label para mostrar el algoritmo escogido, por ejemplo.
        """
        # Ajustar el texto del label_algoritmo_escogido
        self.ui.label_algoritmo_escogido.setText(f"\"{self.algoritmo}\"")

    def setupTables(self):
        """
        Llena las dos tablas (tiempos de espera y tiempos de sistema)
        con los datos recibidos, incluyendo la fila adicional para el promedio.
        """
        # 1) Tiempos de Espera
        #   - La cantidad de filas será len(tiempo_espera) + 1 para el promedio
        n = len(self.tiempo_espera)
        self.ui.tabla_tiempos_espera.setRowCount(n + 1)
        # Establecer encabezados verticales (P1, P2, ..., y "PROMEDIO")
        # Podrías usar setVerticalHeaderLabels o setItem en la columna de encabezado.
        # Ejemplo: setVerticalHeaderItem
        row_labels = list(self.tiempo_espera.keys()) + ["PROM"]
        self.ui.tabla_tiempos_espera.setVerticalHeaderLabels(row_labels)

        # Llenar celdas
        row = 0
        for pid, valor in self.tiempo_espera.items():
            item = QTableWidgetItem(str(valor))
            self.ui.tabla_tiempos_espera.setItem(row, 0, item)
            row += 1

        # Última fila: promedio
        item_promedio_espera = QTableWidgetItem(str(self.promedio_espera))
        self.ui.tabla_tiempos_espera.setItem(n, 0, item_promedio_espera)

        # 2) Tiempos de Sistema
        self.ui.tabla_tiempos_sistema.setRowCount(n + 1)
        row_labels_sistema = list(self.tiempo_sistema.keys()) + ["PROM"]
        self.ui.tabla_tiempos_sistema.setVerticalHeaderLabels(row_labels_sistema)

        row = 0
        for pid, valor in self.tiempo_sistema.items():
            item = QTableWidgetItem(str(valor))
            self.ui.tabla_tiempos_sistema.setItem(row, 0, item)
            row += 1

        item_promedio_sistema = QTableWidgetItem(str(self.promedio_sistema))
        self.ui.tabla_tiempos_sistema.setItem(n, 0, item_promedio_sistema)

    def connectSignals(self):
        """
        Conecta los botones 'VOLVER' y 'MOSTRAR DIAGRAMA'.
        """
        self.ui.boton_volver.clicked.connect(self.volver)
        self.ui.boton_mostrar_diagrama.clicked.connect(self.mostrarDiagrama)

    def volver(self):
        """
        Cierra la ventana actual y vuelve a abrir la ventana tabla.
        """
        from ControllerWindows.controller_ventana_principal import ControllerVentanaPrincipal
        self.ventana_tabla = ControllerVentanaPrincipal()
        self.ventana_tabla.show()
        self.close()

    def mostrarDiagrama(self):
        from ControllerWindows.dibujar_diagrama_gantt import dibujar_gantt  # o la ruta donde definiste la función
        dibujar_gantt(self.intervals, titulo=f"Gantt - {self.algoritmo}")
