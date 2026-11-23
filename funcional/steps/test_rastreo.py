from pytest_bdd import given, parsers, scenarios, then, when

from pages.rastreo_page import RastreoPage
from support import api
from support.config import URL_FRONT

scenarios("rastreo.feature")


@given(parsers.parse('que existe un envío registrado de "{remitente}" para "{destinatario}"'))
def envio_existente(contexto_prueba, remitente, destinatario):
    contexto_prueba.update(guia=api.registrar_envio(remitente, destinatario), nombres=(remitente, destinatario))


@when("rastreo ese envío sin iniciar sesión", target_fixture="rastreo")
def rastrear(page, contexto_prueba):
    rastreo = RastreoPage(page, URL_FRONT)
    rastreo.rastrear(contexto_prueba["guia"])
    return rastreo


@then(parsers.parse('veo el estado "{estado}"'))
def estado(rastreo, estado):
    assert estado in rastreo.texto()


@then(parsers.parse('veo los nombres "{remitente}" y "{destinatario}"'))
def nombres_enmascarados(rastreo, remitente, destinatario):
    texto = rastreo.texto()
    assert remitente in texto and destinatario in texto


@then("no veo los nombres completos")
def sin_nombres(rastreo, contexto_prueba):
    texto = rastreo.texto()
    assert all(n not in texto for n in contexto_prueba["nombres"])
