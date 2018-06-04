import datetime


def make_response(response, status, v_errors=None):
    response['status'] = status

    if status == 200:
        msg = 'Obliczenia zakończone sukcesem!'
    elif status == 400 and v_errors == None:
        msg = 'Przydział dla wprowadzonych danych nie jest możliwy.'
    elif status == 400 and v_errors != None:
        msg = (
            'Wystąpiły błędy walidacji. Jeżeli nie używasz aplikacji w '
            'nieprzewidziany sposób, to nie powinno się to wydarzyć.'
        )
    elif status == 416:
        msg = (
            'Niektóre wartości kosztów są zbyt wysokie i mogą '
            'spowodować przekroczenie zakresu liczb całkowitych.'
        )
    elif status == 500:
        msg = 'Wystąpił wewnętrzny błąd serwera.'
    elif status == 501:
        msg = 'Nie znaleziono określonego typu obliczeń.'

    response['message'] = msg
    response['calculationDate'] = datetime.datetime.now().isoformat()
    return response
