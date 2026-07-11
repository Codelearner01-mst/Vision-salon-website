
from . import main
from flask import render_template, abort
from ..models.team_model import TeamModel


@main.route('/team')
def team():
    try:
        team_members = TeamModel.query.all()
        if not team_members:
            abort(404)
        team_members = [team.json() for team in team_members]
        return render_template('team.html',team=team_members)
    except Exception as e:
        abort(500)

@main.route('/team/<int:member_id>')
def team_detail(member_id):
    member = TeamModel.query.get(member_id)
    if not member:
        abort(404)
    member = member.json()
    return render_template("team_detail.html", member=member)
