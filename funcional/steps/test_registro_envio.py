from pytest_bdd import given, parsers, scenarios, then, when
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.registro_envio_page import RegistroEnvioPage
from support.config import CLAVES, URL_FRONT

scenarios("registro_envio.feature")

DATOS = {"rem_nombre": "Ana Torres", "rem_doc": "1000000001", "rem_tel": "3001234545", "rem_dir": "Calle 1 # 1-1",
         "des_nombre": "Luis Gómez", "des_doc": "2000000002", "des_tel": "3009876543", "des_dir": "Carrera 2 # 2-2"}


@given("que ingresé como operador", target_fixture="registro")
def ingreso_operador(page):
    login = LoginPage(page, URL_FRONT)
    login.abrir_ingreso()
    login.ingresar("operador", CLAVES["operador"])
    return RegistroEnvioPage(page, URL_FRONT)


@when(parsers.parse('registro un envío de "{origen}" a "{destino}"'))
def registrar(registro, origen, destino):
    registro.registrar(DATOS, origen, destino, "Caja con documentos")


@then("veo un número de guía con formato TF y doce caracteres")
def guia_valida(registro):
    assert registro.guia() is not None


@then("puedo imprimir el comprobante")
def imprimir(registro):
    expect(registro.boton_imprimir()).to_be_enabled()
