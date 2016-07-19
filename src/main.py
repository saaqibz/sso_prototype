from flask import Flask, render_template, jsonify, request, abort
from database import LlamaBase, Llama

app = Flask(__name__)

# In-Memory 'Database'
db = LlamaBase()

# Llama Viewer App
# Llama Feeder App
# Llama Market App

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


@app.route('/user', methods=['GET'])
def get_user():
    user = get_user_from_cookie(db, request)
    if user is None:
        return abort(404)
    return jsonify(user.serialize())

@app.route('/user/login', methods=['POST'])
def user_login():
    user = db.users.get(request.json['user'])
    if user != None and request.json['pass'] == user.password:
        token = db.create_api_token(user.name)['id']
        response = jsonify(user.serialize())
        response.set_cookie('api_token', token, 10*60)  # Lasts 10 minutes
    else:
        response = abort(403)

    return response


def get_user_from_cookie(db, request):
    username = db.api_tokens[request.cookies['api_token']]['user']
    if username is not None:
        return db.users[username]

    return None


@app.route('/llama', methods=['GET'])
def get_llamas():
    user = get_user_from_cookie(db, request)
    if user is None:
        return abort(403)

    llamas = [llama.serialize() for llama in db.llamas.values() if llama.owner == user.name]
    return jsonify({'llamas': llamas})


@app.route('/llama', methods=['POST'])
def post_llamas():
    user = get_user_from_cookie(db, request)
    if user is None:
        return abort(403)

    llama = Llama(user.name)
    db.llamas[llama.id] = llama
    return jsonify({'added': llama.serialize()})


@app.route('/llama/<int:llama_id>', methods=['DELETE'])
def delete_llamas(llama_id):
    user = get_user_from_cookie(db, request)
    if user is None:
        return abort(403)

    if db.llamas.get(llama_id) == None:
        return abort(404)
    elif db.llamas[llama_id].owner != user.name:
        return abort(403)

    return jsonify({'deleted': 'llama {}'.format(llama_id)})


@app.route('/cash', methods=['GET'])
def get_cash():
    user = get_user_from_cookie(db, request)
    if user is None:
        return abort(403)

    return jsonify({'cash': '${}'.format(user.cash)})


@app.route('/cash/<int:amt>', methods=['PUT'])
def put_cash(amt):
    user = get_user_from_cookie(db, request)
    if user is None:
        return abort(403)

    user.cash = amt
    return jsonify({'updated': 'cash = ${}'.format(amt)})


@app.route('/inventory', methods=['GET'])
def get_inventory():
    pass


@app.route('/inventory', methods=['DELETE'])
def delete_inventory():
    pass


@app.route('/inventory', methods=['POST'])
def add_to_inventory():
    pass


if __name__ == '__main__':
    app.run(debug=True)
