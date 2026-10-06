from flask import Blueprint, g, redirect, render_template, url_for, flash, request
from app.security.decorators import check_role
from app.models.enums import UserRole
from app.models.assignment import Assignment
from app.models.user import User
from app.algorithms.study_scheduler import build_study_schedule
from app.models.student_settings import StudentSettings
import calendar
from datetime import date

bp = Blueprint('student', __name__, url_prefix='/student')
bp.before_request(check_role(UserRole.STUDENT.value))

@bp.route('/')
def redirect_to_dashboard():
    return redirect(url_for('student.dashboard'))

@bp.route('/dashboard')
def dashboard():
    classrooms = [(c, User.get_by_id(c.teacher_id)) for c in g.user.get_classrooms()]
    assignments = Assignment.get_for_student(g.user.id)
    return render_template('student/dashboard.html', classrooms=classrooms, assignments=assignments)


@bp.route('/schedule')
def schedule():
    try:
        today = date.today()
        year  = request.args.get('year',  today.year,  type=int)
        month = request.args.get('month', today.month, type=int)

        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        shown_date = date(year, month, 1)
        study_schedule = build_study_schedule(g.user)
        weeks = calendar.Calendar(firstweekday=0).monthdatescalendar(year, month)
        assignments = {a.id: a for a in Assignment.get_for_student(g.user.id)}
    except Exception as e:
        flash(str(e))
        return render_template('student/schedule.html', study_schedule={}, weeks=[], assignments={}, today=today, month=month, day_abbr=list(calendar.day_abbr), prev_month=prev_month, prev_year=prev_year, next_month=next_month, next_year=next_year, year=year, shown_date=today)

    return render_template('student/schedule.html', study_schedule=study_schedule, weeks=weeks, assignments=assignments, today=today, month=month, day_abbr=list(calendar.day_abbr), prev_month=prev_month, prev_year=prev_year, next_month=next_month, next_year=next_year, year=year, shown_date=shown_date)

@bp.route('/settings', methods=('GET', 'POST'))
def settings():
    days = ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
    student_settings = StudentSettings.get_by_student_id(g.user.id)

    form = {'procrastination_factor': student_settings.procrastination_factor, 'exclude_overdue': student_settings.exclude_overdue}
    for day in days:
        form['hours_free_' + day] = getattr(student_settings, 'hours_free_' + day)

    if request.method == 'POST':
        form = {key: request.form.get(key, False) for key in form}
        form['exclude_overdue'] = 'exclude_overdue' in request.form

        try:
            student_settings.update_settings(float(form['procrastination_factor']), bool(form['exclude_overdue']), *[float(form['hours_free_' + day]) for day in days])
            flash('Settings updated successfully.')
            return redirect(url_for('student.settings'))
        except ValueError as ve:
            flash(str(ve))
        except Exception as e:
            flash('An unexpected error occurred while saving settings: ' + str(e))

    return render_template('student/settings.html', form=form)