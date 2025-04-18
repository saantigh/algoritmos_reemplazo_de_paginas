# Controller/controller_ventana_principal.py


from PyQt5.QtWidgets import QMainWindow, QMessageBox
from DesignWindows.ventana_principal import Ui_MainWindow
from ControllerWindows.controller_ventana_calculo import ControllerVentanaCalculo  # Asegúrate de tener este controlador implementado

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
        text = self.ui.campo_ingresar_cadena.text().strip()
        # 1) Validación: la cadena no debe estar vacía y debe contener solo dígitos
        if not text:
            QMessageBox.warning(self, "Cadena vacía",
                                "Por favor ingresa una cadena de dígitos.")
            return
        if not text.isdigit():
            QMessageBox.warning(self, "Formato inválido",
                                "Solo se permiten dígitos (0–9), sin espacios ni otros caracteres.")
            return

        # 2) Conversión a lista de enteros
        referencias = [int(caracter) for caracter in text]
        print(referencias)

        #Crear y mostrar la ventana de cálculo, pasándole la lista
        self.ventana_calculo = ControllerVentanaCalculo(referencias)
        self.ventana_calculo.show()
        # Opcional: cerrar u ocultar la ventana principal
        self.close()
        

