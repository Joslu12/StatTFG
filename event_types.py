from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os,json
import importlib
from models import *
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
    #events = db.relationship("Event",backref='player',lazy=True)
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
        fields=('lineup_player_id','lineup_match_id','lineup_team_id','lineup_played','lineup_jersey_number','lineup_position_id','lineup_sustitution','lineup_injury')

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
    event_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    event_rel_id=db.Column(db.String(45),primary_key=True,nullable=False)

    # Relationships
    events = db.relationship("Event",backref='event_related',lazy=True)
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
    event_posession=db.Column(db.Integer)
    event_posession_team_id=db.Column(db.Integer,db.ForeignKey('team.team_id'))
    event_play_pattern=db.Column(db.String(45))
    event_team_id=db.Column(db.Integer,db.ForeignKey('team.team_id'))
    event_player_id=db.Column(db.Integer,db.ForeignKey('player.player_id'))
    event_position_id=db.Column(db.Integer,db.ForeignKey('position.position_id'),nullable=False)
    event_location_x=db.Column(db.Integer)
    event_location_y=db.Column(db.Integer)
    event_duration=db.Column(db.Float)
    event_under_pressure=db.Column(db.Integer)
    event_off_camera=db.Column(db.Integer)
    event_out=db.Column(db.Integer)

    # Relantionships
    team= db.relationship("Team", foreign_keys=[event_team_id])
    posession_team= db.relationship("Team", foreign_keys=[event_posession_team_id])
    player= db.relationship("Player", foreign_keys=[event_player_id])
    position=db.relationship("Position",foreign_keys=[event_position_id])
    
    def __init__(self,event_id,event_match_id,event_index,event_period,event_timestamp,event_minute,event_second,event_type,event_posession,event_posession_team_id,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out):
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
        self.event_position_id=event_position_id
        self.event_location_x=event_location_x
        self.event_location_y=event_location_y
        self.event_duration=event_duration
        self.event_under_pressure=event_under_pressure
        self.event_off_camera=event_off_camera
        self.event_out=event_out

# Event Schema
class EventSchema(ma.Schema):
    class Meta:
        fields=('event_id','event_match_id','event_index','event_period','event_timestamp','event_minute','event_second','event_type','event_posession','event_posession_team','event_play_pattern','event_team_id','event_player_id','event_position_id','event_location_x','event_location_y','event_duration','event_under_pressure','event_off_camera','event_out')


# Types

# EvCarry
class EvCarry(db.Model):
    __tablename__ = 'evcarry'
    
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_end_loc_x=db.Column(db.Integer,nullable=False)
    ev_end_loc_y=db.Column(db.Integer,nullable=False)

    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_end_loc_x,ev_end_loc_y):
        self.ev_id=ev_id
        self.ev_end_loc_x=ev_end_loc_x
        self.ev_end_loc_y=ev_end_loc_y

# EvCarry Schema
class EvCarrySchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_end_loc_x','ev_end_loc_y')

# Pass
class EvPass(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_recipient_id=db.Column(db.Integer,db.ForeignKey('player.player_id'))
    ev_length=db.Column(db.Float,nullable=False)
    ev_angle=db.Column(db.Float,nullable=False)
    ev_height=db.Column(db.String(20),nullable=False)
    ev_end_loc_x=db.Column(db.Integer,nullable=False)
    ev_end_loc_y=db.Column(db.Integer,nullable=False)
    ev_body_part=db.Column(db.String(20),nullable=False)
    ev_assisted_shot_id=db.Column(db.String(45))
    ev_backheel= db.Column(db.Integer)
    ev_deflected=db.Column(db.Integer)
    ev_misscommunication=db.Column(db.Integer)
    ev_cross=db.Column(db.Integer)
    ev_cut_back=db.Column(db.Integer)
    ev_switch=db.Column(db.Integer)
    ev_shot_assist=db.Column(db.Integer)
    ev_goal_assist=db.Column(db.Integer)
    ev_type=db.Column(db.String(25))
    ev_outcome=db.Column(db.String(20))

    __tablename__ = 'evpass'

    # Relationships
    recipient= db.relationship("Player", foreign_keys=[ev_recipient_id])
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_recipient_id,ev_length,ev_angle,ev_height,ev_end_loc_x,ev_end_loc_y,ev_body_part,ev_assisted_shot_id,ev_backheel,ev_deflected,ev_misscommunication,ev_cross,ev_cut_back,ev_switch,ev_shot_assist,ev_goal_assist,ev_type,ev_outcome):
        self.ev_id=ev_id
        self.ev_recipient_id=ev_recipient_id
        self.ev_length=ev_length
        self.ev_angle=ev_angle
        self.ev_height=ev_height
        self.ev_end_loc_x=ev_end_loc_x
        self.ev_end_loc_y=ev_end_loc_y
        self.ev_body_part=ev_body_part
        self.ev_assisted_shot_id=ev_assisted_shot_id
        self.ev_backheel=ev_backheel
        self.ev_deflected=ev_deflected
        self.ev_misscommunication=ev_misscommunication
        self.ev_cross=ev_cross
        self.ev_cut_back=ev_cut_back
        self.ev_switch
        self.ev_shot_assist=ev_shot_assist
        self.ev_goal_assist=ev_goal_assist
        self.ev_type=ev_type
        self.ev_outcome=ev_outcome

