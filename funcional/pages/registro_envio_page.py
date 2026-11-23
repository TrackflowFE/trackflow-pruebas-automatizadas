import re

from playwright.sync_api import expect

from .base_page import BasePage


class RegistroEnvioPage(BasePage):
    # Localizadores
    CAMPOS = {"rem_nombre": "input[name=rem_nombre]", "rem_doc": "input[name=rem_doc]", "rem_tel": "input[name=rem_tel]",
              "rem_dir": "input[name=rem_dir]", "des_nombre": "input[name=des_nombre]", "des_doc": "input[name=des_doc]",
              "des_tel": "input[name=des_tel]", "des_dir": "input[name=des_dir]"}
    DESCRIPCION = "textarea[name=descripcion]"
    BOTON_REGISTRAR = "REGISTRAR ENVÍO"
    GUIA = re.compile(r"\bTF[0-9A-Z]{12}\b")

    def registrar(self, datos: dict, origen: str, destino: str, descripcion: str):
        for campo, valor in datos.items():
            self.page.fill(self.CAMPOS[campo], valor)
        self.escoger_ciudad(0, origen)
        self.escoger_ciudad(1, destino)
        self.page.fill(self.DESCRIPCION, descripcion)
        self.page.get_by_role("button", name=self.BOTON_REGISTRAR).click()
        expect(self.page.get_by_text("Solicitud recibida")).to_be_visible()

    def guia(self) -> str | None:
        m = self.GUIA.search(self.contenido())
        return m.group(0) if m else None

    def boton_imprimir(self):
        return self.page.get_by_role("button", name="Imprimir comprobante")
