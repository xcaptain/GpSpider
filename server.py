from flask import Flask, request, send_file
from lib import scrap_by_keyword
from datetime import date

server = Flask(__name__)


@server.route("/")
def hello():
    print(request.args)
    keyword = request.args.get('keyword')
    excel_file_path = scrap_by_keyword(keyword, date.today())
    return send_file(excel_file_path, as_attachment=True)


if __name__ == "__main__":
    server.run(host='0.0.0.0')