# EvPass Schema
class EvPassSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_recipient_id','ev_length','ev_angle','ev_height','ev_end_loc_x','ev_end_loc_y','ev_body_part','ev_assisted_shot_id','ev_backheel','ev_deflected','ev_misscommunication','ev_cross','ev_cut_back','ev_switch','ev_shot_assist','ev_goal_assist','ev_type','ev_outcome')

# EvBallReceipt
class EvBallReceipt(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_outcome=db.Column(db.String(20))
    
    __tablename__ = 'evballreceipt'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_outcome):
        self.ev_id=ev_id
        self.ev_outcome=ev_outcome

# EvBallReceipt Schema
class EvBallReceiptSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_outcome')

# EvPressure
class EvPressure(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_counterpress=db.Column(db.Integer)

    __tablename__ = 'evpressure'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_counterpress):
        self.ev_id=ev_id
        self.ev_counterpress=ev_counterpress

# EvPressure Schema
class EvPressureSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_counterpress')

# EvBallRecovery
class EvBallRecovery(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_offensive=db.Column(db.Integer)
    ev_recovery_failure=db.Column(db.Integer)

    __tablename__ = 'evballrecovery'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_offensive,ev_recovery_failure):
        self.ev_id=ev_id
        self.ev_offensive=ev_offensive
        self.ev_recovery_failure=ev_recovery_failure

# EvBallRecovery Schema
class EvBallRecoverySchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_offensive','ev_recovery_failure')

# EvDuel
class EvDuel(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_type=db.Column(db.String(25),nullable=False)
    ev_outcome=db.Column(db.String(20))
    ev_counterpress=db.Column(db.Integer)

    __tablename__ = 'evduel'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_type,ev_outcome,ev_counterpress):
        self.ev_id=ev_id
        self.ev_type=ev_type
        self.ev_outcome=ev_outcome
        self.ev_counterpress=ev_counterpress

# EvDuel Schema
class EvDuelSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_type','ev_outcome','ev_counterpress')

# EvClearance 
class EvClearance(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_aerial_won=db.Column(db.Integer)
    ev_body_part=db.Column(db.String(20))

    __tablename__ = 'clearance'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_aerial_won,ev_body_part):
        self.ev_id=ev_id
        self.ev_aerial_won=ev_aerial_won
        self.ev_body_part=ev_body_part
    
# EvClearance Schema
class EvClearanceSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_aerial_won','ev_body_part')

# EvDribble 
class EvDribble(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_outcome=db.Column(db.String(20),nullable=False)
    ev_nutmeg=db.Column(db.Integer)
    ev_overrun=db.Column(db.Integer)
    ev_no_touch=db.Column(db.Integer)

    __tablename__='evdribble'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_outcome,ev_nutmeg,ev_overrun,ev_no_touch):
        self.ev_id=ev_id
        self.ev_outcome=ev_outcome
        self.ev_nutmeg=ev_nutmeg
        self.ev_overrun=ev_overrun
        self.ev_no_touch=ev_no_touch

# EvDribble Schema
class EvDribbleSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_outcome','ev_nutmeg','ev_overrun','ev_no_touch')

# EvBlock 
class EvBlock(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_counterpress=db.Column(db.Integer)
    ev_deflection=db.Column(db.Integer)
    ev_offensive=db.Column(db.Integer)
    ev_save_block=db.Column(db.Integer)

    __tablename__='evblock'  
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_counterpress,ev_deflection,ev_offensive,ev_save_block):
        self.ev_id=ev_id
        self.ev_counterpress=ev_counterpress
        self.ev_deflection=ev_deflection
        self.ev_offensive=ev_offensive
        self.ev_save_block=ev_save_block

# EvBlock Schema
class EvBlockSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_counterpress','ev_deflection','ev_offensive','ev_save_block')

