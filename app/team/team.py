from . import main
from .team_data import team_data
from flask import render_template, abort


@main.route('/team')
def team():
    return render_template('team.html',team=team_data.values())

@main.route('/team/<int:member_id>')
def team_detail(member_id):
    member = team_data.get(member_id)
    if not member:
        abort(404)
    return render_template("team_detail.html", member=member)
