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
    stadiums = db.relationship('Stadium',backref='country',lazy=True)
    referees = db.relationship('Referee',backref='country',lazy=True)
    managers = db.relationship('Manager',backref='country',lazy=True)
    players = db.relationship("Player",backref='country',lazy=True)
    competitions = db.relationship('Competition',backref='country',lazy=True)
    teams = db.relationship("Team",backref='country',lazy=True)


    def __init__(self,country_id,country_name):
        self.country_id=country_id
        self.country_name=country_name

# Country Schema
class CountrySchema(ma.Schema):
    class Meta:
        fields=('country_id','country_name')

#Competition Class/Model
class Competition(db.Model):
    competition_id=db.Column(db.Integer,primary_key=True,nullable=False)
    competition_season_id=db.Column(db.Integer,primary_key=True,nullable=False)
    competition_name=db.Column(db.String(45),nullable=False)
    competition_gender=db.Column(db.String(45),nullable=False)
    competition_country_id=db.Column(db.Integer,db.ForeignKey('country.country_id'),nullable=False)
    competition_season_name=db.Column(db.String(45),nullable=False)
    competition_match_update=db.Column(db.DateTime,nullable=False)
    competition_match_available=db.Column(db.DateTime,nullable=False)

    # Relationships
    matchs= db.relationship("Match",backref='competition',lazy=True)

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

# Player Class/Model
class Player(db.Model):
    player_id=db.Column(db.Integer,primary_key=True,nullable=False)
    player_name=db.Column(db.String(45),nullable=False)
    player_nickname=db.Column(db.String(45))
    player_country_id=db.Column(db.Integer,db.ForeignKey('country.country_id'),nullable=False)

    #Relantionships
    events = db.relationship("Event",backref='player',lazy=True)
    lineups = db.relationship("Lineup",backref='player',lazy=True)
    def __init__(self,player_id,player_name,player_nickname,player_country_id):
        self.player_id=player_id
        self.player_name=player_name
        self.player_nickname=player_nickname
        self.player_country_id=player_country_id
    
# Player Schema
class PlayerSchema(ma.Schema):
    class Meta:
        fields=('player_id','player_name','player_nickname','player_country_id')

# Referee Class/Model
class Referee(db.Model):
    referee_id=db.Column(db.Integer,primary_key=True,nullable=False)
    referee_name=db.Column(db.String(45),nullable=False)
    referee_country_id=db.Column(db.Integer,db.ForeignKey('country.country_id'),nullable=False)

    # Relantionships
    matchs = db.relationship("Match",backref='referee',lazy=True)

    def __init__(self,referee_id,referee_name,referee_country_id):
        self.referee_id=referee_id
        self.referee_name=referee_name
        self.referee_country_id=referee_country_id

# Referee Schema
class RefereeSchema(ma.Schema):
    class Meta:
        fields=('referee_id','referee_name','referee_country_id')

# Stadium Class/Model
class Stadium(db.Model):
    stadium_id= db.Column(db.Integer,primary_key=True,nullable=False)
    stadium_name=db.Column(db.String(45),nullable=False)
    stadium_country_id=db.Column(db.Integer,db.ForeignKey('country.country_id'),nullable=False)

    # Relantionships
    matchs = db.relationship("Match",backref='stadium',lazy=True)

    def __init__(self,stadium_id,stadium_name,stadium_country_id):
        self.stadium_id=stadium_id
        self.stadium_name=stadium_name
        self.stadium_country_id=stadium_country_id

# Stadium Schema
class StadiumSchema(ma.Schema):
    class Meta:
        fields=('stadium_id','stadium_name','stadium_country_id')

#Manager Class/Model
class Manager(db.Model):
    manager_id=db.Column(db.Integer,primary_key=True,nullable=False)
    manager_name=db.Column(db.String(45),nullable=False)
    manager_nickname=db.Column(db.String(45))
    manager_dob=db.Column(db.DateTime)
    manager_country_id=db.Column(db.Integer,db.ForeignKey('country.country_id'),nullable=False)
    # Relationships
    teams = db.relationship("Team",backref='manager',lazy=True)

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

# Team Class/Model
class Team(db.Model):
    team_id=db.Column(db.Integer,primary_key=True,nullable=False)
    team_name=db.Column(db.String(45),nullable=False)
    team_gender=db.Column(db.String(45),nullable=False)
    team_manager_id=db.Column(db.Integer,db.ForeignKey('manager.manager_id'))
    team_group=db.Column(db.String(45))
    team_country_id=db.Column(db.Integer,db.ForeignKey('country.country_id'),nullable=False)

    # Relationships
    lineups = db.relationship("Lineup",backref='team',lazy=True)

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


