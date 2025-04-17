# ControllerWindows/controller_ventana_tabla.py

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QMessageBox
from PyQt5.QtCore import Qt
from DesignWindows.ventana_tabla import Ui_MainWindow as Ui_VentanaTabla
from ControllerWindows.simulador_procesos import SimuladorProcesos
from ControllerWindows.controller_ventana_resultados import ControllerVentanaResultados

class ControllerVentanaTabla(QMainWindow):
    def __init__(self, num_procesos):
        super().__init__()
        self.num_procesos = num_procesos
        self.ui = Ui_VentanaTabla()
        self.ui.setupUi(self)
        self.setupTable()
        self.setupVisibility()
        self.connectSignals()

    def setupTable(self):
        """
        Configura la tabla:
         - Se establecen 'num_procesos' filas.
         - Se asignan los encabezados verticales como 'P1', 'P2', …, 'Pn'.
         - Las celdas de las dos columnas (Ráfaga y Tiempo de llegada) quedan vacías y editables.
        """
        # La tabla tiene 2 columnas ya definida en el diseño.
        self.ui.tabla_procesos.setRowCount(self.num_procesos)
        # Establecemos los encabezados verticales (IDs) usando setVerticalHeaderLabels
        headers = [f"P{i+1}" for i in range(self.num_procesos)]
        self.ui.tabla_procesos.setVerticalHeaderLabels(headers)
        # (Opcional) Si deseas inicializar las celdas de las columnas, puedes hacerlo:
        for i in range(self.num_procesos):
            # Columna 0: Ráfaga (editable)
            self.ui.tabla_procesos.setItem(i, 0, QTableWidgetItem(""))
            # Columna 1: Tiempo de llegada (editable)
            self.ui.tabla_procesos.setItem(i, 1, QTableWidgetItem(""))

    def setupVisibility(self):
        """
        Inicialmente se ocultan los widgets relacionados con el Quantum.
        Además, se deshabilita el botón SIMULAR.
        """
        self.ui.subtitulo_quantum.setVisible(False)
        self.ui.seleccionador_quantum.setVisible(False)
        self.ui.boton_seleccionar_quantum.setVisible(False)
        self.ui.boton_simular.setEnabled(False)

    def connectSignals(self):
        """
        Conecta los eventos de los botones:
         - BOTÓN VOLVER: vuelve a la ventana principal.
         - BOTÓN SELECCIONAR ALGORITMO: gestiona la selección del algoritmo.
         - BOTÓN SELECCIONAR QUANTUM: para Round Robin, habilita SIMULAR si el quantum es válido.
         - BOTÓN SIMULAR: Verifica que todo esté correcto en la tabla antes de enviar los datos a los algoritmos
        """
        self.ui.boton_volver.clicked.connect(self.volver)
        self.ui.boton_seleccionar_algoritmo.clicked.connect(self.seleccionarAlgoritmo)
        self.ui.boton_seleccionar_quantum.clicked.connect(self.seleccionarQuantum)
        self.ui.boton_simular.clicked.connect(self.simular)

    def volver(self):
        """
        Cierra la ventana actual y vuelve a abrir la ventana principal.
        """
        from ControllerWindows.controller_ventana_principal import ControllerVentanaPrincipal
        self.ventana_principal = ControllerVentanaPrincipal()
        self.ventana_principal.show()
        self.close()

    def seleccionarAlgoritmo(self):
        """
        Al hacer clic en 'SELECCIONAR' para el algoritmo:
          - Si se elige FIFO o SJF: habilita directamente el botón SIMULAR.
          - Si se elige ROUND ROBIN: muestra los widgets de quantum y deja deshabilitado SIMULAR hasta seleccionar un quantum.
        """
        alg = self.ui.seleccionador_algoritmo.currentText().strip().upper()
        if alg in ["FIFO", "SJF"]:
            self.ui.boton_simular.setEnabled(True)
            # Asegúrate de ocultar los widgets de quantum si se mostraron anteriormente.
            self.ui.subtitulo_quantum.setVisible(False)
            self.ui.seleccionador_quantum.setVisible(False)
            self.ui.boton_seleccionar_quantum.setVisible(False)
        elif alg == "ROUND ROBIN":
            self.ui.subtitulo_quantum.setVisible(True)
            self.ui.seleccionador_quantum.setVisible(True)
            self.ui.boton_seleccionar_quantum.setVisible(True)
            self.ui.boton_simular.setEnabled(False)
        else:
            self.ui.boton_simular.setEnabled(False)

    def seleccionarQuantum(self):
        """
        Al hacer clic en 'SELECCIONAR' para el quantum, se verifica que el valor
        seleccionado sea válido y se habilita el botón SIMULAR.
        """
        quantum_str = self.ui.seleccionador_quantum.currentText()
        try:
            quantum = int(quantum_str)
            if quantum >= 1:
                self.ui.boton_simular.setEnabled(True)
            else:
                self.ui.boton_simular.setEnabled(False)
        except ValueError:
            self.ui.boton_simular.setEnabled(False)


    def simular(self):
        simulador = SimuladorProcesos(self.ui.tabla_procesos,
                                    self.ui.seleccionador_algoritmo,
                                    self.ui.seleccionador_quantum)
        result = simulador.simular(self)  # 'self' se pasa como parent para los mensajes
        if result is None:
            return  # Error en validación o ejecución
        intervals, tiempo_sistema, tiempo_espera, promedio_tiempo_sistema, promedio_tiempo_espera = result

         # Llamar a la ventana de resultados
        algoritmo = self.ui.seleccionador_algoritmo.currentText().strip().upper()
        self.ventana_resultados = ControllerVentanaResultados(
            algoritmo=algoritmo,
            intervals=intervals,
            tiempo_espera=tiempo_espera,
            tiempo_sistema=tiempo_sistema,
            promedio_espera=promedio_tiempo_espera,
            promedio_sistema=promedio_tiempo_sistema
        )
        self.ventana_resultados.show()
        # Si deseamos, puedes cerrar esta ventana o mantenerla abierta
        self.close()
            
