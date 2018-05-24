from flask import Blueprint, jsonify

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(404)
def page_not_found(e):
    return jsonify(status=404, message=str(e)), 404


@blueprint.app_errorhandler(400)
def bad_request(e):
    return jsonify(status=400, message=str(e)), 400


@blueprint.app_errorhandler(500)
def internal_server_error(e):
    return jsonify(status=500, message=str(e)), 500
