from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.login_page import LoginPage
from support.config import CLAVES, URL_FRONT

scenarios("sesion.feature")


@given("que estoy en la pantalla de ingreso", target_fixture="login")
def pantalla_ingreso(page):
    login = LoginPage(page, URL_FRONT)
    login.abrir_ingreso()
    return login


@when(parsers.parse('ingreso con el usuario "{usuario}" y su clave'))
def ingresar_valido(login, usuario):
    login.ingresar(usuario, CLAVES[usuario])


@when(parsers.parse('ingreso con el usuario "{usuario}" y la clave "{clave}"'))
def ingresar_con_clave(login, usuario, clave):
    login.ingresar(usuario, clave)


@then(parsers.parse('veo la pantalla "{titulo}"'))
def veo_pantalla(page, titulo):
    expect(page.locator("h1").first).to_have_text(titulo)


@then(parsers.parse('veo el aviso "{aviso}"'))
def veo_aviso(login, aviso):
    login.ver_texto(aviso)
