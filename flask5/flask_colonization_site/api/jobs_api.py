from flask import *
from data import db_session
from data.users import User
from data.jobs import Jobs

blueprint = Blueprint("jobs_api",
                      __name__,
                      template_folder="templates")


@blueprint.route('/api/jobs', methods=["GET", "POSt"])
def get_jobs():
    session = db_session.create_session()
    if request.method == "GET":

        def format_for_table(d: dict, categories: list):
            dn = dict()
            dn["Title of activity"] = d['job']
            leader = session.query(User).filter(User.id == d['team_leader']).first()
            dn["Team leader"] = f"{leader.surname} {leader.name}"
            dn["Duration"] = f"{d['work_size']} hours"
            dn["List of collaborators"] = d["collaborators"]
            dn["Hazard category"] = ', '.join(map(lambda x: str(x.id), categories))
            dn["Is finished"] = "Finished" if d[
                'is_finished'] else "Is not finished"
            return [tuple(dn.keys()), tuple(dn.values()), d['creator']]

        return jsonify([format_for_table(i.__dict__, i.categories) for i in session.query(Jobs)])
    elif request.method == "POST":
        if not request.json:
            return jsonify({'error': 'Empty request'})
        elif not all(key in (rj := request.json) for key in
                     {'team_leader',
                      'job',
                      'collaborators',
                      'is_finished',
                      'work_size',
                      'job_id',
                      'current_user_id'}):
            return jsonify({'error': 'Bad request'})
        elif session.query(Jobs).get(request.json['job_id']):
            return jsonify(error="Id already exists")
        jobs = Jobs()
        jobs.team_leader = request.json['team_leader']
        jobs.job = request.json['job']
        jobs.collaborators = request.json['collaborators']
        jobs.is_finished = request.json['is_finished']
        jobs.work_size = request.json['work_size']
        jobs.id = request.json["job_id"]
        jobs.creator = request.json['current_user_id']
        session.add(jobs)
        session.commit()
        return jsonify(success="OK")
    return jsonify(error="Method is not allowed")


@blueprint.route("/api/jobs/<int:job_id>")
def get_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if job:
        job = job.__dict__
        del job["_sa_instance_state"]
        return jsonify(job)
    else:
        return jsonify(error="Invalid id")


@blueprint.route("/api/jobs/del/<int:job_id>")
def del_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if job:
        job.delete()
        for job in session.query(Jobs).filter(Jobs.id > job_id):
            job.id -= 1
    else:
        return jsonify(error="Id not found")
    session.commit()
    return jsonify(success="OK")


@blueprint.route("/api/jobs/edit/<int:job_id>")
def edit_job(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if jobs:
        jobs.team_leader = request.json['team_leader']
        jobs.job = request.json['job']
        jobs.collaborators = request.json['collaborators']
        jobs.is_finished = request.json['is_finished']
        jobs.work_size = request.json['work_size']
        jobs.id = request.json["job_id"]
        jobs.creator = request.json['current_user_id']
        session.commit()
        return jsonify(success="OK")
    else:
        return jsonify(error="Id not found")
