from flask import jsonify
from flask_restful import Api, abort, reqparse, Resource
import datetime as dt
from . import db_session
from .jobs import Jobs


def abort_if_jobs_NotFound(jobid):
    sess = db_session.create_session()
    job = sess.query(Jobs).get(jobid)
    if not job:
        abort(404, message=f'Job with id={jobid} not found')


parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('start_date', required=True)
parser.add_argument('collaborators', required=True)
parser.add_argument('is_finished', required=True, type=bool)


class JobResourse(Resource):
    def get(self, jobid):
        abort_if_jobs_NotFound(jobid)
        sess = db_session.create_session()
        job = sess.query(Jobs).get(jobid)
        return jsonify({'job': job.to_dict(only=('id', 'job', 'team_leader', 'work_size',
                                                 'start_date', 'is_finished', 'collaborators'))})

    def delete(self, jobid):
        abort_if_jobs_NotFound(jobid)
        sess = db_session.create_session()
        job = sess.query(Jobs).get(jobid)
        sess.delete(job)
        sess.commit()
        return jsonify({'success': 'OK'})


class JobListResourse(Resource):
    def get(self):
        sess = db_session.create_session()
        jobs = sess.query(Jobs).all()
        return jsonify({'jobs': [job.to_dict(only=('id', 'job', 'team_leader', 'work_size',
                                                   'start_date', 'is_finished', 'collaborators'))
                                 for job in jobs]})

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        job = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        job.dates(args['start_date'])
        sess.add(job)
        sess.commit()
        return jsonify({'success': 'OK'})