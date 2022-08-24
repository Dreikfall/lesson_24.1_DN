import os
from utils import do_cmd
from flask import Flask, request
from exceptions import FilterMapColErrors, SortError, CmdError, UniqueErrors

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=['POST'])
def perform_query():
    req_arg = request.json
    try:
        path = os.path.join(DATA_DIR, req_arg.get('file_name'))
        data_iter = do_cmd(req_arg, path)
    except FileNotFoundError:
        return 'Данного файла не существует'
    except FilterMapColErrors:
        return 'Необходимо ввести value в диапазоне 1-3'
    except SortError:
        return 'Необходимо установить значение value "asc" или "desc"'
    except ValueError:
        return 'Необходимо числовое значение value'
    except CmdError:
        return 'Неверно заданы пары cmd/value или они отсутствуют'
    except UniqueErrors:
        return 'Значение value должно быть ""'
    return app.response_class(data_iter, content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=True)
