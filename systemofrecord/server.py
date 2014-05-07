from flask import Flask, jsonify, request, render_template
from flask.ext.basicauth import BasicAuth
import itertools
import logging
import os
from .chain import DocumentChain
from .storage import RedisStorage

app = Flask(__name__)

# Auth
if os.environ.get('BASIC_AUTH_USERNAME'):
    app.config['BASIC_AUTH_USERNAME'] = os.environ['BASIC_AUTH_USERNAME']
    app.config['BASIC_AUTH_PASSWORD'] = os.environ['BASIC_AUTH_PASSWORD']
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)


if 'REDISCLOUD_URL' in os.environ:
    storage = RedisStorage(os.environ['REDISCLOUD_URL'])
else:
    storage = RedisStorage(os.environ['SYSTEMOFRECORDREDIS_1_PORT_6379_TCP'].replace('tcp://', 'redis://'))

if 'WEBHOOKS' in os.environ:
    webhooks = os.environ['WEBHOOKS'].split(',')
else:
    webhooks = []

# Automatically connect to titles and geo services in development
if 'TITLES_1_PORT_8004_TCP' in os.environ:
    webhooks.append(os.environ['TITLES_1_PORT_8004_TCP'].replace('tcp://', 'http://') + '/titles-revisions')
if 'GEO_1_PORT_8005_TCP' in os.environ:
    webhooks.append(os.environ['GEO_1_PORT_8005_TCP'].replace('tcp://', 'http://') + '/titles-revisions')

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

@app.route('/invalid-entries', methods=['GET'])
def invalid_entries_list():
    limit = int(request.args.get('limit', 100))
    entries = itertools.islice(chain.invalid_entries(), limit)
    return jsonify({
        'entries': [e.serialize() for e in entries]
    })

@app.route('/entries/<entry_id>', methods=['GET'])
def entry_detail(entry_id):
    return jsonify(chain.get(entry_id).serialize())

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
