from . import main
from flask import render_template
from ..models import TeamModel


@main.route('/story')
def story():
    team_data = TeamModel.query.all()
    try:
        team = [t.json() for t in team_data] if team_data else []
    except Exception as e:
        print("Failed to fetch team data for story page:", e)
        team = []
    return render_template('story.html', team=team)
