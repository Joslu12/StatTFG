from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os,json

# Init app
app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)



# Country Class/Model
class Country(db.Model):
    country_id=db.Column(db.Integer,primary_key=True,nullable=False)
    country_name=db.Column(db.String(45),nullable=False)

    #Relantionships     
   # stadiums = db.relationship("Stadium")
    #referees = db.relationship("Referee")
    #managers = db.relationship("Manager")
    #players = db.relationship("Player")
    #competitions = db.relationship("Competition")
    #teams = db.relationship("Team")


    def __init__(self,country_id,country_name):
        self.country.id=country_id
        self.country_name=country_name

# Country Schema
class CountrySchema(ma.Schema):
    class Meta:
        fields=('country_id','country_name')

# Position Class/Model
class Position(db.Model):
    position_id=db.Column(db.Integer,primary_key=True,nullable=False)
    position_name=db.Column(db.String(3),nullable=False)

    #Relantionships     
    #lineup = db.relationship('Lineup')

    def __init__(self,position_id,position_name):
        self.position.id=position_id
        self.position_name=position_name

# Position Schema
class PositionSchema(ma.Schema):
    class Meta:
        fields=('position_id','position_name')


# Match Class/Model
class Match(db.Model):
    match_id = db.Column(db.Integer,primary_key=True,nullable=False)
    match_season_id= db.Column(db.Integer,primary_key=True,nullable=False)
    match_competition_id = db.Column(db.Integer,db.ForeignKey('Competition.competition_id'),nullable=False)
    match_date = db.Column(db.DateTime,nullable=False)
    match_kick_off= db.Column(db.DateTime,nullable=False)
    match_stadium_id = db.Column(db.Integer,db.ForeignKey('Stadium.stadium_id'),nullable=False)
    match_referee_id = db.Column(db.Integer,db.ForeignKey('Referee.referee_id'),nullable=False)
    match_home_team_id = db.Column(db.Integer,db.ForeignKey('Team.team_id'),nullable=False)
    match_away_team_id = db.Column(db.Integer,db.ForeignKey('Team.team_id'),nullable=False)
    match_home_score = db.Column(db.Integer,nullable=False)
    match_away_score = db.Column(db.Integer,nullable=False)
    match_competition_stage = db.Column(db.String(45),nullable=False)

    #Relantionships
    #events = db.relationship("Event")
    #lineups = db.relationship("Lineup")

    def __init__(self,match_id,match_season_id,match_competition_id,match_date,match_kick_off,match_stadium_id,match_referee_id,match_home_team_id,match_away_team_id,match_home_score,match_away_score,match_competition_stage):
        self.match_id = match_id
        self.match_season_id= match_season_id
        self.match_competition_id =match_competition_id
        self.match_date = match_date
        self.match_kick_off= match_kick_off
        self.match_stadium_id = match_stadium_id
        self.match_referee_id = match_referee_id
        self.match_home_team_id = match_home_team_id
        self.match_away_team_id = match_away_team_id
        self.match_home_score = match_home_score
        self.match_away_score = match_away_score
        self.match_competition_stage = match_competition_stage

# Match Schema
class MatchSchema(ma.Schema):
    class Meta:
        fields=('match_id' , 'match_season_id' , 'match_competition_id' ,' match_date' , 'match_kick_off' , 'match_stadium_id' , 'match_referee_id' , 'match_home_team_id' , 'match_away_team_id', 'match_home_score', 'match_away_score' , 'match_competition_stage')

# Stadium Class/Model
class Stadium(db.Model):
    stadium_id= db.Column(db.Integer,primary_key=True,nullable=False)
    stadium_name=db.Column(db.String(45),nullable=False)
    stadium_country_id=db.Column(db.Integer,db.ForeignKey('Country.country_id'),nullable=False)

    # Relantionships
    #matchs = db.relationship("Match")

    def __init__(self,stadium_id,stadium_name,stadium_country_id):
        self.stadium_id=stadium_id
        self.stadium_name=stadium_name
        self.stadium_country_id=stadium_country_id

