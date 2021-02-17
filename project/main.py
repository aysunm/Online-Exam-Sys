from flask import Blueprint, render_template, current_app, Flask, stream_with_context, request, Response, flash, redirect, url_for, session
from flask_login import login_required, current_user
from .__init__ import db
from .models import Exam, User, Question, UsersAnswers, UsersExams
import datetime

main = Blueprint('main', __name__)


def stream_template(template_name, **context):
    current_app.update_template_context(context)
    t = current_app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.disable_buffering()
    return rv


@main.route('/')
def index():
    exams = Exam.query.join(User, Exam.owner_id == User.id).add_columns(Exam.id, Exam.name, Exam.start_date,
                                                                        Exam.end_date,
                                                                        User.name.label("uname"))
    is_user_solved = [False for _ in exams]
    if current_user.is_authenticated:
        for idx, ex in enumerate(exams):
            user_solved = UsersExams.query.filter_by(exam_id=ex.id, user_id=current_user.id).first()
            if user_solved:
                is_user_solved[idx] = True

    return Response(stream_with_context(stream_template("index.html", rows=exams, is_user_solved=is_user_solved,
                                                        today_date=datetime.datetime.now())))


@main.route('/profile')
@login_required
def profile():
    users_exams = UsersExams.query.filter_by(user_id=current_user.id)\
        .join(Exam, Exam.id == UsersExams.exam_id) \
        .add_columns(Exam.id.label("examid"), Exam.name,
                     Exam.start_date, Exam.end_date, UsersExams.user_id.label("user_id"))
    return Response(stream_with_context(stream_template('profile.html', res={'name': current_user.name,
                                                                             'exams': users_exams})))


@main.route('/profile/answers/<int:exid>')
@login_required
def show_answers(exid):
    answers = UsersAnswers.query.filter_by(user_id=current_user.id)\
        .join(Question, Question.id == UsersAnswers.question_id) \
        .add_columns(Question.id.label("questionid"), Question.question_text,
                     Question.exam_id, UsersAnswers.answer.label("answer")) \
        .filter_by(exam_id=exid)
    return render_template('show_answers.html', answers=answers)


@main.route('/create')
@login_required
def create():
    user = User.query.filter_by(id=current_user.id).first()
    if user.role == 'Admin':
        return render_template('create_exam.html')
    return Response('<Unauthorized>', 401)


@main.route('/create', methods=['POST'])
@login_required
def create_exam():
    exam_name = request.form.get('examname')
    start_date = request.form.get('startdate')
    end_date = request.form.get('enddate')
    owner_id = current_user.id
    new_exam = Exam(name=exam_name, start_date=start_date, end_date=end_date, owner_id=owner_id)
    db.session.add(new_exam)
    db.session.commit()
    return redirect(url_for('main.add_question', exid=new_exam.id))


@main.route('/question/<int:exid>', methods=['POST', 'GET'])
@login_required
def add_question(exid):
    exam = Exam.query.filter_by(id=exid).first()
    if exam:
        if request.method == 'POST':
            question_text = request.form.get('quetext')
            a = request.form.get('A')
            b = request.form.get('B')
            c = request.form.get('C')
            d = request.form.get('D')
            e = request.form.get('E')
            true_answer = request.form.get('trueans')
            point = request.form.get('point')

            new_question = Question(question_text=question_text, a=a, b=b, c=c, d=d, e=e, exam_id=exid, point=point, true_answer=true_answer)
            db.session.add(new_question)
            db.session.commit()
            flash("Question added!")
            return render_template("add_question.html", res={'ex_name': exam.name, 'exam_id': exid})
        else:
            return render_template("add_question.html", res={'ex_name': exam.name, 'exam_id': exid})
    else:
        flash('No exam found for this id.')
        return redirect(url_for('main.create'))


@main.route('/exam/<int:exid>')
@login_required
def show_exam(exid):
    user_solved = UsersExams.query.filter_by(exam_id=exid, user_id=current_user.id).first()
    if user_solved:
        return redirect(url_for('main.index'))

    exam = Exam.query.filter_by(id=exid).first()
    questions = Question.query.filter_by(exam_id=exid)
    return render_template('show_exam.html', exam=exam, questions=questions)


@main.route('/exam/submit/<int:exid>', methods=['POST'])
@login_required
def submit_answers(exid):
    if request.method == 'POST':
        user_solved = UsersExams.query.filter_by(exam_id=exid, user_id=current_user.id).first()
        if user_solved:
            return redirect(url_for('main.index'))
        questions = Question.query.filter_by(exam_id=exid)
        new_users_exams = UsersExams(user_id=current_user.id, exam_id=exid)
        db.session.add(new_users_exams)
        for q in questions:
            answer = ""
            if f"ans{q.id}" in request.form.keys():
                answer = request.form.get(f"ans{q.id}")
            else:
                pass
            new_users_answers = UsersAnswers(user_id=current_user.id, question_id=q.id, answer=answer)
            db.session.add(new_users_answers)

        db.session.commit()
        flash("Exam successfully sent!")
    return redirect(url_for('main.index'))


