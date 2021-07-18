import logging

from typing import Dict

import requests
from sqlalchemy import text
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from aki.models.base import engine
from aki.utils.constants import DICT_OPTIONS, LIST_STATIC_OPTIONS, DEFAULT_WELCOME_OPTION, MSG_WELCOME, MSG_RETURN
from aki.utils.wdsl import ClientWSDL

logger = logging.getLogger()


class TwilioWhatsapp:

    def __init__(self, settings, ramq, **kwargs):
        self.client = Client(settings.get('ACCOUNT_SID'), settings.get('AUTH_TOKEN'))
        self.client_wsdl = ClientWSDL()
        self.service_providers = 'C:/projects/lavanderia-aki/aki/data/providers.wsdl'
        self.from_whatsapp_number = settings['FROM_WHATSAPP_NUMBER'] or self.data.get('To')
        self.menu_options = DICT_OPTIONS
        self.static_options = LIST_STATIC_OPTIONS
        self.data = self.clean(kwargs)
        self._option = DEFAULT_WELCOME_OPTION
        self.ramq = ramq
        self._param = None

    @staticmethod
    def clean(data) -> Dict[str, str]:
        from markupsafe import escape
        try:
            return {d[0]: escape(d[1]) for d in data.items()}
        except AttributeError:
            return {}

    @property
    def to_whatsapp_number(self):
        return "%s" % self.data.get('From')

    @property
    def user_message(self):
        return "%s" % self.data.get('Body')

    def update_option(self):
        user_entry = self.user_message.upper()
        if user_entry not in [DEFAULT_WELCOME_OPTION, 'R']:
            self._option = user_entry[:1]
        if len(user_entry) > 3 and user_entry != DEFAULT_WELCOME_OPTION:
            self._option = 'C.1'
        elif user_entry.startswith("C-"):
            self._option = 'A.1'
        if self.menu_options.get(self._option):
            if len(user_entry) < 3 and user_entry in list(self.menu_options[self._option]):
                self._option = self.menu_options[self._option][user_entry]
            elif 'param' in list(self.menu_options[self._option]):
                self._param = user_entry
                self._option = self.menu_options[self._option]['param']

    def get_static_message(self):
        if self._option == DEFAULT_WELCOME_OPTION:
            return 'Hola. {}'.format(MSG_WELCOME)
        elif self._option == 'A':
            return '{}\n\n{}'.format(
                "Ingresa C- más tu código de pedido: Ejemplo C-101010",
                MSG_RETURN
            )
        elif self._option == 'A.1':
            with engine.connect() as connection:
                t = text("")
                result = connection.execute(t)
            return None
        elif self._option == 'B':
            return '{}\n{}\n\n{}'.format(
                "*B1)* Ingresa código de proveedor",
                "*B2)* Lista de proveedores",
                MSG_RETURN
            )
        elif self._option == 'B.2':
            self.client_wsdl.wsdl = self.service_providers
            response = self.client_wsdl.get_wsdl_providers()
            if response:
                values = "\n".join(['```Nombre:{}\nCategoría:{}\n```'.format(r['title'], r['category'])
                                    for r in response])
                _msg = "Proveedores registrados:\n\n{}".format(values)
                return "{}\n\n{}".format(_msg, MSG_RETURN)
        elif self._option == 'C':
            return '{}\n\n{}'.format(
                "Escribe tu mensaje:",
                MSG_RETURN
            )
        elif self._option == 'C.1.1':
            self.ramq.send(
                {
                    "message_id": 555555,
                    "from": "MyMailinatorTest",
                    "to": "dsdjonathan",
                    "subject": "Trabajo final DSD",
                    "text": self.user_message
                },
                routing_key='flask_rabmq.test',
                exchange_name='flask_rabmq'
            )
            return '{}\n\n{}'.format(
                "Mensaje enviado!",
                MSG_RETURN
            )
        elif self._option == 'D':
            return '{}\n{}\n\n{}'.format(
                "*D1)* Ver últimos mensajes",
                "*D2)* Ingresar código de ticket",
                MSG_RETURN
            )
        elif self._option == 'D.1':

            response = requests.get('https://www.mailinator.com/v2/domains/private/inboxes/testinbox')
            if response:
                values = "\n".join(['```Nombre:{}\nCategoría:{}\n```'.format(r['title'], r['category'])
                                    for r in response])
                _msg = "Proveedores registrados:\n\n{}".format(values)
                return "{}\n\n{}".format(_msg, MSG_RETURN)
        return MSG_RETURN

    def prepare_message(self):
        self.update_option()
        if self._option in self.static_options:
            return self.get_static_message()
        return ''

    def send_whatsapp_message(self):
        body_message = self.prepare_message()
        if body_message:
            try:
                return self.client.messages.create(
                    from_=self.from_whatsapp_number,
                    body=body_message,
                    to=self.to_whatsapp_number
                )
            except TwilioRestException as exp:
                logger.error(exp.msg, exc_info=True)
        return None

