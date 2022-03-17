from ast import GtE
from crypt import methods
from pickle import GET
from flask_script import Manager, Server

manager = Manager(app)
manager.add_command('server',Server)

@app.route('/user/<user_id>/', methods=['GET'])
def get_one_user():
        return ''


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method ='sha256')
    new_user 
    return ''

@app.route('/user/<user_id>/', methods=['DELETE'])
def delete_user():
        return ''

if __name__ == '__main__':
    manager.run()