# EvGoalkeeper
class EvGoalkeeper(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_outcome=db.Column(db.String(20))
    ev_technique=db.Column(db.String(20))
    ev_position=db.Column(db.String(20))
    ev_body_part=db.Column(db.String(20))
    ev_type=db.Column(db.String(20),nullable=False)

    __tablename__='evgoalkeeper'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_outcome,ev_technique,ev_position,ev_body_part,ev_type):
        self.ev_id=ev_id
        self.ev_outcome=ev_outcome
        self.ev_technique=ev_technique
        self.ev_position=ev_position
        self.ev_body_part=ev_body_part
        self.ev_type=ev_type

# EvGoalkeeper Schema
class EvGoalkeeper(ma.Schema):
    class Meta:
        fields=('ev_id','ev_outcome','ev_technique','ev_position','ev_body_part','ev_type')

# EvMiscontrol 
class EvMiscontrol(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False) 
    ev_aerial_won=db.Column(db.Integer)

    __tablename__='evmiscontrol'
     # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_aerial_won):
        self.ev_id=ev_id
        self.ev_aerial_won=ev_aerial_won

# EvMiscontrol Schema
class EvMiscontrolSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_aerial_won')

# EvFoulCommited
class EvFoulCommited(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False) 
    ev_counterpress= db.Column(db.Integer)
    ev_offensive=db.Column(db.Integer)
    ev_type=db.Column(db.String(45))
    ev_advantage=db.Column(db.Integer)
    ev_penalty=db.Column(db.Integer)
    ev_card=db.Column(db.String(20))

    __tablename__='evfoulcommited'
     # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_counterpress,ev_offensive,ev_type,ev_advantage,ev_penalty,ev_card):
        self.ev_id=ev_id
        self.ev_counterpress=ev_counterpress
        self.ev_offensive=ev_offensive
        self.ev_type=ev_type
        self.ev_advantage=ev_advantage
        self.ev_penalty=ev_penalty
        self.ev_card=ev_card

# EvFoulCommited Schema
class EvFoulCommitedSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_counterpress','ev_offensive','ev_type','ev_advantage','ev_penalty','ev_card')

# EvDribbledPast
class EvDribbledPast(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False) 
    ev_counterpress= db.Column(db.Integer)

    __tablename__='evdribbledpast'
     # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_counterpress):
        self.ev_id=ev_id
        self.ev_counterpress=ev_counterpress

# EvDribbledPast Schema
class EvDribbledPastSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_counterpress')

# EvFoulWon
class EvFoulWon(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False) 
    ev_defensive= db.Column(db.Integer)
    ev_advantage= db.Column(db.Integer)
    ev_penalty= db.Column(db.Integer)

    __tablename__='evfoulwon'
     # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_defensive,ev_advantage,ev_penalty):
        self.ev_id=ev_id
        self.ev_defensive=ev_defensive
        self.ev_advantage=ev_advantage
        self.ev_penalty=ev_penalty

# EvFoulWon Schema
class EvFoulWonSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_defensive','ev_advantage','ev_penalty')

# EvShot
class EvShot(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False) 
    ev_key_pass_id=db.Column(db.String(45),db.ForeignKey('event.event_id'))
    ev_end_loc_x=db.Column(db.Integer,nullable=False)
    ev_end_loc_y=db.Column(db.Integer,nullable=False)
    ev_end_loc_z=db.Column(db.Integer)
    ev_aerial_won=db.Column(db.Integer)
    ev_follows_dribble=db.Column(db.Integer)
    ev_first_time=db.Column(db.Integer)
    ev_open_goal=db.Column(db.Integer)
    ev_deflected=db.Column(db.Integer)
    ev_technique=db.Column(db.String(20),nullable=False)
    ev_body_part=db.Column(db.String(20),nullable=False)
    ev_type=db.Column(db.String(20),nullable=False)
    ev_outcome=db.Column(db.String(20),nullable=False)

    __tablename__='evshot'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])
    pase= db.relationship("Event",foreign_keys=[ev_key_pass_id])

    def __init__(self,ev_id,ev_key_pass_id,ev_end_loc_x,ev_end_loc_y,ev_end_loc_z,ev_aerial_won,ev_follows_dribble,ev_first_time,ev_open_goal,ev_deflected,ev_technique,ev_body_part,ev_type,ev_outcome):
        self.ev_id=ev_id
        self.ev_key_pass_id=ev_key_pass_id
        self.ev_end_loc_x=ev_end_loc_x
        self.ev_end_loc_y=ev_end_loc_y
        self.ev_end_loc_z=ev_end_loc_z
        self.ev_aerial_won=ev_aerial_won
        self.ev_follows_dribble=ev_follows_dribble
        self.ev_first_time=ev_first_time
        self.ev_open_goal=ev_open_goal
        self.ev_deflected=ev_deflected
        self.ev_technique=ev_technique
        self.ev_body_part=ev_body_part
        self.ev_type=ev_type
        self.ev_outcome=ev_outcome

