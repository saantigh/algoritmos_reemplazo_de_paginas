# ControllerWindows/controller_ventana_resultados.py

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QColor, QBrush
from DesignWindows.ventana_resultados import Ui_MainWindow as Ui_VentanaResultados

class ControllerVentanaResultados(QMainWindow):
    def __init__(self, referencia, matrix, faults, total_faults, algoritmo, parent_window):
        """
        referencia      -- lista de referencia de páginas
        matrix          -- lista de listas con el estado de cada marco por columna
        faults          -- lista con '*' o '' indicando fallo por columna
        total_faults    -- entero, total de fallos
        algoritmo       -- nombre del algoritmo (str)
        parent_window   -- instancia de ControllerVentanaCalculo
        """
        super().__init__()
        self.ui = Ui_VentanaResultados()
        self.ui.setupUi(self)

        self.referencia = referencia
        self.matrix = matrix
        self.faults = faults
        self.total_faults = total_faults
        self.algoritmo = algoritmo
        # guardamos la referencia a la ventana anterior
        self.parent = parent_window

        self._populate()
        self.ui.boton_volver.clicked.connect(self.volver)

    def _populate(self):
        tw = self.ui.matriz_resultados
        refs = self.referencia
        matrix = self.matrix      # lista de listas: cada sublista es el estado de un marco
        faults = self.faults      # lista de '*' o '' por cada referencia
        marcos = len(matrix)
        cols = len(refs)

        # Total de filas = 1 (referencia) + marcos + 1 (fallos)
        total_rows = 1 + marcos + 1

        tw.setColumnCount(cols)
        tw.setRowCount(total_rows)
        tw.horizontalHeader().setVisible(False)
        tw.verticalHeader().setVisible(False)
        tw.setStyleSheet("""
            QTableWidget { 
               background-color: rgb(33,33,33);
               color: white;
               gridline-color: #555555;
            }
        """)

        # 1) Fila 0: lista de referencia en azul oscuro
        from PyQt5.QtGui import QColor, QBrush
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QTableWidgetItem

        for c, val in enumerate(refs):
            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QBrush(QColor("#003366")))   # azul oscuro
            item.setForeground(QBrush(QColor("white")))
            tw.setItem(0, c, item)

        # 2) Filas 1..marcos: estados de los marcos
        for f in range(marcos):
            row_idx = 1 + f
            for c in range(cols):
                v = matrix[f][c]
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignCenter)
                tw.setItem(row_idx, c, item)

        # 3) Última fila: fallos ('*' o '')
        fault_row = total_rows - 1
        for c, mark in enumerate(faults):
            item = QTableWidgetItem(mark)
            item.setTextAlignment(Qt.AlignCenter)
            if mark == "*":
                item.setForeground(QBrush(QColor("red")))
            tw.setItem(fault_row, c, item)

        # Actualizar labels
        self.ui.subtitulo_algoritmo_seleccionado.setText(
            f"ALGORITMO SELECCIONADO: {self.algoritmo}"
        )
        self.ui.subtitulo_algoritmo_seleccionado.setEnabled(True)

        self.ui.label_numero_fallos.setText(
            f"NUMERO DE FALLOS: {self.total_faults}"
        )
        self.ui.label_numero_fallos.setEnabled(True)

    def volver(self):
        # re-habilitamos los controles en la ventana calculo
        pw = self.parent
        pw.ui.ingresar_marcos.setEnabled(True)
        pw.ui.boton_confirmar_marcos.setEnabled(True)
        pw.ui.seleccionar_algoritmo.setEnabled(False)
        pw.ui.boton_confirmar_algoritmo.setEnabled(False)
        pw.ui.boton_calcular_algoritmo.setEnabled(False)
        self.close()

            
