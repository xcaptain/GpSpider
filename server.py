from flask import Flask, request, send_file
from lib import scrap_by_keyword

server = Flask(__name__)


@server.route("/")
def hello():
    print(request.args)
    keyword = request.args.get('keyword')
    excel_file_path = scrap_by_keyword(keyword)
    return send_file(excel_file_path, as_attachment=True)


if __name__ == "__main__":
    server.run(host='0.0.0.0')
