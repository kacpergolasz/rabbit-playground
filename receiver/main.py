#!/usr/bin/env python
import logging

import pika, sys, os

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

root.addHandler(handler)


def main():
    log = logging.getLogger("asd")
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="host.docker.internal", port=5672))
        channel = connection.channel()
        channel.queue_declare(queue='hello')

        def callback(ch, method, properties, body):
            log.info(f" [x] Received {body}")

        channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

        log.info(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except Exception as e:
        log.exception(e)


print("HELLLLOOOOOO")
# if __name__ == '__main__':
try:
    main()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
