from flask import Flask, jsonify, request
import os
from .chain import DocumentChain
from .storage import RedisStorage

app = Flask(__name__)

if 'REDISCLOUD_URL' in os.environ:
    storage = RedisStorage(os.environ['REDISCLOUD_URL'])
else:
    storage = RedisStorage('redis://%s:%s' % (
        os.environ.get('REDIS_1_PORT_6379_TCP_ADDR'),
        os.environ.get('REDIS_1_PORT_6379_TCP_PORT')
    ))
chain = DocumentChain(storage)

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
