import re
import time

from pytest_bdd import given, parsers, scenarios, then, when

from pages.pqr_page import PqrPage
from support.config import URL_FRONT

scenarios("pqr.feature")


@given(parsers.parse('que radiqué una "{tipo}" con la descripción "{descripcion}"'), target_fixture="pqr")
@when(parsers.parse('radico una "{tipo}" con la descripción "{descripcion}"'), target_fixture="pqr")
def radicar(page, contexto_prueba, tipo, descripcion):
    pqr = PqrPage(page, URL_FRONT)
    correo = f"cliente{int(time.time() * 1000)}@trackflow.test"
    pqr.radicar(tipo, descripcion, correo)
    contexto_prueba.update(radicado=pqr.radicado(), correo=correo)
    return pqr


@when(parsers.parse('consulto el radicado con el correo "{correo}"'))
def consultar(pqr, contexto_prueba, correo):
    pqr.consultar(contexto_prueba["radicado"], correo)


@then(parsers.parse('veo un radicado con formato "PQR-AAAA-NNNNN"'))
def formato(contexto_prueba):
    assert re.fullmatch(r"PQR-\d{4}-\d{5}", contexto_prueba["radicado"])


@then(parsers.parse('veo el estado "{estado}"'))
def estado(pqr, estado):
    assert f"Estado: {estado}" in pqr.contenido()


@then(parsers.parse('veo el aviso "{aviso}"'))
def aviso(pqr, aviso):
    pqr.ver_texto(aviso)
