import re

from playwright.sync_api import expect

from .base_page import BasePage


class RecogidaPage(BasePage):
    # Localizadores
    DIRECCION = "input[name=address]"
    CONTACTO = "input[name=contactName]"
    TELEFONO = "input[name=contactPhone]"
    FECHA = "input[name=scheduledDate]"
    FRANJA = "select[name=timeSlot]"
    TAMANO = "select[name=packageSize]"
    PESO = "input[name=weightKg]"

    def solicitar(self, ciudad: str, fecha: str, franja="08:00-10:00", peso="5"):
        self.escoger_ciudad(0, ciudad)
        self.page.fill(self.DIRECCION, "Calle 45 # 12-30")
        self.page.fill(self.CONTACTO, "Ana Torres")
        self.page.fill(self.TELEFONO, "3001234567")
        self.page.fill(self.FECHA, fecha)
        self.page.select_option(self.FRANJA, franja)
        self.page.select_option(self.TAMANO, label="Mediano")
        self.page.fill(self.PESO, peso)
        self.enviar()
        expect(self.page.get_by_text("Solicitud aceptada")).to_be_visible()

    def numero(self) -> str:
        return re.search(r"Solicitud aceptada: (\S+)", self.contenido()).group(1)

    def codigo(self) -> str:
        return re.search(r"Código de gestión: (\S+)", self.contenido()).group(1)
