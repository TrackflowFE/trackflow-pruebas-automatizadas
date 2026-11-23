"""Pasos compartidos por varias características."""
from pytest_bdd import given, parsers

from pages.base_page import BasePage
from support.config import URL_FRONT


@given(parsers.parse('que estoy en la pantalla "{pantalla}"'))
def en_pantalla(page, pantalla):
    p = BasePage(page, URL_FRONT)
    p.abrir()
    p.ir_a(pantalla)
