import json
import logging

import requests
from flask import Flask, request, Response
from flask_rabmq import RabbitMQ

from aki.models.base import Session
from aki.models.empleados import EmployeesModel
from aki.utils.twilio import TwilioWhatsapp

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ACCOUNT_SID'] = 'ACc59a40f67abcb7799b31203adf7266a6'
app.config['AUTH_TOKEN'] = '62c672c95576b6a5c76277b91e0ed76f'
app.config['FROM_WHATSAPP_NUMBER'] = 'whatsapp:+14155238886'

logging.basicConfig(format='%(asctime)s %(process)d,%(threadName)s %(filename)s:%(lineno)d [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

app.config.setdefault('RABMQ_RABBITMQ_URL', 'amqps://ziaajaez:e7_iKeEclkgZgCnpMy_POTe7e9xtFPDn@fish.rmq.cloudamqp.com/ziaajaez')
app.config.setdefault('RABMQ_SEND_EXCHANGE_NAME', 'flask_rabmq')
app.config.setdefault('RABMQ_SEND_EXCHANGE_TYPE', 'topic')

ramq = RabbitMQ()
ramq.init_app(app=app)


@app.route('/')
def heart():
    return {"lavanderia": "aki"}


@app.route('/empleados/nuevo/', methods=['POST'])
def handle_new_employee():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            if data.get('first_name') and data.get('document'):
                session = Session()
                exists_emp = session.query(EmployeesModel).filter(EmployeesModel.document == data['document']).first()
                if exists_emp is not None:
                    return {"status": "error", "message": "already exists"}

                values = {
                    'first_name': data['first_name'],
                    'last_name': data.get('last_name'),
                    'street': data.get('street'),
                    'document': data['document'],
                    'phone': data.get('phone'),
                    'district': data.get('district'),
                }
                new_employee = EmployeesModel(**values)

                session.add(new_employee)
                session.commit()

                return {"status": "success", "message": f"employee {new_employee.first_name} has been created successfully."}
            else:
                return {"status": "error", "message": "Data required"}
        else:
            return {"status": "error", "message": "The request payload is not in JSON format"}


@app.route('/empleados/', methods=['GET'])
def handle_employees():
    if request.method == 'GET':
        session = Session()
        employees = session.query(EmployeesModel).all()

        results = [
            {
                "id": employee.id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "street": employee.street,
                "document": employee.document,
                "phone": employee.phone,
                "district": employee.district
            } for employee in employees]

        return {"count": len(results), "employees": results, "status": "success"}


@app.route('/whatsapp/', methods=['POST', 'GET'])
def whatsapp():
    if request.method == 'POST':
        data = request.form.to_dict()
        if data:
            instance = TwilioWhatsapp(app.config, ramq, **data)
            message = instance.send_whatsapp_message()
            if message:
                return Response(status=200)
        return Response(status=400)
    return Response(status=404)


@app.route('/send-message/', methods=['POST', 'GET'])
def send_message():
    if request.method == 'POST':
        data = dict(request.json)
        ramq.send(
            {
                "message_id": 555555,
                "from": "MyMailinatorTest",
                "to": "dsdjonathan",
                "subject": "Trabajo final DSD",
                "text": data.get("text")
            },
            routing_key='flask_rabmq.test',
            exchange_name='flask_rabmq'
        )
    else:
        ramq.send(
            {
                "message_id": 111111, "message": "Mensajería con colas CloudAMQ", "status": "enviando"
            },
            routing_key='flask_rabmq.test',
            exchange_name='flask_rabmq'
        )
    return {'success': True, "message": "enviado!"}


@app.route('/webhooks/', methods=['GET', 'POST'])
def flask_rabmq_webhooks():
    return {'success': True}


@ramq.queue(exchange_name='flask_rabmq', routing_key='flask_rabmq.test')
def flask_rabmq_test(body):
    logger.info("Recibiendo mensaje")
    logger.info(body)
    data = json.loads(body)
    if data.get('from') == 'MyMailinatorTest':
        try:
            requests.post(
                url="https://www.mailinator.com/api/v2/domains/public/webhook/",
                data=json.dumps(data)
            )
        except Exception as e:
            logger.error(e)
            pass

    return {'success': True}

ramq.run_consumer()

