# Controller/controller_ventana_principal.py

from PyQt5.QtWidgets import QMainWindow
from DesignWindows.ventana_principal import Ui_MainWindow
from ControllerWindows.controller_ventana_tabla import ControllerVentanaTabla  # Asegúrate de tener este controlador implementado

class ControllerVentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conectarEventos()

    def conectarEventos(self):
        # Conecta el botón de salir para cerrar la aplicación
        self.ui.boton_salir.clicked.connect(self.salir)
        # Conecta el botón siguiente para abrir la ventana de tabla y enviarle el número de procesos
        self.ui.boton_siguiente.clicked.connect(self.siguiente)

    def salir(self):
        self.close()

    def siguiente(self):
        # Lee el número de procesos seleccionado en el QComboBox 'numero_de_procesos'
        num_procesos = int(self.ui.numero_de_procesos.currentText())
        # Instancia la ventana de la tabla, pasando el número de procesos
        self.ventana_tabla = ControllerVentanaTabla(num_procesos)
        self.ventana_tabla.show()
        self.close()  # Opcional: cierra la ventana principal


