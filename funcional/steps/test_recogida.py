import datetime as dt

from pytest_bdd import parsers, scenarios, then, when

from pages.recogida_page import RecogidaPage
from support.config import URL_FRONT

scenarios("recogida.feature")


def dentro_de_dos_dias_habiles() -> str:
    d = dt.datetime.now(dt.timezone(dt.timedelta(hours=-5))).date() + dt.timedelta(days=2)
    return (d + dt.timedelta(days=1) if d.isoweekday() == 7 else d).isoformat()


@when(parsers.parse('solicito una recogida en "{ciudad}" para dentro de dos días hábiles'), target_fixture="recogida")
def solicitar(page, ciudad):
    recogida = RecogidaPage(page, URL_FRONT)
    recogida.solicitar(ciudad, dentro_de_dos_dias_habiles())
    return recogida


@then(parsers.parse('veo un número de recogida que empieza por "{prefijo}"'))
def numero(recogida, prefijo):
    assert recogida.numero().startswith(prefijo)


@then("veo un código de gestión de ocho caracteres")
def codigo(recogida):
    assert len(recogida.codigo()) == 8
