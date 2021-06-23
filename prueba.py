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
                new_ev=Event(ev_id,event_match_id,index,period,timestamp,minute,second,evtype,event_posession,event_posession_team,event_play_pattern,event_team_id,event_player_id,event_location_x,event_location_y,event_duration,event_under_pressure,event_off_camera,event_out)
                db.session.add(new_ev)
                db.session.commit()
                #if 'related_events' in json:
                #    readEventRelated(ev_id,json['related_events'])
#el bueno                
def readEvent(data):
    for d in data:
        event_match_id=d[0]['match_id']
        if  db.session.query(Match).filter(Match.match_id == event_match_id).first():
            for json in d:
                ev_id=json['id']
                if  db.session.query(Event).filter(Event.event_id == ev_id).count() == 0:
                    evtype=json['type']['name']
                    """
                    if(evtype == 'Pass'): readPass(json,event_match_id)
                    elif(evtype == 'Carry'): readCarry(json,event_match_id)
                    elif(evtype == 'Ball Receipt'): readBallReceipt(json,event_match_id)
                    elif(evtype == 'Pressure'): readPressure(json,event_match_id)
                    elif(evtype == 'Ball Recovery'): readBallRecovery(json,event_match_id)
                    elif(evtype == 'Duel'): readDuel(json,event_match_id)
                    elif(evtype == 'Clearance'): readClearance(json,event_match_id)
                    elif(evtype == 'Dribble'): readDribble(json,event_match_id)
                    elif(evtype == 'Block'): readBlock(json,event_match_id)
                    elif(evtype == 'Dribbled Past'): readDribbledPast(json,event_match_id)
                    """
                    
                    if(evtype == 'Goal Keeper'): readGoalkeeper(json,event_match_id)
                    elif(evtype == 'Miscontrol'): readMiscontrol(json,event_match_id)
                    elif(evtype == 'Foul Commited'): readFoulCommited(json,event_match_id)
                    
                    
                else:
                     pass
                """
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
                """

## para leer eventos concretos
def readEvent(data):

    for json in data:
        event_match_id=json['match_id']
        if  db.session.query(Match).filter(Match.match_id == event_match_id).first():
            ev_id=json['id']
            if  db.session.query(Event).filter(Event.event_id == ev_id).count() == 0:
                evtype=json['type']['name']
                #"""
                if(evtype == 'Pass'): readPass(json,event_match_id)
                elif(evtype == 'Carry'): readCarry(json,event_match_id)
                elif(evtype == 'Ball Receipt'): readBallReceipt(json,event_match_id)
                elif(evtype == 'Pressure'): readPressure(json,event_match_id)
                elif(evtype == 'Ball Recovery'): readBallRecovery(json,event_match_id)
                elif(evtype == 'Duel'): readDuel(json,event_match_id)
                elif(evtype == 'Clearance'): readClearance(json,event_match_id)
                elif(evtype == 'Dribble'): readDribble(json,event_match_id)
                elif(evtype == 'Block'): readBlock(json,event_match_id)
                elif(evtype == 'Dribbled Past'): readDribbledPast(json,event_match_id)
                elif(evtype == 'Miscontrol'): readMiscontrol(json,event_match_id)
                elif(evtype == 'Foul Committed'): readFoulCommited(json,event_match_id)
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
               
                #"""
                """   
                if(evtype == 'Goal Keeper'): readGoalkeeper(json,event_match_id)
                if(evtype == 'Foul Won'): readFoulWon(json,event_match_id)
                elif(evtype == 'Shot'): readShot(json,event_match_id)
                elif(evtype == 'Interception'): readInterception(json,event_match_id)
                """     

            else:
                pass
               


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
#readCompetition(competition_data)
#readMatch1(match_data) #managers,referee,stadium
#readMatchTeam(match_data) #teams
#readLineupPlayer(lineup_data) #players
#readMatch(match_data) #matchs
#readLineup(lineup_data) #lineups
readEvent(event_data)#events
print("All read")