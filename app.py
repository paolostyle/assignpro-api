import error_handlers
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from ap_flow import CalcType, make_response, FlowNetwork
from ap_flow.solvers import simple, sum, bottleneck

app = Flask(__name__)
app.register_blueprint(error_handlers.blueprint)


@app.route('/solve', methods=['POST'])
def solve_assignment():
    if not request.json:
        abort(400)

    data = request.get_json()
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

    return jsonify(response), response['status']


if __name__ == '__main__':
    CORS(app, origins=['http://localhost:8080'], methods=['POST', 'OPTIONS'])
    app.run()