# Lineup Class/Model
class Lineup(db.Model):
    lineup_player_id=db.Column(db.Integer,db.ForeignKey('player.player_id'),primary_key=True,nullable=False)
    lineup_match_id=db.Column(db.Integer,db.ForeignKey('match.match_id'),primary_key=True,nullable=False)
    lineup_team_id = db.Column(db.Integer,db.ForeignKey('team.team_id'),nullable=False)
    lineup_played= db.Column(db.Integer,nullable=False)
    lineup_jersey_number= db.Column(db.Integer,nullable=False)
    lineup_position_id =  db.Column(db.Integer,db.ForeignKey('position.position_id'),nullable=False)
    lineup_sustitution = db.Column(db.Integer)
    lineup_injury = db.Column(db.Integer)

    # Relationship
    #players= db.relationship("Player")

    def __init__(self,lineup_player_id,lineup_match_id,lineup_team_id,lineup_played,lineup_jersey_number,lineup_position_id,lineup_sustitution,lineup_injury):
        self.lineup_player_id=lineup_player_id
        self.lineup_match_id=lineup_match_id
        self.lineup_team_id=lineup_team_id
        self.lineup_played=lineup_played
        self.lineup_jersey_number=lineup_jersey_number
        self.lineup_position_id=lineup_position_id
        self.lineup_sustitution=lineup_sustitution
        self.lineup_injury=lineup_injury

# Lineup Schema
class LineupSchema(ma.Schema):
    class Meta:
        fields=('lineup_player_id','lineup_match_id','lineup_team_id','lineup_played','lineup_jersey_number','lineup_position_id','lineup_sustituion','lineup_injury')

# Position Class/Model
class Position(db.Model):
    position_id=db.Column(db.Integer,primary_key=True,nullable=False)
    position_name=db.Column(db.String(3),nullable=False)

    # Relantionships     
    lineups = db.relationship("Lineup",backref='position',lazy=True)

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
    match_competition_id = db.Column(db.Integer,db.ForeignKey('competition.competition_id'),nullable=False)
    match_date = db.Column(db.DateTime,nullable=False)
    match_kick_off= db.Column(db.DateTime)
    match_stadium_id = db.Column(db.Integer,db.ForeignKey('stadium.stadium_id'))
    match_referee_id = db.Column(db.Integer,db.ForeignKey('referee.referee_id'))
    match_home_team_id = db.Column(db.Integer,db.ForeignKey('team.team_id'),nullable=False)
    match_away_team_id = db.Column(db.Integer,db.ForeignKey('team.team_id'),nullable=False)
    match_home_score = db.Column(db.Integer,nullable=False)
    match_away_score = db.Column(db.Integer,nullable=False)
    match_competition_stage = db.Column(db.String(45),nullable=False)

    # Relantionships
    events = db.relationship("Event",backref='match',lazy=True)
    lineups = db.relationship("Lineup",backref='match',lazy=True)
    home_team= db.relationship("Team", foreign_keys=[match_home_team_id])
    away_team= db.relationship("Team", foreign_keys=[match_away_team_id])

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

# EventRelated Class/Model
class EventRelated(db.Model):
    event_id=db.Column(db.String(45),primary_key=True,nullable=False)
    event_rel_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)

    # Relationships
     #events = db.relationship("Event",backref='event_related',lazy=True)
    def __init__(self,event_id,event_rel_id):
        self.event_id=event_id
        self.event_rel_id=event_rel_id

# EventRelated Schema
class EventRelatedSchema(ma.Schema):
    class Meta:
        fields=('event_id','event_rel_id')

