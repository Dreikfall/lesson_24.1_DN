import re


from werkzeug.exceptions import BadRequest
from typing import Iterable

from exceptions import FilterMapColErrors, SortError, CmdError, UniqueErrors


def iterator(file: str) -> Iterable:
    """Итератор всего лога"""

    with open(file, 'r', encoding='utf-8') as f:
        return (i for i in f.readlines())


def filter_query(iter_obj: Iterable, value: str) -> Iterable:
    """Фильтрация по вхождению слова"""

    iter_obj = filter(lambda x: value in x, iter_obj)
    return iter_obj


def filter_map(iter_obj: Iterable, col: str) -> Iterable:
    """Фильтрация по столбцам"""

    if col == '1':
        iter_obj = map(lambda x: f'{x.split()[0]}\n', iter_obj)
        return iter_obj
    elif col == '2':
        iter_obj = map(lambda x: f"{x[x.find('['):x.find(']')+1]}\n", iter_obj)
        return iter_obj
    elif col == '3':
        iter_obj = map(lambda x: f'''{x[x.find('"'):]}\n''', iter_obj)
        return iter_obj
    raise FilterMapColErrors('Необходимо ввести value в диапазоне 1-3')


def filter_unique(iter_obj: Iterable, value: str) -> Iterable:
    """Только уникальные значения"""

    if value != '""':
        raise UniqueErrors('Значение value должно быть ""')
    uniq_set = iter(set(iter_obj))
    return uniq_set


def filter_sort(iter_obj: Iterable, asc_desc: str | bool) -> Iterable:
    """Фильтрация по алфавиту в обе стороны"""
    if asc_desc not in ['asc', 'desc']:
        raise SortError('Необходимо установить значение value "asc" или "desc"')
    asc_desc = True if asc_desc == 'desc' else False
    iter_obj = sorted(iter_obj, reverse=asc_desc)
    return iter_obj


def filter_limit(iter_obj: Iterable, limit: int) -> Iterable:
    """Лимит записей"""
    lst = list(iter_obj)
    buff = (lst[i] for i in range(limit))
    return buff


def filter_regex(iter_obj: Iterable, query: str) -> Iterable:
    """Для POST запроса строк 'images.png' с учетом экранирования  '.*images/\\w+\\.png.*'"""
    result = (f'{x}\n' for i in iter_obj for x in (re.findall(fr'{query}', i)))
    return result


def do_query(cmd: str, value: str, iter_obj: Iterable) -> Iterable:
    """Функция набора фильтров"""
    if cmd == 'filter':
        iter_obj = filter_query(iter_obj, value)
    elif cmd == 'map':
        iter_obj = filter_map(iter_obj, value)
    elif cmd == 'unique':
        iter_obj = filter_unique(iter_obj, value)
    elif cmd == 'sort':
        iter_obj = filter_sort(iter_obj, value)
    elif cmd == 'limit':
        iter_obj = filter_limit(iter_obj, int(value))
    elif cmd == 'regex':
        iter_obj = filter_regex(iter_obj, value)
    else:
        raise BadRequest
    return iter_obj


def do_cmd(params: dict, path: str) -> Iterable:
    """Функция определяющая количество аргументов"""
    result = iterator(path)
    if 'cmd1' in params and 'value1' in params:
        result = do_query(params['cmd1'], params['value1'], result)
    if 'cmd2' in params and 'value2' in params:
        result = do_query(params['cmd2'], params['value2'], result)
    if not result:
        raise CmdError
    return result

