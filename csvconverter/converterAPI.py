from flask import Flask, jsonify
from flask_restful import Resource, Api
import pika
import xml.etree.ElementTree as ET

app = Flask(__name__)
api = Api(app)
rows = ''


def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))


def get_channel(connection):
    return connection.channel()


def get_channel_csv(connection):
    return connection.channel()


def stop_connection(connection):
    connection.close()


# Following method deals with getting data from XML and changing it into comma separated values
def parseXML(body):
    global rows
    xml_data = ET.fromstring("<root>" + body + "</root>")
    rows = ''
    for child_of_root in xml_data:

        for text_block in child_of_root:
            columns = ''
            for text_line in text_block:
                column_data = ''
                for string_content in text_line:
                    attribs = string_content.attrib
                    if 'CONTENT' in attribs:  # get the attribute content's value
                        column_data = column_data + string_content.attrib['CONTENT']

                columns = columns + column_data
            rows = rows + columns + ','
        rows = rows + '\n'
    print rows

    return 'Successful'


@app.route('/converter', methods=['POST'])
def get_task():
    global rows

    # Following code block deals with getting message from RabbitMQ for XML conversion

    connection = get_connection()
    channel = get_channel(connection)
    channel_csv = get_channel_csv(connection)

    channel.queue_declare(queue='xmltocsv')
    channel_csv.queue_delete(queue='csvconversion')
    channel_csv.queue_declare(queue='csvconversion')

    method_frame, header_frame, body = channel.basic_get(queue='xmltocsv')

    # Following code ensures that we get only one message from the queue and then closes the connection

    if method_frame.NAME == 'Basic.GetEmpty':
        stop_connection(connection)
        return ''
    else:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        stop_connection(connection)
        parseXML(body)

        # Following block deals with publishing message on RabbitMQ csvconversion queue for GUI

        connection = get_connection()
        channel_csv = get_channel_csv(connection)

        channel_csv.queue_declare(queue='csvconversion')

        channel_csv.basic_publish(exchange='',
                              routing_key='csvconversion',
                              body=rows)
        stop_connection(connection)
        return 'Successful'


if __name__ == '__main__':
    app.run(port='5002')