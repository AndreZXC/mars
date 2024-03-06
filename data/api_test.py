import requests
import pprint
import datetime as dt


pprint.pprint(requests.get('http://127.0.0.1:5000/api/jobs').json())
pprint.pprint(requests.get('http://127.0.0.1:5000/api/job/1').json())
pprint.pprint(requests.get('http://127.0.0.1:5000/api/job/111').json())
pprint.pprint(requests.post('http://127.0.0.1:5000/api/jobs', json={'job': 'Перезагрузка',
                                                                    'team_leader': 3,
                                                                    'work_size': 3,
                                                                    'start_date': dt.datetime.now().strftime(''),
                                                                    'is_finished': False,
                                                                    'collaborators': '2, 3'
                                                                    }).json())