from playwright.sync_api import expect

from .base_page import BasePage


class ChatbotPage(BasePage):
    # Localizadores
    ABRIR = "Abrir el asistente"
    TEXTO = "input[name=texto]"
    ENVIAR = "Enviar"
    VENTANA = "[role=dialog]"

    def abrir_asistente(self):
        self.abrir()
        self.page.get_by_role("button", name=self.ABRIR).click()
        expect(self.page.locator(self.TEXTO)).to_be_visible()

    def preguntar(self, texto: str):
        self.page.fill(self.TEXTO, texto)
        self.page.get_by_role("button", name=self.ENVIAR).click()

    def ventana(self):
        return self.page.locator(self.VENTANA).last

    def boton(self, etiqueta: str):
        return self.ventana().get_by_role("button", name=etiqueta)
