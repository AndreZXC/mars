import requests
import pytest
from main import main


main()


def test_getall():
    assert requests.get('http://127.0.0.1:5000/api/jobs').json()


def test_jobone():
    assert (requests.get('http://127.0.0.1:5000/api/jobs/1').json() ==
            {'job': {'collaborators': '3',
                     'id': 1,
                     'is_finished': True,
                     'job': 'Починка компьютера',
                     'start_date': '2024-02-27 20:48:16',
                     'team_leader': 1,
                     'work_size': 10}})


def test_wrongid():
    assert requests.get('http://127.0.0.1:5000/api/jobs/100').json() == {'err': 'Not found'}


def test_wrongtype():
    with pytest.JSONDecodeError:
        requests.get('http://127.0.0.1:5000/api/jobs/abhvdza').json()