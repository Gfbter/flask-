from studentApp import app, db
from studentApp.models import Client
#from sqlalchemy import in_, not_

def parse_filter(table, column, value, filter_op):
    if filter_op == '=':
        print('=')
        return getattr(table, column) == value
    elif filter_op == '<':
        print('<')
        return getattr(table, column) < value
    elif filter_op == '>':
        print('>')
        return getattr(table, column) > value
    elif filter_op == '<=':
        print('<=')
        return getattr(table, column) <= value
    elif filter_op == '>=':
        print('>=')
        return getattr(table, column) >= value
    elif filter_op == '<>':
        print('<>')
        return getattr(table, column) != value
    elif filter_op == 'in':
        print('in')
        return getattr(table, column).in_(str(value).split(';'))
    elif filter_op == 'not in':
        print('not in')
        return ~getattr(table, column).in_(str(value).split(';'))
    elif filter_op == 'like':
        print('like')
        return getattr(table, column).like('%' + str(value) + '%')
    elif filter_op == 'not like':
        print('not like')
        return ~getattr(table, column).like('%' + str(value) + '%')
    elif filter_op == 'not between':
        print('not between')
        return ~getattr(table, column).between(str(value).split(';')[0], str(value).split(';')[1])
    elif filter_op == 'between':
        print('between')
        return getattr(table, column).between(str(value).split(';')[0], str(value).split(';')[1])
        