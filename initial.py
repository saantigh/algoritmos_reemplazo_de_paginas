import sys
from PyQt5.QtWidgets import QApplication
from ControllerWindows.controller_ventana_principal import ControllerVentanaPrincipal


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = ControllerVentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())
    