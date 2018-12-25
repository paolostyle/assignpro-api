import error_handlers
from flask import Flask, request, jsonify, abort, send_file, redirect
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from ap_flow import CalcType, make_response, FlowNetwork, get_request_validator
from ap_flow.solvers import simple, sum, bottleneck

app = Flask(__name__)

SWAGGER_URL = '/api/docs'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    '/api/swagger.json'
)

app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(error_handlers.blueprint)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
CORS(app, methods=['POST', 'OPTIONS'])


@app.route('/')
def redirect_to_docs():
    return redirect('/api/docs', code=302)


@app.route('/api/swagger.json')
def swagger_json():
    return send_file('swagger.json')


@app.route('/api/solve', methods=['POST'])
def solve_assignment():
    if not request.json:
        abort(400)

    data = request.get_json()
    rv = get_request_validator()
    validation_result = rv.validate(data)

    if validation_result:
        fn = FlowNetwork(data['workers'], data['tasks'], data['costs'])

        if data['type'] == CalcType.SUM:
            response = sum.solve(fn)
        elif data['type'] == CalcType.SUM_MAX:
            response = sum.solve(fn, True)
        elif data['type'] == CalcType.BOTTLENECK:
            response = bottleneck.solve(fn)
        elif data['type'] == CalcType.SIMPLE:
            response = simple.solve(fn)
        else:
            response = make_response({}, 501)
    else:
        response = make_response({}, 400, validation_result.errors)

    return jsonify(response), response['status']


if __name__ == '__main__':
    app.run()