# Event Class/Model
class Event(db.Model):
    event_id=db.Column(db.String(45),primary_key=True,nullable=False)
    event_match_id=db.Column(db.Integer,db.ForeignKey('match.match_id'),nullable=False)
    event_index=db.Column(db.Integer,nullable=False)
    event_period=db.Column(db.Integer,nullable=False)
    event_timestamp=db.Column(db.Time,nullable=False)
    event_minute=db.Column(db.Integer,nullable=False)
    event_second=db.Column(db.Integer,nullable=False)
    event_type=db.Column(db.String(45),nullable=False)
    event_posession=db.Column(db.Integer,nullable=False)
    event_posession_team_id=db.Column(db.Integer,db.ForeignKey('team.team_id'),nullable=False)
    event_play_pattern=db.Column(db.String(45),nullable=False)
    event_team_id=db.Column(db.Integer,db.ForeignKey('team.team_id'),nullable=False)
    event_player_id=db.Column(db.Integer,db.ForeignKey('player.player_id'))
    event_location_x=db.Column(db.Integer)
    event_location_y=db.Column(db.Integer)
    event_duration=db.Column(db.Float)
    event_under_pressure=db.Column(db.Integer)
    event_off_camera=db.Column(db.Integer)
    event_out=db.Column(db.Integer)
    event_related_id=db.Column(db.String(200),db.ForeignKey('event_related.event_id'))

    # Relantionships
    team= db.relationship("Team", foreign_keys=[event_team_id])
    posession_team= db.relationship("Team", foreign_keys=[event_posession_team_id])
    #event_related = db.relationship("EventRelated", foreign_keys=[event_related_id])

    def __init__(self,event_id,event_match_id,event_index,event_period,event_timestamp,event_minute,event_second,event_type,event_posession,event_posession_team_id,event_play_pattern,event_team_id,event_player_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out,event_related_id):
        self.event_id=event_id
        self.event_match_id=event_match_id
        self.event_index=event_index
        self.event_period=event_period
        self.event_timestamp=event_timestamp
        self.event_minute=event_minute
        self.event_second=event_second
        self.event_type=event_type
        self.event_posession=event_posession
        self.event_posession_team_id=event_posession_team_id
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


# Methods

def readCountry(data):
    country_id=data['id']
    name=data['name']
    new_country=Country(country_id,name)
    db.session.add(new_country)
    db.session.commit()

def readManager(data):
    manager_id=data['id']
    name=data['name']
    nickname=data['nickname']
    dob=data['dob']
    country_id=data['country']['id']
    new_manager=Manager(manager_id,name,nickname,dob,country_id)
    db.session.add(new_manager)
    db.session.commit()

def readReferee(data):
    ref_id=data['id']
    name=data['name']
    if 'country' in data:
        country=data['country']['id']
    else:
        country=300 # Unknown
    new_ref=Referee(ref_id,name,country)
    db.session.add(new_ref)
    db.session.commit()

def readStadium(data):
    sta_id=data['id']
    name=data['name']
    country=data['country']['id']
    new_sta=Stadium(sta_id,name,country)
    db.session.add(new_sta)
    db.session.commit()

def readHomeTeam(data):
    manager_id=None #UnboundLocalError: local variable 'manager_id' referenced before assignment
    team_id=data['home_team_id']
    name=data['home_team_name']
    gender=data['home_team_gender']
    group=data['home_team_group']
    country=data['country']
    if not db.session.query(Country).filter(Country.country_id == country['id']).first():
        readCountry(country)
    country_id=country['id']
    if 'managers' in data:
        manager=data['managers'][0]
        if not db.session.query(Manager).filter(Manager.manager_id == manager['id']).first():
            readManager(manager)
            manager_id=manager['id']
        
    new_team=Team(team_id,name,gender,manager_id,group,country_id)
    db.session.add(new_team)
    db.session.commit()

def readAwayTeam(data):
    manager_id=None #UnboundLocalError: local variable 'manager_id' referenced before assignment
    team_id=data['away_team_id']
    name=data['away_team_name']
    gender=data['away_team_gender']
    group=data['away_team_group']
    country=data['country']
    if not db.session.query(Country).filter(Country.country_id == country['id']).first():
        readCountry(country)
    country_id=country['id']
    if 'managers' in data:
        manager=data['managers'][0]
        if not db.session.query(Manager).filter(Manager.manager_id == manager['id']).first():
            readManager(manager)
            manager_id=manager['id']

    new_team=Team(team_id,name,gender,manager_id,group,country_id)
    db.session.add(new_team)
    db.session.commit()

def readLineupCountry(data):
    for json in data:
        lineup1=json[0]['lineup']
        lineup2=json[1]['lineup']
        for p in lineup1:
            country=p['country']['id']
            if not db.session.query(Country).filter(Country.country_id == country).first():
                readCountry(country)
        
        for p in lineup2:
            country=p['country']['id']
            if not db.session.query(Country).filter(Country.country_id == country).first():
                readCountry(country)

