import time
import os
from csirtg_indicator import Indicator

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

OUTPUT_PATH = os.getenv('CSIRTG_INDICATOR_BINDRPZ_PATH', '/etc/bind/rpz')


def get_lines(data, filename=OUTPUT_PATH, **kwargs):
    output = StringIO()
    text = [
        ";;; generated by: {} at {}".
            format('csirtg-indicator', time.strftime('%Y-%m-%dT%H:%M:%S %Z')),
        ';RPZ DATA!',
        '$TTL    1',
        '@       IN      SOA     localhost. root.localhost. (',
        '                     {}         ; Serial'.format(int(time.time())),
        '                         604800         ; Refresh',
        '                          86400         ; Retry',
        '                        2419200         ; Expire',
        '                          86400 )       ; Negative Cache TTL',
        ';',
        '@       IN      NS      localhost.'
    ]

    for t in text:
        output.write(t)
        yield str(output.getvalue())

        if isinstance(output, StringIO):
            output.truncate(0)

    for i in data:
        if isinstance(i, Indicator):
            i = i.__dict__()

        if i['itype'] != 'fqdn':
            continue

        output.write('{}        CNAME .'.format(i['indicator'], filename))
        output.write('*.{}        CNAME .'.format(i['indicator'], filename))
        yield output.getvalue()

        if isinstance(output, StringIO):
            output.truncate(0)
