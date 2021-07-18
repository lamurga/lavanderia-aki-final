from zeep import Client

import logging

logger = logging.getLogger()


class ClientWSDL:
    def __init__(self):
        self.__wsdl = None

    @property
    def wsdl(self):
        return self.__wsdl

    @wsdl.setter
    def wsdl(self, value):
        self.__wsdl = Client(value)

    def get_wsdl_providers(self):
        if self.wsdl and hasattr(self.wsdl.service, 'getAllProviders'):
            try:
                return self.wsdl.service.getAllProviders()
            except Exception as exp:
                logger.warning(repr(exp), exc_info=True)
        return ''