# Stadium Schema
class StadiumSchema(ma.Schema):
    class Meta:
        fields=('stadium_id','stadium_name','stadium_country_id')

# Lineup Class/Model
class Lineup(db.Model):
    lineup_player_id=db.Column(db.Integer,db.ForeignKey('Player.player_id'),primary_key=True,nullable=False)
    lineup_match_id=db.Column(db.Integer,db.ForeignKey('Match.match_id'),primary_key=True,nullable=False)
    lineup_team_id = db.Column(db.Integer,db.ForeignKey('Team.team_id'),nullable=False)
    lineup_played= db.Column(db.Integer,nullable=False)
    lineup_jersey_number= db.Column(db.Integer,nullable=False)
    lineup_position_id =  db.Column(db.Integer,db.ForeignKey('Position.position_id'),nullable=False)
    lineup_sustituion = db.Column(db.Integer)
    lineup_injury = db.Column(db.Integer)

    # Relationship
    #players= db.relationship("Player")

    def __init__(self,lineup_player_id,lineup_match_id,lineup_team_id,lineup_played,lineup_jersey_number,lineup_position_id,lineup_sustituion,lineup_injury):
        self.lineup_player_id=lineup_player_id
        self.lineup_match_id=lineup_match_id
        self.lineup_team_id=lineup_team_id
        self.lineup_played=lineup_played
        self.lineup_jersey_number=lineup_jersey_number
        self.lineup_position_id=lineup_position_id
        self.lineup_sustituion=lineup_sustituion
        self.lineup_injury=lineup_injury

# Lineup Schema
class LineupSchema(ma.Schema):
    class Meta:
        fields=('lineup_player_id','lineup_match_id','lineup_team_id','lineup_played','lineup_jersey_number','lineup_position_id','lineup_sustituion','lineup_injury')

# Competition Class/Model
class Competition(db.Model):
    competition_id=db.Column(db.Integer,primary_key=True,nullable=False)
    competition_season_id=db.Column(db.Integer,primary_key=True,nullable=False)
    competition_name=db.Column(db.String(45),nullable=False)
    competition_gender=db.Column(db.String(45),nullable=False)
    competition_country_id=db.Column(db.Integer,db.ForeignKey('Country.country_id'),nullable=False)
    competition_season_name=db.Column(db.String(45),nullable=False)
    competition_match_update=db.Column(db.DateTime,nullable=False)
    competition_match_available=db.Column(db.DateTime,nullable=False)

    def __init__(self,competition_id,competition_season_id,competition_name,competition_gender,competition_country_id,competition_season_name,competition_match_update,competition_match_available):
        self.competition_id=competition_id
        self.competition_season_id=competition_season_id
        self.competition_name=competition_name
        self.competition_gender=competition_gender
        self.competition_country_id=competition_country_id
        self.competition_season_name=competition_season_name
        self.competition_match_update=competition_match_update
        self.competition_match_available=competition_match_available

#Competition Schema
class CompetitionSchema(ma.Schema):
    class Meta:
        fields=('competition_id','competition_season_id','competition_name','competition_gender','competition_country_id','competition_season_name','competition_match_update','competition_match_available')

# Team Class/Model
class Team(db.Model):
    team_id=db.Column(db.Integer,primary_key=True,nullable=False)
    team_name=db.Column(db.String(45),nullable=False)
    team_gender=db.Column(db.String(45),nullable=False)
    team_manager_id=db.Column(db.Integer,db.ForeignKey('Manager.manager_id'),nullable=False)
    team_group=db.Column(db.String(45))
    team_country_id=db.Column(db.Integer,db.ForeignKey('Country.country_id'),nullable=False)

    #Relantionships
    #events = db.relationship("Event")
    #matchs = db.relationship("Match")
    #lineups = db.relationship("Lineup")

    def __init__(self,team_id,team_name,team_gender,team_manager_id,team_group,team_country_id):
        self.team_id=team_id
        self.team_name=team_name
        self.team_gender=team_gender
        self.team_manager_id=team_manager_id
        self.team_group=team_group
        self.team_country_id=team_country_id