# EvShot Schema
class EvShotSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_key_pass_id','ev_end_loc_x','ev_end_loc_y','ev_end_loc_z','ev_aerial_won','ev_follows_dribble','ev_first_time','ev_open_goal','ev_deflected','ev_technique','ev_body_part','ev_type','ev_outcome')

# EvInterception 
class EvInterception(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_outcome=db.Column(db.String(20))

    __tablename__='evinterception'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_outcome):
        self.ev_id=ev_id
        self.ev_outcome=ev_outcome

# EvInterception Schema
class EvInterceptionSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_outcome')

# EvSubstitution 
class EvSubstitution(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_replacement=db.Column(db.String(20),nullable=False)
    ev_outcome=db.Column(db.String(20),nullable=False)

    __tablename__='evsubstitution'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_replacement,ev_outcome):
        self.ev_id=ev_id
        self.ev_replacement
        self.ev_outcome=ev_outcome

# EvSubstitution  Schema
class EvSubstitutionSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_replacement','ev_outcome')

# EvStartingXI
class EvStartingXI(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_match_id=db.Column(db.Integer,db.ForeignKey('match.match_id'),primary_key=True,nullable=False)
    ev_team_id=db.Column(db.Integer,db.ForeignKey('team.team_id'),nullable=False)
    ev_formation=db.Column(db.Integer,nullable=False)
    ev_player_id=db.Column(db.Integer,db.ForeignKey('player.player_id'),nullable=False)
    ev_position_id=db.Column(db.Integer,db.ForeignKey('position.position_id'),nullable=False)
    ev_jersey_number=db.Column(db.Integer,nullable=False)

    __tablename__='evstartingxi'

    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])
    match= db.relationship("Match",foreign_keys=[ev_match_id])
    team = db.relationship("Team",foreign_keys=[ev_team_id])
    player= db.relationship("Player",foreign_keys=[ev_player_id])
    position = db.relationship("Position",foreign_keys=[ev_position_id])

    def __init__(self,ev_id,ev_match_id,ev_team_id,ev_formation,ev_player_id,ev_position_id,ev_jersey_number):
        self.ev_id=ev_id
        self.ev_match_id=ev_match_id
        self.ev_team_id=ev_team_id
        self.ev_formation=ev_formation
        self.ev_player_id=ev_player_id
        self.ev_position_id=ev_position_id
        self.ev_jersey_number=ev_jersey_number

# EvStartingXI Schema
class EvStartingXISchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_match_id','ev_team_id','ev_formation','ev_player_id','ev_position_id','ev_jersey_number')

# EvTacticalShift
class EvTacticalShift(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_match_id=db.Column(db.Integer,db.ForeignKey('match.match_id'),primary_key=True,nullable=False)
    ev_team_id=db.Column(db.Integer,db.ForeignKey('team.team_id'),nullable=False)
    ev_formation=db.Column(db.Integer,nullable=False)
    ev_player_id=db.Column(db.Integer,db.ForeignKey('player.player_id'),nullable=False)
    ev_position_id=db.Column(db.Integer,db.ForeignKey('position.position_id'),nullable=False)
    ev_jersey_number=db.Column(db.Integer,nullable=False)

    __tablename__='evtacticalshift'

    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])
    match= db.relationship("Match",foreign_keys=[ev_match_id])
    team = db.relationship("Team",foreign_keys=[ev_team_id])
    player= db.relationship("Player",foreign_keys=[ev_player_id])
    position = db.relationship("Position",foreign_keys=[ev_position_id])

    def __init__(self,ev_id,ev_match_id,ev_team_id,ev_formation,ev_player_id,ev_position_id,ev_jersey_number):
        self.ev_id=ev_id
        self.ev_match_id=ev_match_id
        self.ev_team_id=ev_team_id
        self.ev_formation=ev_formation
        self.ev_player_id=ev_player_id
        self.ev_position_id=ev_position_id
        self.ev_jersey_number=ev_jersey_number

# EvTacticalShift Schema
class EvTacticalShiftSchema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_match_id','ev_team_id','ev_formation','ev_player_id','ev_position_id','ev_jersey_number')

# Ev5050
class Ev5050(db.Model):
    ev_id=db.Column(db.String(45),db.ForeignKey('event.event_id'),primary_key=True,nullable=False)
    ev_outcome=db.Column(db.String(20),nullable=False)

    __tablename__='ev5050'
    # Relationships
    event= db.relationship("Event",foreign_keys=[ev_id])

    def __init__(self,ev_id,ev_outcome):
        self.ev_id=ev_id
        self.ev_outcome=ev_outcome

# Ev5050 Schema
class Ev5050Schema(ma.Schema):
    class Meta:
        fields=('ev_id','ev_outcome')