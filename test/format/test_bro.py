# -*- coding: utf-8 -*-
from csirtg_indicator.format.bro import get_lines
import pytest
from csirtg_indicator import Indicator
from faker import Faker
fake = Faker()

@pytest.fixture
def indicator():
    i = {
            'indicator': "example.com",
            'itype': 'fqdn',
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reported_at': '2015-01-01T00:00:00Z'
        }
    return Indicator(**i)


@pytest.fixture
def indicator_unicode(indicator):
    indicator.indicator = 'http://xz.job391.com/down/ï¿½ï¿½ï¿½ï¿½à¿ªï¿½ï¿½@89_1_60'
    return indicator


def test_format_bro(indicator, indicator_unicode):
    data = [indicator, indicator_unicode]

    n = list(get_lines(data))
    assert len(n) > 0

    n = indicator.to_bro()
    assert "xz.job391.com" in n


def test_format_bro_random(indicator):
    for d in range(0, 100):
        for i in [fake.ipv4, fake.ipv6, fake.uri, fake.domain_name]:
            indicator.indicator = i()
            assert Indicator.indicator

            assert len(list(get_lines([indicator]))) > 0


if __name__ == '__main__':
    test_format_bro()
