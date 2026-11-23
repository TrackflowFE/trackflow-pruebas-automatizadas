from pytest_bdd import given, parsers, scenarios, then, when
from playwright.sync_api import expect

from pages.chatbot_page import ChatbotPage
from support.config import URL_FRONT

scenarios("chatbot.feature")


@given("que abrí el asistente", target_fixture="chat")
def abrir(page):
    chat = ChatbotPage(page, URL_FRONT)
    chat.abrir_asistente()
    return chat


@when(parsers.parse('pregunto "{texto}"'))
def preguntar(chat, texto):
    chat.preguntar(texto)


@then(parsers.parse('el asistente responde con un texto que contiene "{fragmento}"'))
def responde(chat, fragmento):
    expect(chat.ventana()).to_contain_text(fragmento)


@then(parsers.parse('me ofrece el botón "{etiqueta}"'))
def ofrece(chat, etiqueta):
    expect(chat.boton(etiqueta)).to_be_visible()
