from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os,json
import importlib
from event_types import *

# Init app
app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Methods


def update(json,event_match_id):
    print("\n Nueva")
    ev_id=json['id']
    # Substitution Details
    ev_replacement=json['substitution']['replacement']['id']
    ev_outcome=None
    if 'outcome' in json['substitution']:
        ev_outcome=json['substitution']['outcome']['name']
    new_sb=EvSubstitution(ev_id,ev_replacement,ev_outcome)
    db.session.add(new_sb)
    db.session.commit()

def readPass(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Pass Details
    ev_recipient_id=None
    if 'recipient' in json['pass']:
        ev_recipient_id=json['pass']['recipient']['id']
    ev_length=json['pass']['length']
    ev_angle=json['pass']['angle']
    ev_height=json['pass']['height']['name']
    ev_end_loc_x=json['pass']['end_location'][0]
    ev_end_loc_y=json['pass']['end_location'][1]
    ev_body_part=None
    if 'body_part' in json:
        ev_body_part=json['pass']['body_part']['name']
    ev_assisted_shot_id=None
    ev_backheel= None
    ev_deflected=None
    ev_misscommunication=None
    ev_cross=None
    ev_cut_back=None
    ev_switch=None
    ev_shot_assist=None
    ev_goal_assist=None
    ev_type=None
    ev_outcome=None
    # Optional
    if 'type' in json['pass']:
        ev_type=json['pass']['type']['name']
    if 'shot_assit' in json['pass']:
        ev_assisted_shot_id=json['pass']['assisted_shot_id']
        ev_shot_assist=1
    if 'backheel' in json['pass']:
        ev_backheel=1
    if 'deflected' in json['pass']:
        ev_deflected=1
    if 'misscommunication' in json['pass']:
        ev_misscommunication=1
    if 'cross' in json['pass']:
        ev_cross =1
    if 'cut_back' in json['pass']:
        ev_cut_back=1
    if 'switch' in json['pass']:
        ev_switch=1
    if 'goal_assist' in json['pass']:
        ev_assisted_shot_id=json['pass']['assisted_shot_id']
        ev_goal_assist=1
    if 'outcome' in json['pass']:
        ev_outcome=json['pass']['outcome']['name']
    # Insert Pass
    new_pass=EvPass(ev_id,ev_recipient_id,ev_length,ev_angle,ev_height,ev_end_loc_x,ev_end_loc_y,ev_body_part,ev_assisted_shot_id,ev_backheel,ev_deflected,ev_misscommunication,ev_cross,ev_cut_back,ev_switch,ev_shot_assist,ev_goal_assist,ev_type,ev_outcome)
    db.session.add(new_pass)
    db.session.commit()

def readCarry(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Carry Details
    ev_end_loc_x=json['carry']['end_location'][0]
    ev_end_loc_y=json['carry']['end_location'][1]
    new_carry=EvCarry(ev_id,ev_end_loc_x,ev_end_loc_y)
    db.session.add(new_carry)
    db.session.commit()

def readBallReceipt(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # BallReceipt Details
    ev_outcome=None
    # Optional
    if 'ball_receipt' in json:
        if 'outcome' in json['ball_receipt']:
            ev_outcome=json['ball_receipt']['outcome']['name']
    # Insert BallReceipt
    new_ball=EvBallReceipt(ev_id,ev_outcome)
    db.session.add(new_ball)
    db.session.commit()

def readPressure(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Pressure Details
    ev_counterpress=None
    if 'counterpress' in json:
        ev_counterpress=1
    new_press=EvPressure(ev_id,ev_counterpress)
    db.session.add(new_press)
    db.session.commit()

def readBallRecovery(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # BallRecovery Details
    ev_offensive=None
    ev_recovery=None
    if 'ball_recovery' in json:
        if 'offensive' in json['ball_recovery']:
            ev_offensive=1
        if 'recovery_failure' in json['ball_recovery']:
            ev_recovery=1
    new_reco=EvBallRecovery(ev_id,ev_offensive,ev_recovery)
    db.session.add(new_reco)
    db.session.commit()

def readDuel(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Duel Details
    ev_type=json['duel']['type']['name']
    ev_outcome=None
    ev_counterpress=None
    if 'outcome' in json['duel']:
        ev_outcome=json['duel']['outcome']['name']
    if 'counterpress' in json:
        ev_counterpress=1
    new_duel=EvDuel(ev_id,ev_type,ev_outcome,ev_counterpress)
    db.session.add(new_duel)
    db.session.commit()

def readClearance(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Clearance Details
    ev_aerial_won=None
    ev_body_part=None
    if 'clearance' in json:
        if 'aerial_won' in json['clearance']:
            ev_aerial_won=1
        if 'body_part' in json['clearance']:
            ev_body_part=json['clearance']['body_part']['name']
    new_clea=EvClearance(ev_id,ev_aerial_won,ev_body_part)
    db.session.add(new_clea)
    db.session.commit()

def readDribble(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Dribble Dedtails
    ev_nutmeg=None
    ev_overrun=None
    ev_no_touch=None
    ev_outcome=json['dribble']['outcome']['name']
    if 'nutmeg' in json['dribble']:
        ev_nutmeg=1
    if 'overrun' in json['dribble']:
        ev_overrun=1
    if 'no_touch' in json:
        ev_no_touch=1
    new_dribble=EvDribble(ev_id,ev_outcome,ev_nutmeg,ev_overrun,ev_no_touch)
    db.session.add(new_dribble)
    db.session.commit()

def readBlock(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    #Block Details
    ev_counterpress=None
    ev_deflection=None
    ev_offensive=None
    ev_save_block=None
    if 'counterpress' in json:
        ev_counterpress=1
    if 'block' in json:
        if 'deflection' in json['block']:
            ev_deflection=1
        if 'offensive' in json['block']:
            ev_offensive=1
        if 'save_block' in json['block']:
            ev_save_block=1
    new_block=EvBlock(ev_id,ev_counterpress,ev_deflection,ev_offensive,ev_save_block)
    db.session.add(new_block)
    db.session.commit()

def readGoalkeeper(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=None
    if 'player' in json:
        event_player_id=json['player']['id']
    event_position_id=None
    if 'position' in json:
        event_position_id=json['position']['id']
    event_location_x=None
    event_location_y=None
    if 'location' in json:
        event_location_x=json['location'][0]
        event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Goalkeeper Details
    ev_outcome=None
    ev_technique=None
    ev_position=None
    ev_body_part=None
    ev_type=None
    if 'type' in json['goalkeeper']:
        ev_type=json['goalkeeper']['type']['name']
    if 'outcome' in json['goalkeeper']:
        ev_outcome=json['goalkeeper']['outcome']['name']
    if 'technique' in json['goalkeeper']:
        ev_technique=json['goalkeeper']['technique']['name']
    if 'position' in json['goalkeeper']:
        ev_position=json['goalkeeper']['position']['name']
    if 'body_part' in json['goalkeeper']:
        ev_body_part=json['goalkeeper']['body_part']['name']
    new_gk=EvGoalkeeper(ev_id,ev_outcome,ev_technique,ev_position,ev_body_part,ev_type)
    #new_gk=EvGoalkeeper(ev_id=ev_id,ev_outcome=ev_outcome,ev_technique=ev_technique,ev_position=ev_position,ev_body_part=ev_body_part,ev_type=ev_type)
    db.session.add(new_gk)
    db.session.commit()

def readMiscontrol(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Miscontrol Details
    ev_aerial_won=None
    if 'miscontrol' in json:
        if 'aerial_won' in json['miscontrol']:
            ev_aerial_won=1
    new_mc=EvMiscontrol(ev_id,ev_aerial_won)
    db.session.add(new_mc)
    db.session.commit()
    
def readFoulCommited(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    # Foul Commited Details
    ev_counterpress=None
    ev_offensive=None
    ev_type=None
    ev_advantage=None
    ev_penalty=None
    ev_card=None
    if 'counterpress' in json:
        ev_counterpress=1
    if 'foul_committed' in json:
        if 'advantage' in json['foul_committed']:
            ev_advantage=1
        if 'card' in json['foul_committed']:
            ev_card=json['foul_committed']['card']['name']
        if 'offensive' in json['foul_committed']:
            ev_offensive=json['foul_committed']['offensive']
        if 'type' in json['foul_committed']:
            ev_type=json['foul_committed']['type']['name']
        if 'penalty' in json['foul_committed']:
            ev_penalty=json['foul_committed']['penalty']
    new_fc=EvFoulCommited(ev_id,ev_counterpress,ev_offensive,ev_type,ev_advantage,ev_penalty,ev_card)
    db.session.add(new_fc)
    db.session.commit()

def readDribbledPast(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Dribbled Past
    ev_counterpress=None
    if 'counterpress' in json:
        ev_counterpress=1
    new_db=EvDribbledPast(ev_id,ev_counterpress)
    db.session.add(new_db)
    db.session.commit()

def readFoulWon(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # FoulWon Details
    ev_defensive=None
    ev_advantage=None
    ev_penalty=None
    if 'foul_won' in json:
        if 'defensive' in json['foul_won']:
            ev_defensive=1
        if 'advantage' in json['foul_won']:
            ev_advantage=1
        if 'penalty' in json['foul_won']:
            ev_penalty=1
    new_fw=EvFoulWon(ev_id,ev_defensive,ev_advantage,ev_penalty)
    db.session.add(new_fw)
    db.session.commit()

def readShot(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=None
    event_location_y=None
    if 'location' in json:
        event_location_x=json['location'][0]
        event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Shot Details
    ev_end_loc_x=json['shot']['end_location'][0]
    ev_end_loc_y=json['shot']['end_location'][1]
    ev_end_loc_z=None
    if len(json['shot']['end_location'])==3:
        ev_end_loc_z=json['shot']['end_location'][2]
    ev_technique=json['shot']['technique']['name']
    ev_type=json['shot']['type']['name']
    ev_body_part=json['shot']['body_part']['name']
    ev_outcome=json['shot']['outcome']['name']
    ev_key_pass_id=None
    ev_aerial_won=None
    ev_follows_dribble=None
    ev_first_time=None
    ev_open_goal=None
    ev_deflected=None
    if 'key_pass_id' in json:
        ev_key_pass_id=json['key_pass_id']
    if 'aerial_won' in json['shot']:
        ev_aerial_won=json['shot']['aerial_won']
    if 'follows_dribble' in json['shot']:
        ev_follows_dribble=json['shot']['follows_dribble']
    if 'first_time' in json['shot']:
        ev_first_time=json['shot']['first_time']
    if 'open_goal' in json['shot']:
        ev_open_goal=json['shot']['open_goal']
    if 'deflected' in json['shot']:
        ev_deflected=json['shot']['deflected']
    new_shot=EvShot(ev_id,ev_key_pass_id,ev_end_loc_x,ev_end_loc_y,ev_end_loc_z,ev_aerial_won,ev_follows_dribble,ev_first_time,ev_open_goal,ev_deflected,ev_technique,ev_body_part,ev_type,ev_outcome)
    db.session.add(new_shot)
    db.session.commit()

def readInterception(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Interception Details
    ev_outcome= None
    if 'interception' in json:
        ev_outcome=json['interception']['outcome']['name']
    new_in=EvInterception(ev_id,ev_outcome)
    db.session.add(new_in)
    db.session.commit()

def readSubstitution(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=None
    event_location_y=None
    if 'location' in json:
        event_location_x=json['location'][0]
        event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Substitution Details
    ev_replacement=json['substitution']['replacement']['id']
    ev_outcome=None
    if 'outcome' in json['substitution']:
        ev_outcome=json['substitution']['outcome']['name']
    new_sb=EvSubstitution(ev_id,ev_replacement,ev_outcome)
    db.session.add(new_sb)
    db.session.commit()

def readStartingXI(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=None
    if 'player' in json:
        event_player_id=json['player']['id']
    event_position_id=None
    if 'position' in json:
        event_position_id=json['position']['id']
    event_location_x=None
    event_location_y=None
    if 'location' in json:
        event_location_x=json['location'][0]
        event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # StartingXI Details
    ev_team=json['team']['id']
    ev_formation=json['tactics']['formation']
    ev_lineup=json['tactics']['lineup']
    for p in ev_lineup:
        ev_player=p['player']['id']
        ev_position=p['position']['id']
        ev_jersey_number=p['jersey_number']
        new_p=EvStartingXI(ev_id,event_match_id,ev_team,ev_formation,ev_player,ev_position,ev_jersey_number)
        db.session.add(new_p)
    db.session.commit()

def readTacticalShift(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=None
    if 'player' in json:
        event_player_id=json['player']['id']
    event_position_id=None
    if 'position' in json:
        event_position_id=json['position']['id']
    event_location_x=None
    event_location_y=None
    if 'location' in json:
        event_location_x=json['location'][0]
        event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # StartingXI Details
    ev_team=json['team']['id']
    ev_formation=json['tactics']['formation']
    ev_lineup=json['tactics']['lineup']
    for p in ev_lineup:
        ev_player=p['player']['id']
        ev_position=p['position']['id']
        ev_jersey_number=p['jersey_number']
        new_p=EvTacticalShift(ev_id,event_match_id,ev_team,ev_formation,ev_player,ev_position,ev_jersey_number)
        db.session.add(new_p)
    db.session.commit()

def read5050(json,event_match_id):
    # Create Event
    ev_id=json['id']
    index=json['index']
    period=json['period']
    timestamp=json['timestamp']
    minute=json['minute']
    second=json['second']
    evtype=json['type']['name']         
    event_posession=json['possession']
    event_posession_team=json['possession_team']['id']
    event_play_pattern=json['play_pattern']['name']
    event_team_id=json['team']['id']
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=None
    if 'duration' in json:
        event_duration=json['duration']
    event_under_pressure=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # 5050 Details
    ev_outcome= json['50_50']['outcome']['name']
    new_50=Ev5050(ev_id,ev_outcome)
    db.session.add(new_50)
    db.session.commit()


def readEventRelated(evid,data):
    """
    try:
        for d in data:
            new_evrel=EventRelated(evid,d)
            db.session.add(new_evrel)
        db.session.commit()
    except:
        pass
    """

def readEv(data):
    for json in data:
        """
        if(evtype == 'Pass'): readPass(json,event_match_id)
        elif(evtype == 'Carry'): readCarry(json,event_match_id)
        
        evtype=json['type']['name']
        event_match_id=json['match_id']
        if(evtype == 'Ball Recovery'): 
            if  db.session.query(Event).filter(Event.event_id == json['id']).count() == 0:
                readBallRecovery(json,event_match_id)
        if(evtype == 'Ball Receipt*'): 
            if  db.session.query(Event).filter(Event.event_id == json['id']).count() == 0:
                readBallReceipt(json,event_match_id)
        else:
            pass 
        """
        event_match_id=json['match_id']
        ev_id=json['id']
        if  db.session.query(Event).filter(Event.event_id == ev_id).count() == 0:
            readSubstitution(json,event_match_id)
        else:
            update(json,event_match_id)

def readEvent(data):
    for json in data:
        event_match_id=json['match_id']
        if  db.session.query(Match).filter(Match.match_id == event_match_id).first():
            ev_id=json['id']
            if  db.session.query(Event).filter(Event.event_id == ev_id).count() == 0:
                evtype=json['type']['name']
                """
                if(evtype == 'Foul Won'): readFoulWon(json,event_match_id)
                elif(evtype == 'Ball Receipt*'): readBallReceipt(json,event_match_id)
                elif(evtype == 'Foul Committed'): readFoulCommited(json,event_match_id)
                elif(evtype == 'Interception'): readInterception(json,event_match_id)
                elif(evtype == 'Shot'): readShot(json,event_match_id)
                elif(evtype == 'Substitution'): readSubstitution(json,event_match_id)
                elif(evtype == 'Tactical Shift'): readTacticalShift(json,event_match_id)
                elif(evtype == 'Starting XI'): readStartingXI(json,event_match_id)
                elif(evtype == '50/50'): read5050(json,event_match_id)

                """
                #if(evtype == 'Goal Keeper'): readGoalkeeper(json,event_match_id)
                if(evtype == 'Duel'): readDuel(json,event_match_id)
                elif(evtype == 'Dribble'): readDribble(json,event_match_id)
                else:
                    pass
    """           
    for d in data:
        event_match_id=d[0]['match_id']
        if  db.session.query(Match).filter(Match.match_id == event_match_id).first():
            for json in d:
                ev_id=json['id']
                if  db.session.query(Event).filter(Event.event_id == ev_id).count() == 0:
                    evtype=json['type']['name']
                    #
                    if(evtype == 'Pass'): readPass(json,event_match_id)
                    elif(evtype == 'Carry'): readCarry(json,event_match_id)
                    elif(evtype == 'Pressure'): readPressure(json,event_match_id)
                    elif(evtype == 'Ball Recovery'): readBallRecovery(json,event_match_id)
                    elif(evtype == 'Duel'): readDuel(json,event_match_id)
                    elif(evtype == 'Clearance'): readClearance(json,event_match_id)
                    elif(evtype == 'Dribble'): readDribble(json,event_match_id)
                    elif(evtype == 'Block'): readBlock(json,event_match_id)
                    elif(evtype == 'Dribbled Past'): readDribbledPast(json,event_match_id)
                    elif(evtype == 'Miscontrol'): readMiscontrol(json,event_match_id)
                    #
                    #if(evtype == 'Goal Keeper'): readGoalkeeper(json,event_match_id)

                    if(evtype == 'Foul Won'): readFoulWon(json,event_match_id)
                    elif(evtype == 'Ball Receipt*'): readBallReceipt(json,event_match_id)
                    elif(evtype == 'Foul Committed'): readFoulCommited(json,event_match_id)
                    elif(evtype == 'Interception'): readInterception(json,event_match_id)
                    else:
                     pass
                    #
                    else:
                        index=json['index']
                        period=json['period']
                        timestamp=json['timestamp']
                        minute=json['minute']
                        second=json['second']
                        event_posession=None
                        event_posession_team=None
                        event_play_pattern=None
                        event_team_id=None
                        event_player_id=None
                        event_position_id=None
                        event_location_x=None
                        event_location_y=None
                        event_duration=None
                        event_under_pressure=None
                        event_off_camera=None
                        event_out=None
                        new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
                        db.session.add(new_ev)
                    #
                else:
                     pass
    """
# Read JSON
event_data=list()

def readData():
    # Event
    #events=os.listdir("open-data-master/data/events")
    #path="open-data-master/data/events/"
    events=os.listdir("../a")
    path="../a/"
    for e in events:
        print(e)
        with open(path+e,encoding="utf-8") as f:
            current_data= json.load(f)
        n = e[:e.find('.')]
        current_data[0]['match_id'] = n
        
        for a in current_data:
            evtype=a['type']['name']
            a['match_id']=n
            if evtype == 'Dribble':
                event_data.append(a)
            if evtype == 'Duel':
                event_data.append(a)
            """
            if evtype == 'Pass' or evtype == 'Carry':
            #if  evtype == 'Shot' or evtype == 'Substitution' or evtype == 'Tactical Shift':
                a['match_id']=n
                if  db.session.query(Event).filter(Event.event_id == a['id']).count() == 0:
                    event_data.append(a)
        """
        #event_data.append(current_data)
        
        #Completed: Foul Won,Committed,Interception, Ball Receipt,substitution,Tactical shift,Shot,starting,GoalKeeper,Pass,Carry,Pressure,BALL RECEIPT,ball recovery
readData() 
print("leido")
readEvent(event_data)
#readEvent(event_data)