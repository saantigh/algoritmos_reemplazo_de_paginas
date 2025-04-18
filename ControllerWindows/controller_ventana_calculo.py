# ControllerWindows/controller_ventana_calculo.py

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from DesignWindows.ventana_calculo import Ui_MainWindow as Ui_VentanaCalculo
#from ControllerWindows.controller_ventana_calculo import ControllerVentanaResultados
# Importa tus módulos de algoritmos de reemplazo de páginas
from Algoritmos.algoritmos import Algoritmos

class ControllerVentanaCalculo(QMainWindow):
    def __init__(self, referencia_list):
        super().__init__()
        self.ui = Ui_VentanaCalculo()
        self.ui.setupUi(self)
        # Lista de referencia que viene de la ventana principal
        self.referencias = referencia_list  # e.g. [2,3,2,3,5,...]
        self.marcos = None
        self.algoritmo = None
        self.result_window = None  # Para mantener referencia
        self._fill_referencias()
        self._connect_signals()

    def _fill_referencias(self):
        # Rellena la QTableWidget con 1 fila y tantas columnas como elementos
        refs = self.referencias
        tw = self.ui.tabla_referencias
        tw.setRowCount(1)
        tw.setColumnCount(len(refs))
        tw.verticalHeader().setVisible(False)
        tw.horizontalHeader().setVisible(False)
        # Ajusta estilo: texto blanco en todas las celdas
        tw.setStyleSheet("""
            QTableWidget {
                background-color: #343434;
                color: white;            /* Texto en blanco */
                gridline-color: #555555;
            }
        """)
        for col, val in enumerate(refs):
            itm = QTableWidgetItem(str(val))
            itm.setTextAlignment(QtCore.Qt.AlignCenter)
            tw.setItem(0, col, itm)

    def _connect_signals(self):
        self.ui.boton_volver.clicked.connect(self._volver)
        self.ui.boton_confirmar_marcos.clicked.connect(self._confirmar_marcos)
        self.ui.boton_confirmar_algoritmo.clicked.connect(self._confirmar_algoritmo)
        self.ui.boton_calcular_algoritmo.clicked.connect(self._calcular_algoritmo)

    def _volver(self):
        from ControllerWindows.controller_ventana_principal import ControllerVentanaPrincipal
        # Regresa a la ventana principal
        self.principal = ControllerVentanaPrincipal()
        self.principal.show()
        self.close()

    def _confirmar_marcos(self):
        texto = self.ui.ingresar_marcos.text().strip()
        if not texto.isdigit():
            QMessageBox.warning(self, "Error", "El número de marcos debe ser un entero válido.")
            return
        self.marcos = int(texto)
        # Deshabilita la entrada y el botón
        self.ui.ingresar_marcos.setEnabled(False)
        self.ui.boton_confirmar_marcos.setEnabled(False)
        # Habilita selección de algoritmo
        self.ui.seleccionar_algoritmo.setEnabled(True)
        self.ui.boton_confirmar_algoritmo.setEnabled(True)

    def _confirmar_algoritmo(self):
        self.algoritmo = self.ui.seleccionar_algoritmo.currentText().strip()
        # Deshabilita la selección y el botón
        self.ui.seleccionar_algoritmo.setEnabled(False)
        self.ui.boton_confirmar_algoritmo.setEnabled(False)
        # Habilita el cálculo
        self.ui.boton_calcular_algoritmo.setEnabled(True)

    def _calcular_algoritmo(self):
        if self.marcos is None:
            QMessageBox.warning(self, "Error", "Debe confirmar primero el número de marcos.")
            return
        if not self.algoritmo:
            QMessageBox.warning(self, "Error", "Debe confirmar primero el algoritmo a usar.")
            return

        # Ejecuta el algoritmo elegido
        algoritmos=Algoritmos()
        try:
            if self.algoritmo == "FIFO":
                matrix, faults_per_column, total_faults = algoritmos.fifo(self.referencias, self.marcos)
            elif self.algoritmo == "LRU":
                matrix, faults_per_column, total_faults = algoritmos.lru(self.referencias, self.marcos)
            elif self.algoritmo == "OPTIMO":
                matrix, faults_per_column, total_faults = algoritmos.optimo(self.referencias, self.marcos)
            elif self.algoritmo == "FIFO MEJORADO":
                matrix, faults_per_column, total_faults = algoritmos.fifo_mejorado(self.referencias, self.marcos)
            else:
                raise ValueError("Algoritmo no reconocido")
        except Exception as e:
            QMessageBox.critical(self, "Error al ejecutar algoritmo", str(e))
            return

        # Abre la ventana de resultados y le pasa los datos
        #self.result_window = ControllerVentanaResultados(
        #    matrix, faults_per_column, total_faults, self.algoritmo
        #)
        #self.result_window.show()

        # (Opcional) podrías esconder esta ventana si no quieres que quede visible
        # self.hide()
