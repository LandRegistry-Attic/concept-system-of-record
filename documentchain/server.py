from flask import Flask, jsonify, request
import logging
import os
from .chain import DocumentChain
from .storage import RedisStorage

app = Flask(__name__)

if 'REDISCLOUD_URL' in os.environ:
    storage = RedisStorage(os.environ['REDISCLOUD_URL'])
else:
    storage = RedisStorage(os.environ['SYSTEMOFRECORDREDIS_1_PORT_6379_TCP'].replace('tcp://', 'redis://'))

if 'WEBHOOKS' in os.environ:
    webhooks = os.environ['WEBHOOKS'].split(',')
else:
    webhooks = []

# Automatically connect to titles service in development
if 'TITLES_1_PORT_8004_TCP' in os.environ:
    webhooks.append(os.environ['TITLES_1_PORT_8004_TCP'].replace('tcp://', 'http://') + '/titles-revisions')

chain = DocumentChain(
    storage=storage,
    webhooks=webhooks,
)

@app.before_first_request
def setup_logging():
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

@app.route('/entries', methods=['GET', 'POST'])
def entry_list():
    if request.method == 'POST':
        if not request.json:
            return '', 400
        id = chain.add(request.json)
        res = jsonify({"id": id})
        res.status_code = 201
        return res
    else:
        return jsonify({'entries': [e.serialize() for e in chain.all()]})


@app.route('/entries/<entry_id>', methods=['GET'])
def entry_detail(entry_id):
    return jsonify(chain.get(entry_id).serialize())