def readMatchCountry(data):
    for d in data:
        for json in d:
            #print(json)
            country1=json['home_team']['country']['id']
            if not db.session.query(Country).filter(Country.country_id == country1).first():
                readCountry(country1)
            country2=json['away_team']['country']['id']
            if not db.session.query(Country).filter(Country.country_id == country2).first():
                readCountry(country2)
            if 'managers' in json['home_team']:
                if 'country' in json['home_team']['managers'][0]:
                    country3=json['home_team']['managers'][0]['country']
                    if not db.session.query(Country).filter(Country.country_id == country3['id']).first():
                        readCountry(country3)
            if 'managers' in json['away_team']:
                if 'country' in json['away_team']['managers'][0]:      
                    country4=json['away_team']['managers'][0]['country']
                    if not db.session.query(Country).filter(Country.country_id == country4['id']).first():
                        readCountry(country4)
            if 'referee' in json:
                if 'country' in json['referee']:
                    country5=json['referee']['country']
                    if not db.session.query(Country).filter(Country.country_id == country5['id']).first():
                        readCountry(country5)
            
def readMatch1(data):
    for d in data:
        for json in d:
            #print(json)
            if 'managers' in json['home_team']:
                manager1=json['home_team']['managers'][0]
                if not db.session.query(Manager).filter(Manager.manager_id == manager1['id']).first():
                    readManager(manager1)
            
            if 'managers' in json['away_team']:      
                manager2=json['away_team']['managers'][0]
                if not db.session.query(Manager).filter(Manager.manager_id == manager2['id']).first():
                    readManager(manager2)
            if 'stadium' in json:
                stadium=json['stadium']
                if not db.session.query(Stadium).filter(Stadium.stadium_id == stadium['id']).first():
                    readStadium(stadium)
            if 'referee' in json:
                referee=json['referee']
                if not db.session.query(Referee).filter(Referee.referee_id == referee['id']).first():
                    readReferee(referee)
           
def readMatchTeam(data):
    for d in data:
        for json in d:
            home_team= db.session.query(Team).filter(Team.team_id == json['home_team']['home_team_id']).first()
            if home_team == None:
                readHomeTeam(json['home_team'])
            else:
                if home_team.team_manager_id == None and 'managers' in json['home_team']:
                    home_team.team_manager_id=json['home_team']['managers'][0]['id']
                    db.session.commit()
            away_team= db.session.query(Team).filter(Team.team_id == json['away_team']['away_team_id']).first()
            if away_team == None:
                readAwayTeam(json['away_team'])
            else:
                if away_team.team_manager_id == None and 'managers' in json['away_team']:
                    away_team.team_manager_id=json['away_team']['managers'][0]['id']
                    db.session.commit()

def readCompetition(data):
    for json in data:
        if  not db.session.query(Competition).filter(Competition.competition_id == json['competition_id']).first():
            competition_id = json['competition_id']
            competition_season_id= json['season_id']
            country_name=json['country_name']
            competition_name=json['competition_name']
            competition_gender=json['competition_gender']
            competition_season_name=json['season_name']
            competition_match_update=json['match_updated']
            competition_match_available=json['match_available']
            country=json['country_name']
            o=db.session.query(Country).filter(Country.country_name == country).first()
            competition_country_id=o.country_id

            new_competition = Competition(competition_id, competition_season_id, competition_name, competition_gender, competition_country_id, competition_season_name, competition_match_update, competition_match_available)
            db.session.add(new_competition)
        
    db.session.commit()

def readPlayer(data):
    player_id=data['player_id']
    player_name=data['player_name']
    player_nickname=None
    if 'player_nickname' in data:
        player_nickname=data['player_nickname']
    country_id=data['country']['id']
    new_player=Player(player_id,player_name,player_nickname,country_id)
    db.session.add(new_player)
    db.session.commit()

def readLineupPlayer(data):
    for json in data:
        lineup1=json[0]['lineup']
        lineup2=json[1]['lineup']
        for p in lineup1:
            if not db.session.query(Player).filter(Player.player_id == p['player_id']).first():
                readPlayer(p)
        
        for p in lineup2:
            if not db.session.query(Player).filter(Player.player_id == p['player_id']).first():
                readPlayer(p)

def readLineup(data):
    for json in data:
        match_id=json[0]['match_id']
        if  db.session.query(Match).filter(Match.match_id == match_id).first():
            team1=json[0]['team_id']
            lineup1=json[0]['lineup']
            team2=json[1]['team_id']
            lineup2=json[1]['lineup']
            for p in lineup1:
                player_id=p['player_id']
                jersey_number=p['jersey_number']
                new_lineup=Lineup(player_id,match_id,team1,0,jersey_number,26,0,0)
                if not db.session.query(Lineup).filter(Lineup.lineup_player_id == player_id and Lineup.lineup_match_id == match_id).first():
                    db.session.add(new_lineup)
        
            for p in lineup2:
                player_id=p['player_id']
                jersey_number=p['jersey_number']
                new_lineup=Lineup(player_id,match_id,team2,0,jersey_number,26,0,0)
                if not db.session.query(Lineup).filter(Lineup.lineup_player_id == player_id and Lineup.lineup_match_id == match_id).first():
                    db.session.add(new_lineup)
     
    db.session.commit()    

