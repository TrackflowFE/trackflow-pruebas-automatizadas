import re

from playwright.sync_api import expect

from .base_page import BasePage


class PqrPage(BasePage):
    # Localizadores
    TIPO = "select[name=tipo]"
    NOMBRE = "input[name=contactoNombre]"
    CORREO = "input[name=contactoEmail]"
    DESCRIPCION = "textarea[name=descripcion]"
    ACEPTA = "input[name=aceptaTratamientoDatos]"
    RADICADO = "input[name=radicado]"
    CORREO_CONSULTA = "input[name=email]"

    def radicar(self, tipo: str, descripcion: str, correo: str):
        self.page.select_option(self.TIPO, label=tipo)
        self.page.fill(self.NOMBRE, "Ana Torres")
        self.page.fill(self.CORREO, correo)
        self.page.fill(self.DESCRIPCION, descripcion)
        self.page.check(self.ACEPTA)
        self.enviar()
        expect(self.page.get_by_text("Radicado:").first).to_be_visible()

    def radicado(self) -> str:
        return re.search(r"Radicado: (PQR-\d{4}-\d{5})", self.contenido()).group(1)

    def consultar(self, radicado: str, correo: str):
        self.ir_a("Consultar PQR")
        self.page.fill(self.RADICADO, radicado)
        self.page.fill(self.CORREO_CONSULTA, correo)
        self.enviar()
        self.page.wait_for_load_state("networkidle")
