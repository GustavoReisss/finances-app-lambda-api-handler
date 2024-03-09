from flask import Flask, request
from lambda_function import lambda_handler


app = Flask(__name__)


def make_api_gateway_event():
    event = {
        "httpMethod": request.method,
        "path": request.path,
        "body": "",
        "headers": dict(request.headers),
        "queryStringParameters": request.args.to_dict(),
    }

    event["multiValueQueryStringParameters"] = {
        key: value.split(",")
        for key, value in event["queryStringParameters"].items()
    }

    try:
        event["body"] = request.get_json()
    except:
        pass

    return event


@app.route("/<string:endpoint>", methods=['GET', 'POST'])
@app.route("/<string:endpoint>/<string:pk>", methods=['GET', 'PUT', 'DELETE'])
@app.route("/<string:endpoint>/<string:pk>/<string:sk>", methods=['GET', 'PUT', 'DELETE'])
def handle_request(*args, **kwargs):
    response = lambda_handler(make_api_gateway_event())
    status_code = response.pop("statusCode", 200)
    return response, status_code
    

if __name__ == "__main__":
    app.run(debug=True)
