from flask import jsonify

from init_app import init_base_app

from handler_groups.weather import bp_weather

app = init_base_app(__name__)

app.register_blueprint(bp_weather)

@app.errorhandler(Exception)
def handle_error(e):
    from werkzeug.exceptions import HTTPException
    if isinstance(e, HTTPException):
        return jsonify({
            'status': 'error',
            'message': e.description,
        }), e.code

    return jsonify({
        'status': 'error',
        'message': 'Unknown error',
    }), 500

if __name__ == '__main__':
    app.run()
