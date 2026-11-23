from playwright.sync_api import expect

from .base_page import BasePage


class RastreoPage(BasePage):
    # Localizadores
    GUIA = "input[name=tn]"

    def rastrear(self, guia: str):
        self.abrir()
        self.page.fill(self.GUIA, guia)
        self.enviar()
        expect(self.page.get_by_text("NÚMERO DE GUÍA")).to_be_visible()

    def texto(self) -> str:
        return self.page.locator("body").inner_text()
