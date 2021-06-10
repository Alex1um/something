from flask import *
from flask_wtf import CSRFProtect
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime
from data.forms.reg import RegisterForm
from data.forms.log import *
from flask_login import current_user, login_user, LoginManager, logout_user, login_required
from data.forms.job import *
from data.forms.depart import *
from data.departs import Depart
from api import jobs_api, user_api
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = 'too secret?'
login_manager = LoginManager()
login_manager.init_app(app)

onepath = "./static/css/style.css"
secondpath = "../static/css/style.css"

# --job--


@app.route("/addjob", methods=["GET", "POST"])
@login_required
def addjob():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.job.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        jobs.work_size = form.work_size.data
        jobs.creator = current_user.id
        session.add(jobs)
        session.commit()
        return redirect('/')
    if form.errors:
        for k, v in form.errors.items():
            flash(f"Error with input {k}: {v[0]}")
    return render_template("standart.html",
                           form=form,
                           base_title="Add Job",
                           st_title="Adding Job",
                           current_user=current_user,
                           stpath=onepath)


@app.route("/deletejob/<int:job_id>")
def deletejob(job_id):
    session = db_session.create_session()
    session.query(Jobs).get(job_id).delete()
    for job in session.query(Jobs).filter(Jobs.id > job_id):
        job.id -= 1
    session.commit()
    return redirect("/")


@app.route("/editjob/<int:job_id>", methods=["GET", "POST"])
def editjob(job_id):
    form = JobForm()
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()
    if current_user.id in (job.creator, 1):
        if form.validate_on_submit():
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            job.work_size = form.work_size.data
            session.commit()
            return redirect('/')
        form.team_leader.data = job.team_leader
        form.job.data = job.job
        form.collaborators.data = job.collaborators
        form.work_size.data = job.work_size
        form.is_finished.data = job.is_finished
        if form.errors:
            for k, v in form.errors.items():
                flash(f"Error with input {k}: {v[0]}")
        return render_template("standart.html",
                               form=form,
                               base_title="Edit Job",
                               st_title="Editing Job",
                               current_user=current_user,
                               stpath=secondpath)
    else:
        flash("U does not have permissions")

    if form.errors:
        for k, v in form.errors.items():
            flash(f"Error with input {k}: {v[0]}")
    return redirect("/")


# --job--
# --departments--


@app.route("/departments")
def departments():
    session = db_session.create_session()

    def format_for_table(d: dict):
        dn = dict()
        dn["Title of department"] = d['title']
        leader = session.query(User).filter(User.id == d['chief']).first()
        dn["Chief"] = f"{leader.surname} {leader.name}"
        dn["Members"] = d['members']
        dn["Department Email"] = d["email"]
        return [tuple(dn.keys()), tuple(dn.values()), d['creator']]

    formated = tuple(format_for_table(i.__dict__) for i in session.query(Depart))
    return render_template("deps.html",
                           jobs=formated,
                           current_user=current_user,
                           stpath=onepath,
                           base_title="List of Departments")


@app.route("/adddepartment", methods=["GET", "POST"])
@login_required
def adddepart():
    form = DepartForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        depart = Depart()
        depart.title = form.title.data
        depart.chief = form.chief.data
        depart.members = form.members.data
        depart.email = form.email.data
        depart.creator = current_user.id
        session.add(depart)
        session.commit()
        return redirect('/departments')
    if form.errors:
        for k, v in form.errors.items():
            flash(f"Error with input {k}: {v[0]}")
    return render_template("standart.html",
                           form=form,
                           base_title="Add Department",
                           st_title="Adding Department",
                           current_user=current_user,
                           stpath=onepath)


@app.route("/deletedepartment/<int:dep_id>")
def deletedepart(dep_id):
    session = db_session.create_session()
    session.query(Depart).filter(Depart.id == dep_id).delete()
    for depart in session.query(Depart).filter(Depart.id > dep_id):
        depart.id -= 1
    session.commit()
    return redirect("/departments")


