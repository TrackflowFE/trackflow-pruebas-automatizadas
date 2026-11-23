"""Hooks: un navegador por sesión, un contexto limpio por escenario y captura al final de cada uno."""
import re
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from pages.base_page import BasePage
from support.config import NAVEGADOR, URL_FRONT, VISIBLE

CAPTURAS = Path(__file__).parent / "reports" / "capturas"


@pytest.fixture(scope="session")
def navegador():
    with sync_playwright() as p:
        b = getattr(p, NAVEGADOR).launch(headless=not VISIBLE)
        yield b
        b.close()


@pytest.fixture
def page(navegador, request):
    contexto = navegador.new_context(viewport={"width": 1366, "height": 900}, locale="es-CO",
                                     timezone_id="America/Bogota")
    pagina = contexto.new_page()
    pagina.set_default_timeout(15000)
    yield pagina
    CAPTURAS.mkdir(parents=True, exist_ok=True)
    nombre = re.sub(r"[^\w-]+", "_", request.node.name)[:80]
    pagina.screenshot(path=str(CAPTURAS / f"{NAVEGADOR}_{nombre}.png"), full_page=True)
    contexto.close()


@pytest.fixture
def contexto_prueba():
    """Datos que los pasos de un escenario comparten (guía, radicado, correo...)."""
    return {}


@pytest.fixture
def base(page):
    return BasePage(page, URL_FRONT)
