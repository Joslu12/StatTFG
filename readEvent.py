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
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Pass Details
    ev_recipient_id=json['pass']['recipient']['id']
    ev_length=json['pass']['length']
    ev_angle=json['pass']['angle']
    ev_height=json['pass']['height']['name']
    ev_end_loc_x=json['pass']['end_location'][0]
    ev_end_loc_y=json['pass']['end_location'][1]
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
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
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
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # BallReceipt Details
    ev_outcome=None
    # Optional
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
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
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
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # BallRecovery Details
    ev_offensive=None
    ev_recovery=None
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
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    # Optional
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
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
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Clearance Details
    ev_aerial_won=None
    ev_body_part=None
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
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Dribble Dedtails
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
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
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
    event_player_id=json['player']['id']
    event_position_id=json['position']['id']
    event_location_x=json['location'][0]
    event_location_y=json['location'][1]
    event_duration=json['duration']
    event_under_pressure=None
    event_off_camera=None
    event_out=None
    if 'under_pressure' in json:
        event_under_pressure= 1
    # Insert Event
    new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_position_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
    db.session.add(new_ev)
    db.session.commit()
    if 'related_events' in json:
        readEventRelated(ev_id,json['related_events'])
    # Goalkeeper Details
    ev_outcome=None
    ev_technique=None
    ev_position=None
    ev_body_part=None
    ev_type=json['goalkeeper']['type']['name']
    if 'outcome' in json['goalkeeper']:
        ev_outcome=json['goalkeeper']['outcome']['name']
    if 'technique' in json['goalkeeper']:
        ev_technique=json['goalkeeper']['technique']['name']
    if 'position' in json['goalkeeper']
        ev_position=json['goalkeeper']['position']['name']
    if 'body_part' in json['goalkeeper']:
        ev_body_part=json['goalkeeper']['body_part']['name']
    new_gk=EvGoalkeeper(ev_id,ev_outcome,ev_technique,ev_position,ev_body_part,ev_type)
    db.session.add(new_gk)
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
                print(ev_id)
                if not db.session.query(Event).filter(Event.event_id == ev_id).first():
                    evtype=json['type']['name']
                    if(evtype == 'Pass'): readPass(json,event_match_id)
                    elif(evtype == 'Carry'): readCarry(json,event_match_id)
                    elif(evtype == 'Ball Receipt'): readBallReceipt(json,event_match_id)
                    elif(evtype == 'Pressure'): readPressure(json,event_match_id)
                    elif(evtype == 'Ball Recovery'): readBallRecovery(json,event_match_id)
                    elif(evtype == 'Duel'): readDuel(json,event_match_id)
                    elif(evtype == 'Clearance'): readClearance(json,event_match_id)
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
                        db.session.commit()                

# Read JSON
event_data=list()

def readData():
    # Event
    events=os.listdir("open-data-master/data/events")
    path="open-data-master/data/events/"
    for e in events:
        with open(path+e,encoding="utf-8") as f:
            current_data= json.load(f)
        n = e[:e.find('.')]
        current_data[0]['match_id'] = n
        event_data.append(current_data)

readData()
readEvent(event_data)