@app.route("/editdepartment/<int:dep_id>", methods=["GET", "POST"])
def editdepart(dep_id):
    form = DepartForm()
    session = db_session.create_session()
    depart = session.query(Depart).filter(Depart.id == dep_id).first()
    if current_user.id in (depart.creator, 1):
        if form.validate_on_submit():
            depart.title = form.title.data
            depart.chief = form.chief.data
            depart.members = form.members.data
            depart.email = form.email.data
            depart.creator = current_user.id
            session.commit()
            return redirect('/departments')
        form.title.data = depart.title
        form.chief.data = depart.chief
        form.members.data = depart.members
        form.email.data = depart.email
        if form.errors:
            for k, v in form.errors.items():
                flash(f"Error with input {k}: {v[0]}")
        return render_template("standart.html",
                               form=form,
                               base_title="Edit Department",
                               st_title="Editing Department",
                               current_user=current_user,
                               stpath=secondpath)
    else:
        flash("U does not have permissions")

    if form.errors:
        for k, v in form.errors.items():
            flash(f"Error with input {k}: {v[0]}")
    return redirect("/departments")


# --departments--
# --user sets--


@app.route('/register', methods=["GET", 'POST'])
def register():
    session = db_session.create_session()
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if session.query(User).filter(User.email == form.login.data).first():
            flash("Error with input Login: Invalid login")
        else:
            user = User()
            user.address = form.address.data
            user.position = form.position.data
            user.speciality = form.speciality.data
            user.surname = form.surname.data
            user.name = form.name.data
            user.email = form.login.data
            user.city_from = form.city_from.data
            user.age = int(form.age.data)
            user.modified_date = datetime.datetime.now()
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return redirect("/login")
    if form.errors:
        for k, v in form.errors.items():
            flash(f"Error with input {k}: {v[0]}")
    return render_template("standart.html",
                           base_title="Регистрация",
                           st_title="Register",
                           form=form,
                           current_user=current_user,
                           stpath=onepath)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.login.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                print('login', user)
                return redirect('/')
            else:
                flash("invalid password")
        else:
            flash("Login is invalid")
    if form.errors:
        for k, v in form.errors.items():
            flash(f"Error with input {k}: {v[0]}")
    return render_template("standart.html",
                           base_title="Логин",
                           st_title="Login",
                           current_user=current_user,
                           form=form,
                           stpath=onepath)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/users_show/<int:user_id>")
def get_photo(user_id):
    # session = db_session.create_session()
    user = requests.get(f"http://localhost:5000/api/users/{user_id}").json()
    if not user:
        return jsonify(error="Invalid Id")
    import os
    if f"{user_id}.png" not in os.listdir("./static/images"):
        from io import BytesIO
        from PIL import Image
        toponym_to_find = user["city_from"]
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            return jsonify(error="Place not found")
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        bound = toponym['boundedBy']["Envelope"]
        lc, uc = tuple(map(float, bound['lowerCorner'].split())), tuple(map(float, bound['upperCorner'].split()))
        dx, dy = abs(lc[0] - uc[0]), abs(lc[1] - uc[1])
        mdx = min(dx, dy)
        dx, dy = mdx / 10, mdx / 10
        dx, dy = str(dx), str(dy)
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        # delta = "2.5"
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([dx, dy]),
            "l": "sat",
            # "z": "4.67"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        img = Image.open(BytesIO(response.content))
        # img.show()
        img.save(f"./static/images/{user_id}.png")
    return render_template("home.html",
                           user=user,
                           base_title="Hometown",
                           current_user=current_user,
                           stpath=secondpath)

# --user sets--


@app.route("/")
def mains():
    session = db_session.create_session()

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
    formated = tuple(format_for_table(i.__dict__, i.categories) for i in session.query(Jobs))
    return render_template("main.html",
                           jobs=formated,
                           current_user=current_user,
                           stpath=onepath,
                           base_title="Main page")


def main():
    db_session.global_init("db\\default.sqlite")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    CSRFProtect().init_app(app)
    app.run()


if __name__ == "__main__":
    main()