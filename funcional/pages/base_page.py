"""Acciones comunes a todas las pantallas: navegación por el menú superior y avisos."""
from playwright.sync_api import Page, expect


class BasePage:
    # Localizadores
    MENU = "header"
    ENVIAR_FORMULARIO = "form button[type=submit]"

    def __init__(self, page: Page, url_base: str):
        self.page = page
        self.url_base = url_base

    def abrir(self):
        self.page.goto(self.url_base + "/")
        self.page.wait_for_load_state("networkidle")

    def ir_a(self, opcion: str):
        self.page.get_by_role("button", name=opcion, exact=True).first.click()
        self.page.wait_for_load_state("networkidle")

    def enviar(self):
        self.page.locator(self.ENVIAR_FORMULARIO).first.click()

    def escoger_ciudad(self, campo: int, ciudad: str):
        """Autocompletado de ciudades: escribe las primeras letras y elige la opción exacta."""
        buscador = self.page.get_by_placeholder("Escribe para buscar").nth(campo)
        buscador.fill(ciudad[:4])
        self.page.locator("li", has_text=ciudad).first.click()

    def contenido(self) -> str:
        return self.page.locator("main").first.inner_text()

    def ver_texto(self, texto: str):
        expect(self.page.get_by_text(texto, exact=False).first).to_be_visible()
