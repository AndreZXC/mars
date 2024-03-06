#http://127.0.0.1:5000/api/jobs


import flask
from . import db_session
from .jobs import Jobs


blueprint = flask.Blueprint('jobs_api',
                            __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify({
        'jobs': [item.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'start_date',
                                    'is_finished')) for item in jobs]
    })


@blueprint.route('/api/jobs/<int:jobid>', methods=['GET'])
def get_one_job(jobid):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobid)
    if job:
        return flask.jsonify({
            'job': job.to_dict(only=('job', 'team_leader', 'work_size', 'start_date', 'is_finished'))
        })
    else:
        return flask.make_response(flask.jsonify({'err': 'Not found'}), 404)


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'empty request'}), 400)
    if not all(key in flask.request.json for key in ['job', 'team_leader', 'work_size', 'start_date', 'is_finished',
                                                     'collaborators']):
        return flask.make_response(flask.jsonify({'error': 'bad request'}), 400)
    db_sess = db_session.create_session()
    job = Jobs(
        job=flask.request.json['job'],
        team_leader = flask.request.json['team_leader'],
        work_size=flask.request.json['work_size'],
        is_finished=flask.request.json['is_finished'],
        collaborators=flask.request.json['collaborators']
    )
    job.dates(flask.request.json['start_date'])
    db_sess.add(job)
    db_sess.commit()
    return flask.jsonify({'ret': 'Успех'})