from prettytable import PrettyTable
import arrow
from csirtg_indicator import Indicator
from csirtg_indicator.constants import COLUMNS, MAX_FIELD_SIZE, PYVERSION

if PYVERSION > 2:
    basestring = (str, bytes)


def _indicator_row(i, cols, max_field_size):
    if isinstance(i, Indicator):
        i = i.__dict__()

    r = []
    for c in cols:
        y = i.get(c, '')

        if isinstance(y, list):
            if len(y) > 0 and isinstance(y[0], dict):
                y = ''
            else:
                y = ','.join(y)

        if c == 'confidence' and y is None:
            y = 0.0

        if y and (c in ['first_at', 'last_at', 'reported_at']):
            y = arrow.get(y).format('YYYY-MM-DDTHH:mm:ss.SSSSS')
            y = '{}Z'.format(y)
        else:
            if PYVERSION == 2:
                if isinstance(y, basestring):
                    y = unicode(y)
                    y = y.encode('utf-8', 'ignore')
            y = str(y)
        y = (y[:max_field_size] + '..') if len(y) > max_field_size else y

        r.append(y)

    return r


def get_lines(data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
    t = PrettyTable(cols)

    if not isinstance(data, list):
        data = [data]

    for i in data:

        t.add_row(_indicator_row(i, cols, max_field_size))

    yield str(t)