#Team Schema
class TeamSchema(ma.Schema):
    class Meta:
        fields=('team_id','team_gender','team_manager_id','team_group','team_country_id')

#Manager Class/Model
class Manager(db.Model):
    manager_id=db.Column(db.Integer,primary_key=True,nullable=False)
    manager_name=db.Column(db.String(45),nullable=False)
    manager_nickname=db.Column(db.String(45))
    manager_dob=db.Column(db.DateTime,nullable=False)
    manager_country_id=db.Column(db.Integer,db.ForeignKey('Country.country_id'),nullable=False)

    def __init__(self,manager_id,manager_name,manager_nickname,manager_dob,manager_country_id):
        self.manager_id=manager_id
        self.manager_name=manager_name
        self.manager_nickname=manager_nickname
        self.manager_dob=manager_dob
        self.manager_country_id=manager_country_id

# Manager Schema
class ManagerSchema(ma.Schema):
    class Meta:
        fields=('manager_id','manager_name','manager_nickname','manager_dob','manager_country_id')

# ManagerPK Class/Model
class ManagerPK(db.Model):
    manager_id=db.Column(db.Integer,db.ForeignKey('Manager.manager_id'),primary_key=True,nullable=False)
    team_id=db.Column(db.Integer,db.ForeignKey('Team.team_id'),primary_key=True,nullable=False)
    start=db.Column(db.DateTime,nullable=False)
    end=db.Column(db.DateTime)

    #Relationship
    #managers= db.relationship("Manager") 

    def __init__(self,manager_id,team_id,start,end):
        self.manager_id=manager_id
        self.team_id=team_id
        self.start=start
        self.end=end

# ManagerPK Schema
class ManagerPKSchema(ma.Schema):
    class Meta:
        fields=('manager_id','team_id','start','end')

# Referee Class/Model
class Referee(db.Model):
    referee_id=db.Column(db.Integer,primary_key=True,nullable=False)
    referee_name=db.Column(db.String(45),nullable=False)
    referee_country_id=db.Column(db.Integer,db.ForeignKey('Country.country_id'),nullable=False)

    #Relantionships
    #matchs = db.relationship("Match")

    def __init__(self,referee_id,referee_name,referee_country_id):
        self.referee_id=referee_id
        self.referee_name=referee_name
        self.referee_country_id=referee_country_id

# Referee Schema
class RefereeSchema(ma.Schema):
    class Meta:
        fields=('referee_id','referee_name','referee_country_id')

# Player Class/Model
class Player(db.Model):
    player_id=db.Column(db.Integer,primary_key=True,nullable=False)
    player_name=db.Column(db.String(45),nullable=False)
    player_nickname=db.Column(db.String(45))
    player_country_id=db.Column(db.Integer,db.ForeignKey('Country.country_id'),nullable=False)

    #Relantionships
    #events = db.relationship("Event")

    def __init__(self,player_id,player_name,player_nickname,player_country_id):
        self.player_id=player_id
        self.player_name=player_name
        self.player_nickname=player_nickname
        self.player_country_id=player_country_id
    
# Player Schema
class PlayerSchema(ma.Schema):
    class Meta:
        fields=('player_id','player_name','player_nickname','player_country_id')

# EventRelated Class/Model
class EventRelated(db.Model):
    event_id=db.Column(db.Integer,primary_key=True,nullable=False)
    event_rel_id=db.Column(db.Integer,db.ForeignKey('Event.event_id'),primary_key=True,nullable=False)

    def __init__(self,event_id,event_rel_id):
        self.event_id=event_id
        self.event_rel_id=event_rel_id
    
    

# EventRelated Schema
class EventRelatedSchema(ma.Schema):
    class Meta:
        fields=('event_id','event_rel_id')

