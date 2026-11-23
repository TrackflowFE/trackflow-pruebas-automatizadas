from .base_page import BasePage


class LoginPage(BasePage):
    # Localizadores
    USUARIO = "input[name=usuario]"
    CLAVE = "input[name=clave]"

    def abrir_ingreso(self):
        self.abrir()
        self.ir_a("Ingresar")

    def ingresar(self, usuario: str, clave: str):
        self.page.fill(self.USUARIO, usuario)
        self.page.fill(self.CLAVE, clave)
        self.enviar()
        self.page.wait_for_load_state("networkidle")