def readMatch(data):
    for d in data:
        for json in d:
            if not db.session.query(Match).filter(Match.match_id == json['match_id']).first():
                if not db.session.query(Competition).filter(Competition.competition_season_id == json['season']['season_id']).first():
                    print("ENTRO")
                    country=json['competition']['country_name']
                    o=db.session.query(Country).filter(Country.country_name == country).first()
                    new_comp=Competition(json['competition']['competition_id'],json['season']['season_id'],json['competition']['competition_name'],'unknown',o.country_id,json['season']['season_name'],json['match_date'],json['match_date'])
                    db.session.add(new_comp)
                    db.session.commit()
                match_id=json['match_id']
                match_date=json['match_date']
                match_kick_off=json['kick_off']
                match_competition=json['competition']['competition_id']
                match_season=json['season']['season_id']
                match_home_team=json['home_team']['home_team_id']
                match_away_team=json['away_team']['away_team_id']
                match_home_score=json['home_score']
                match_away_score=json['away_score']
                match_competition_stage=json['competition_stage']['name']
                match_referee=None
                match_stadium_id=None
                if 'referee' in json:
                    match_referee=json['referee']['id']
                if 'stadium' in json:
                    match_stadium_id=json['stadium']['id']

                new_match=Match(match_id,match_season,match_competition,match_date,match_kick_off,match_stadium_id,match_referee,match_home_team,match_away_team,match_home_score,match_away_score,match_competition_stage)
                db.session.add(new_match)
        
        db.session.commit()

def readEventRelated(evid,data):
    for d in data:
        new_evrel=EventRelated(evid,d)
        db.session.add(new_evrel)
    db.session.commit()

def readEvent(data):
    for d in data:
        event_match_id=d[0]['match_id']
        if  db.session.query(Match).filter(Match.match_id == event_match_id).first():
            for json in d:
                ev_id=json['id']
                index=json['index']
                period=json['period']
                timestamp=json['timestamp']
                minute=json['minute']
                second=json['second']
                evtype=json['type']['name']
                event_posession=None
                event_posession_team=None
                event_play_pattern=None
                event_team_id=None
                event_player_id=None
                event_location_x=None
                event_location_y=None
                event_duration=None
                event_under_pressure=None
                event_off_camera=None
                event_out=None
                event_related_id=None
                new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out,event_related_id)
                db.session.add(new_ev)
                db.session.commit()
                #if 'related_events' in json:
                #    readEventRelated(ev_id,json['related_events'])
                

# Read JSON

lineup_data=list()
match_data=list()
event_data=list()

def readData():
    #Lineup
    lineups=os.listdir("open-data-master/data/lineups")
    path="open-data-master/data/lineups/"
    for l in lineups:
        with open(path+l,encoding="utf-8") as f:
            current_data= json.load(f)
        n = l[:l.find('.')]
        current_data[0]['match_id'] = n
        #print(current_data)
        lineup_data.append(current_data)
    # Match
    matches=os.listdir("open-data-master/data/matches")
    path="open-data-master/data/matches/"
    for m in matches:
        with open(path+m,encoding="utf-8") as f:
            current_data= json.load(f)
        match_data.append(current_data)
    # Event
    events=os.listdir("open-data-master/data/events")
    path="open-data-master/data/events/"
    for e in events:
        with open(path+e,encoding="utf-8") as f:
            current_data= json.load(f)
        n = e[:e.find('.')]
        current_data[0]['match_id'] = n
        event_data.append(current_data)

competition_json=open('open-data-master/data/competitions.json')
competition_data =json.load(competition_json)

readData()
print("Data read")
# Read Country
#readLineupCountry(lineup_data)
#readMatchCountry(match_data)
print("Country read")
# Read Tables which only have fk_country
#readCompetition(competition_data)
#readMatch1(match_data) #managers,referee,stadium
#readMatchTeam(match_data) #teams
# readLineupPlayer(lineup_data) #players
#readMatch(match_data) #matchs
#readLineup(lineup_data) #lineups
readEvent(event_data)#events
print("All read")