# Event Class/Model
class Event(db.Model):
    event_id=db.Column(db.Integer,primary_key=True,nullable=False)
    event_match_id=db.Column(db.Integer,db.ForeignKey('Match.match_id'),nullable=False)
    event_index=db.Column(db.Integer,nullable=False)
    event_period=db.Column(db.Integer,nullable=False)
    event_timestamp=db.Column(db.Time,nullable=False)
    event_minute=db.Column(db.Integer,nullable=False)
    event_second=db.Column(db.Integer,nullable=False)
    event_type=db.Column(db.String(45),nullable=False)
    event_posession=db.Column(db.Integer,nullable=False)
    event_posession_team=db.Column(db.Integer,db.ForeignKey('Team.team_id'),nullable=False)
    event_play_pattern=db.Column(db.String(45),nullable=False)
    event_team_id=db.Column(db.Integer,db.ForeignKey('Team.team_id'),nullable=False)
    event_player_id=db.Column(db.Integer,db.ForeignKey('Player.player_id'))
    event_location_x=db.Column(db.Integer)
    event_location_y=db.Column(db.Integer)
    event_duration=db.Column(db.Float)
    event_under_pressure=db.Column(db.Integer)
    event_off_camera=db.Column(db.Integer)
    event_out=db.Column(db.Integer)
    event_related_id=db.Column(db.Integer,db.ForeignKey('EventRelated.event_id'),nullable=False)

    #Relantionships
    #event_related = db.relationship("EventRelated", backref="event_related")

    def __init__(self,event_id,event_match_id,event_index,event_period,event_timestamp,event_minute,event_second,event_type,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out,event_related_id):
        self.event_id=event_id
        self.event_match_id=event_match_id
        self.event_index=event_index
        self.event_period=event_period
        self.event_timestamp=event_timestamp
        self.event_minute=event_minute
        self.event_second=event_second
        self.event_type=event_type
        self.event_posession=event_posession
        self.event_posession_team=event_posession_team
        self.event_play_pattern=event_play_pattern
        self.event_team_id=event_team_id
        self.event_player_id=event_player_id
        self.event_location_x=event_location_x
        self.event_location_y=event_location_y
        self.event_duration=event_duration
        self.event_under_pressure=event_under_pressure
        self.event_off_camera=event_off_camera
        self.event_out=event_out
        self.event_related_id=event_related_id

# Event Schema
class EventSchema(ma.Schema):
    class Meta:
        fields=('event_id','event_match_id','event_index','event_period','event_timestamp','event_minute','event_second','event_type','event_posession','event_posession_team','event_play_pattern','event_team_id','event_player_id','event_location_x','event_location_y','event_duration','event_under_pressure','event_off_camera','event_out','event_related_events_id')

# Init schema en borador




def readCompetition(data):
    for json in data:
        competition_id = json['competition_id']
        competition_season_id= json['season_id']
        country_name=json['country_name']
        competition_name=json['competition_name']
        competition_gender=json['competition_gender']
        competition_season_name=json['season_name']
        competition_match_update=json['match_updated']
        competition_match_available=json['match_available']
        competition_country_id='1'

        new_competition = Competition(competition_id, competition_season_id, competition_name, competition_gender, competition_country_id, competition_season_name, competition_match_update, competition_match_available)
        db.session.add(new_competition)
        
    db.session.commit()
    return readCompetition.jsonify(new_competition)

def readCountry(data):
    country_id=data['id']
    name=data['name']
    new_country=Country(country_id,name)
    db.session.add(new_country)
    db.session.commit()

def readManager(data):
    manager_id=data['d']
    name=data['name']
    nickname=data['nickname']
    dob=data['dob']
    country=data['country']
    country_id=country['id']
    new_manager=Manager(manager_id,name,nickname,dob,country_id)
    db.session.add(new_manager)
    db.session.commit()

def readHomeTeam(data):
    team_id=data['home_team_id']
    name=data['home_team_name']
    gender=data['home_team_gender']
    group=data['home_team_group']
    country=data['country']
    readCountry(country)
    country_id=country['id']
    manager=data['managers']
    readManager(manager)
    manager_id=manager['id']
    new_team=Team(team_id,name,gender,manager_id,group,country_id)
    db.session.add(new_team)
    db.session.commit()

