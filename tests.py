import pytest
import server
from freezegun import freeze_time


@pytest.mark.parametrize('mes,exp', [
    ('echo message', 'message'),
    ('calendar', '2007.04.20 13:37'),
    ('stop', 'TCP Server stops...'),
    ('help', f'Available commands: {", ".join(server.allowed)}'),
])
def test_process_message(mes, exp):
    if(mes == 'calendar'):
        with freeze_time(exp):
            out = server.respond(mes)
    else:
        out = server.respond(mes)

    assert out == exp
