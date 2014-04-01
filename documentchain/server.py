from flask import Flask, jsonify, request
from .chain import DocumentChain
from .storage import DiskStorage

app = Flask(__name__)
chain = DocumentChain(DiskStorage('data/'))

@app.route('/entries', methods=['GET', 'POST'])
def entries():
    if request.method == 'POST':
        if not request.json:
            return '', 400
        id = chain.add(request.json)
        res = jsonify({"id": id})
        res.status_code = 201
        return res
    else:
        return jsonify({'entries': [e.serialize() for e in chain.all()]})
