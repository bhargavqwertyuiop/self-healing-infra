#!/usr/bin/env python3
from flask import Flask, request
import subprocess
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['POST'])
def handle_alert():
    data = request.get_json()
    alerts = data.get('alerts', [])
    for alert in alerts:
        status = alert.get('status')
        name   = alert['labels'].get('alertname')
        logging.info(f"Received alert {name} status={status}")
        # only act on firing alerts
        if status == 'firing':
            # run Ansible playbook
            subprocess.Popen(['ansible-playbook', '-i', '../ansible/hosts', '../ansible/restart-nginx.yml'])
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