def readReferee(data):
    ref_id=data['id']
    name=data['name']
    new_ref=Referee(ref_id,name)
    db.session.add(new_ref)
    db.session.commit()

def readStadium(data):
    sta_id=data['id']
    name=data['name']
    country=data['country']
    country_id=country['id']
    new_sta=Stadium(sta_id,name,country_id)

def readMatch(data):
    match_id=request.json['match_id']
    match_date=request.json['match_date']
    match_kick_off=request.json['kick_off']
    competition=request.json['competition']
    match_competition_id=competition['competition_id']
    season=request.json['season']
    match_season_id=season['season_id']
    home_team=request.json['home_team']
    readHomeTeam(home_team)
    match_home_team_id=home_team['home_team_id']
    away_team=request.json['away_team']
    readAwayTeam(away_team)
    match_away_team_id=away_team['away_team_id']
    match_home_score=request.json['home_score']
    match_away_score=request.json['away_score']
    referee=request.json['referee']
    readReferee(referee)
    match_referee_id=referee['id']
    competition_stagej=request.json['competition_stage']
    match_competition_stage=competition_stagej['name']
    stadium = request.json['stadium']
    readStadium(stadium)
    match_stadium_id=stadium['id']

def readPlayer(data):
    player_id=data['player_id']
    player_name=data['player_name']
    player_nickname=data['player_nickname']
    country=data['country']
    country_id=country['id']
    new_player=Player(player_id,player_name,player_nickname,country_id)
    db.session.add(new_player)
    db.session.commit()

def readLineup(data):
    for json in data:
        team_id=json['team_id']
        lineup=json['lineup']
        lineup_data=json.load(lineup)
        for player in lineup_data:
            readPlayer(player)
            player_id=player['player_id']
            jersey_numer=player['jersey_number']
            new_lineup=Lineup(player_id,team_id,lineup_match_id,lineup_played,jersey_numer)
            db.session.add(new_lineup)
    #match_id?,lineup_played?
    db.session.commit()
    return readLineup.jsonify(new_lineup)

def readRelatedEvents(evid,data):
    for i in data:
        ev_id=evid
        rel= data[i]
        new_ev_rel=EventRelated(ev_id,rel)
        db.session.add(new_ev_rel)
        db.session.commit()

def readEvent(data):
    for json in data:
        ev_id=json['id']
        index=json['index']
        period=json['period']
        timestamp=json['timestamp']
        minute=json['minute']
        second=json['second']
        typed=json['type']
        evtype=typed['name']
        play_patternd=json['play_pattern']
        play_pattern=play_patternd['name']
        team=json['team']
        team_id=team['id']
        duration=data['duration']
        ##opcionales
        tactics=data['tactics']
        related_events=json['related_events']
        readRelatedEvents(ev_id,related_events)
        location=json['location']
        player=json['player']
        position=json['position']
        passd=json['pass']
        carry=json['carry']
        ball_receipt=json['ball_receipt']

        if tactics!= None:
            lineup=tactics['lineup']
            readLineup(lineup)#diferente con posiciones
        else:#hay multiples casos segun el tipo de evento
            ev=data['']
        

# Read JSON
competition_json=open('open-data-master/data/competitions.json')
competition_data =json.load(competition_json)
readCompetition(competition_data)

lineups=os.listdir("open-data-master/data/lineups")
lineup_data=list()
for l in lineups:
    with open(l) as f:
        current_data= json.load(f)
    lineup_data.append(current_data)
    readLineup(lineup_data)

events=os.listdir("open-data-master/data/events")
event_data=list()
for e in events:
    with open(e0) as f:
        current_data= json.load(f)
    event_data.append(current_data)
    readEvent(event_data)

matches=os.listdir("open-data-master/data/matches")
match_data=list()
for l in matchess:
    with open(m) as f:
        current_data= json.load(f)
    match_data.append(current_data)
    readMatch(match_data)

#Run server
if __name__ == '__main__':
    app.run(debug=True)