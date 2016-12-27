from flask import Flask, jsonify, request
from flask_cors import CORS

from nlp.luNlp import analyze_wod, recreate
from nlp.trackable import Builder

application = Flask(__name__)
CORS(application)

 ## Bootstrapping the pickles
 recreate()

@application.route("/", methods=['GET'])
def get():
    return jsonify(status='ok')

@application.route("/", methods=['post'])
def post():
    wod = request.get_json()
    if not wod:
      return jsonify(error='No wod sent'), 400
    result = analyze_wod(wod)
    b = Builder.build(result)
    result = {
      'input': wod,
      'output': b.todict(),
    }
    return jsonify(**result)

if __name__ == '__main__':
     application.run(host= '0.0.0.0', debug=True)