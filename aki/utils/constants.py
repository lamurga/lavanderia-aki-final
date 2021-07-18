# coding: utf-8
DEFAULT_WELCOME_OPTION = 'HOLA'
MSG_WELCOME = "Soy el asistente virtual de Lavandería AKI. Absuelve tus consultas ingresando la letra:\n\n" \
              "*A)* Consultar mi pedido\n" \
              "*B)* Consulta proveedores \n" \
              "*C)* Comunicación con un asesor\n" \
              "*D)* Mensajes recibidos \n" \
              "*E)* Lugares de Atención \n"

MSG_UNKNOWN_CUSTOMER = "Estimado, favor comuníquese al *01-717-8866* a fin de registrarlo."
MSG_RETURN = "*R)* Regresar"

LIST_STATIC_OPTIONS = [
    DEFAULT_WELCOME_OPTION,
    'A', 'A.1',
    'B', 'B.1', 'B.2',
    'C', 'C.1', 'C.1.1',
    'D', 'D.1', 'D.2',
    'E', 'E.1',
]

DICT_MAIN_OPTIONS_ENABLED = {str(o): str(o) for o in ['A', 'B', 'C', 'D', 'E']}
DICT_OPTIONS = {
    DEFAULT_WELCOME_OPTION: DICT_MAIN_OPTIONS_ENABLED,
    'A': {
        'A1': "A.1",
        'R': DEFAULT_WELCOME_OPTION
    },
    'A.1': {'R': 'A'},
    'B': {
        'B1': "B.1",
        'B2': "B.2",
        'R': DEFAULT_WELCOME_OPTION
    },
    'B.1': {'R': 'B'},
    'B.2': {'R': 'B'},
    'C': {
        'C1': "C.1",
        'R': DEFAULT_WELCOME_OPTION
    },
    'C.1': {
        'param': "C.1.1",
        'R': 'C'
    },
    'D': {
        'D1': "D.1",
        'D2': "D.2",
        'R': DEFAULT_WELCOME_OPTION
    },
    'D.1': {'R': 'D'},
    'D.2': {'R': 'D'},
    'E': {
        'E1': "E.1",
        'R': DEFAULT_WELCOME_OPTION
    },
    'E.1': {
        'param': "E.1.1",
        'R': 'E'
    },
}
