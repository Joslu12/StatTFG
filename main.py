from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from event_types import *
import os,json
from bson import ObjectId
from flask import render_template,redirect, url_for, send_from_directory, session
from datetime import datetime
from werkzeug.utils import secure_filename 
from requests import NullHandler, Session
from jinja2 import Template
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import decimal
import math
import io
import base64
#import plotly
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly.io as pio
import matplotlib.image as mpimg 
from  matplotlib.colors import LinearSegmentedColormap
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

@app.route('/', methods=['GET','POST'])
def default():
    if request.method == 'GET':
        pl=db.session.execute(f"SELECT DISTINCT p.player_nickname FROM `player`p JOIN evstartingxi e ON p.player_id=e.ev_player_id JOIN team t ON t.team_id=e.ev_team_id WHERE e.ev_team_id=217 GROUP BY e.ev_player_id ORDER BY COUNT(*) DESC").fetchall()      
        players=list()
        for p in pl:
            players.append(p[0])
        return render_template('index.html',players=players)
    else:
        search = request.form['busqueda']
        pi = db.session.execute(f"SELECT DISTINCT p.player_id FROM `player`p JOIN evstartingxi e ON p.player_id=e.ev_player_id JOIN team t ON t.team_id=e.ev_team_id WHERE t.team_id=217 and (p.player_name LIKE '%{search}%' or p.player_nickname LIKE '%{search}%') GROUP BY e.ev_player_id ORDER BY COUNT(*) DESC").fetchall()
        if(len(pi)>1):
            pid=pi[0][0]
        if(len(pi)==0):
            pid=None
        else:
            pid=pi[0][0]
        print(pid)
        if(search != '' and pid != None):
            seasonlistj=db.session.execute(f"SELECT DISTINCT c.competition_season_id AS season_id, c.competition_season_name AS season_name from competition c join `match` m on m.match_season_id=c.competition_season_id join evstartingxi e on e.ev_match_id=m.match_id where e.ev_player_id={pid} ORDER BY season_name DESC").fetchall(),
            seasonlist=seasonlistj[0]
            season= request.form.get('seasonl')
            match=request.form.get('matchl')
            seasonname="Temporada"
            matchname="Partido"
            avgj=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE a.avgstat_player_id={pid} AND a.avgstat_season_id = 0 ").first()
            return render_template(
                'index.html',busqueda=search,seasonlist=seasonlist, season=season, seasonname=seasonname, matchname=matchname,match=match,#chartH=chartH,
            avgj=avgj,
        )
        else:
            return render_template('index.html',busqueda=search,fail="No hay resultados para la búsqueda")

@app.route('/listado', methods=['GET', 'POST'])  
def lista():
    if request.method == 'GET':
        players=db.session.execute(f"SELECT DISTINCT p.player_id, p.player_nickname, p.player_photo, e.ev_position_id as position FROM `player`p JOIN evstartingxi e ON p.player_id=e.ev_player_id JOIN team t ON t.team_id=e.ev_team_id WHERE e.ev_team_id=217 GROUP BY p.player_id ORDER By e.ev_position_id").fetchall()
        gk=list()
        df=list()
        mc=list()
        dc=list()
        for p in players:
            if p.position == 1:
                gk.append(p)
            if p.position >=2 and p.position<=8:
                df.append(p)
            if p.position>=9 and p.position<=16:
                mc.append(p)
            if p.position>=17:
                dc.append(p)
        return render_template("listado.html",gk=gk,df=df,mc=mc,dc=dc)

@app.route('/jugador/<pid>', methods=['GET', 'POST'])  
def playerroute(pid):
    if request.method == 'GET':  
        playername= db.session.execute(f"SELECT p.player_name from player p where p.player_id = {pid}").first()
        seasonlistj=db.session.execute(f"SELECT DISTINCT c.competition_season_id AS season_id, c.competition_season_name AS season_name from competition c join `match` m on m.match_season_id=c.competition_season_id join evstartingxi e on e.ev_match_id=m.match_id where e.ev_player_id={pid} ORDER BY season_name DESC").fetchall(),
        seasonlist=seasonlistj[0]
        seasonname="Temporada"
        matchname="Partido"
        return render_template( 
                'index.html',busqueda=playername[0],seasonlist=seasonlist,
                seasonname=seasonname, matchname=matchname,
            avgj=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE  p.player_id={pid} AND a.avgstat_season_id = 0 ").first()
        )
    else:
        search = request.form['busqueda']
        pid = db.session.execute(f"SELECT p.player_id FROM  player p WHERE  (p.player_name LIKE '%{search}%' or p.player_nickname LIKE '%{search}%')").first()
        seasonlistj=db.session.execute(f"SELECT DISTINCT c.competition_season_id AS season_id, c.competition_season_name AS season_name from competition c join `match` m on m.match_season_id=c.competition_season_id join evstartingxi e on e.ev_match_id=m.match_id where e.ev_player_id={pid[0]} ORDER BY season_name DESC").fetchall(),
        seasonlist=seasonlistj[0]
        season= request.form.get('seasonl')
        match=request.form.get('matchl')
        seasonname="Temporada"
        matchname="Partido"

        if not season:
            season = "0"   
        if not match:
            match = "0"
        if season != 0 and season != "0":
            seasonname=db.session.execute(f"SELECT DISTINCT c.competition_season_name AS season_name from competition c where c.competition_season_id={season}").first()[0],
        if match != 0 and match != "0":
            matchname=db.session.execute(f"SELECT t1.team_name as home, t2.team_name from `match` m join team t1 on m.match_home_team_id=t1.team_id join team t2 on t2.team_id=m.match_away_team_id where m.match_id={match}")
        return render_template(
            'index.html',busqueda=search,seasonlist=seasonlist, season=season, seasonname=seasonname, matchname=matchname,match=match,
        avgj=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE  (p.player_name LIKE '%{search}%' or p.player_nickname LIKE '%{search}%') AND a.avgstat_season_id = 0 ").first(),
       )
  
@app.route('/comparativa', methods=['GET', 'POST'])  
def comparativa():
    if request.method == 'GET':
        return render_template("comparativa.html")
    else:
        p1= request.form['p1']
        p2=request.form['p2']
        pi1 = db.session.execute(f"SELECT DISTINCT p.player_id FROM `player`p JOIN evstartingxi e ON p.player_id=e.ev_player_id JOIN team t ON t.team_id=e.ev_team_id WHERE t.team_id=217 and (p.player_name LIKE '%{p1}%' or p.player_nickname LIKE '%{p1}%') GROUP BY e.ev_player_id ORDER BY COUNT(*) DESC").fetchall()
        pi2 = db.session.execute(f"SELECT DISTINCT p.player_id FROM `player`p JOIN evstartingxi e ON p.player_id=e.ev_player_id JOIN team t ON t.team_id=e.ev_team_id WHERE t.team_id=217 and (p.player_name LIKE '%{p2}%' or p.player_nickname LIKE '%{p2}%') GROUP BY e.ev_player_id ORDER BY COUNT(*) DESC").fetchall()

        if(pi1 == [] or pi2 == [] or  p1 == '' or p2 == ''):
            return render_template('comparativa.html',p1=p1,p2=p2,fail="No hay resultados para la busqueda")
        if(len(pi1)>1):
            pid1=pi1[0][0]
        else:
            pid1=pi1[0][0]
        if(len(pi2)>1):
            pid2=pi2[0][0]
        else:
            pid2=pi2[0][0]
        print(pid1)
        print(pid2)
        avgj1=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE p.player_id = {pid1} AND a.avgstat_season_id = 0 ").first()
        avgj2=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE p.player_id = {pid2} AND a.avgstat_season_id = 0 ").first()
        photo1=db.session.execute(f"SELECT p.player_photo FROM  player p  WHERE p.player_id = {pid1}").first()
        photo2=db.session.execute(f"SELECT p.player_photo FROM  player p  WHERE p.player_id = {pid2}").first()
        print(photo1)
        seasonlistj1=db.session.execute(f"SELECT DISTINCT c.competition_season_id AS season_id, c.competition_season_name AS season_name from competition c join `match` m on m.match_season_id=c.competition_season_id join evstartingxi e on e.ev_match_id=m.match_id where e.ev_player_id={pid1} GROUP BY e.ev_player_id ORDER BY COUNT(*) DESC").fetchall(),
        seasonlist1=seasonlistj1[0]
        seasonlistj2=db.session.execute(f"SELECT DISTINCT c.competition_season_id AS season_id, c.competition_season_name AS season_name from competition c join `match` m on m.match_season_id=c.competition_season_id join evstartingxi e on e.ev_match_id=m.match_id where e.ev_player_id={pid2} GROUP BY e.ev_player_id ORDER BY COUNT(*) DESC").fetchall(),
        seasonlist2=seasonlistj2[0]
        print(Path("static/"+str(pid1)+"VS"+str(pid2)+".png").is_file(),datetime.now())
        """
        if (Path("static/"+str(pid1)+"VS"+str(pid2)+".png").is_file()):
            img=mpimg.imread("static/"+str(pid1)+"VS"+str(pid2)+".png")
            s = base64.b64encode(img).decode("utf-8").replace("\n", "")
            chart= "data:image/png;base64,%s"%s
        else:
        """
        chart=drawChartComparative(pid1,pid2)
        
        if Path("static/"+str(pid1)+"heatmapS"+str(seasonlist1[0].season_id)+".png").is_file():
            img_array=plt.imread("static/"+str(pid1)+"heatmapS"+str(seasonlist1[0].season_id)+".png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            charts1= "data:image/png;base64,%s"%s
        else:
            charts1=drawHeatMapSeason(pid1,seasonlist1[0].season_id)
        if Path("static/"+str(pid2)+"heatmapS"+str(seasonlist2[0].season_id)+".png").is_file():
            img_array=plt.imread("static/"+str(pid2)+"heatmapS"+str(seasonlist2[0].season_id)+".png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            charts2= "data:image/png;base64,%s"%s
        else:
            charts2=drawHeatMapSeason(pid2,seasonlist2[0].season_id)

        if Path("static/"+str(pid1)+"shotH.png").is_file():
            img_array=plt.imread("static/"+str(pid1)+"shotH.png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            shots1= "data:image/png;base64,%s"%s
        else:
            shots1=drawShotsHistoric(pid1)

        if Path("static/"+str(pid2)+"shotH.png").is_file():
            img_array=plt.imread("static/"+str(pid2)+"shotH.png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            shots2= "data:image/png;base64,%s"%s
        else:
            shots2=drawShotsHistoric(pid2)
            
        return render_template("comparativa.html",p1=p1,p2=p2,chart=chart,photo1=photo1[0],photo2=photo2[0],avgj1=avgj1,avgj2=avgj2,charts1=charts1,charts2=charts2,shots1=shots1,shots2=shots2
        )
 
@app.route('/season', methods=['GET', 'POST'])             
def ajaxs():
    if request.method == "POST":
        search_term = request.form
        season = search_term["value"]
        search = search_term["pid"]
        seasonname=db.session.execute(f"SELECT DISTINCT c.competition_season_name AS season_name from competition c where c.competition_season_id={season}").first()[0]
        pid = db.session.execute(f"SELECT p.player_id FROM  player p WHERE  (p.player_name LIKE '%{search}%' or p.player_nickname LIKE '%{search}%')").first()
        avgj=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE  p.player_id = {pid[0]} AND a.avgstat_season_id = 0 ").first()
        avgjs=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE  p.player_id= {pid[0]} AND a.avgstat_season_id = {season} ").first(),
        datos_modificados = db.session.execute(f"SELECT m.match_id, t1.team_name as home, t2.team_name as away from `match` m join team t1 on m.match_home_team_id=t1.team_id join team t2 on t2.team_id=m.match_away_team_id where m.match_season_id={season} and (m.match_home_team_id=217 or m.match_away_team_id=217)").fetchall()
        if (Path("static/"+str(pid)+"HS"+str(season)+".png").is_file()):
            img=mpimg.imread("static/"+str(pid)+"match"+str(season)+".png")
            s = base64.b64encode(img).decode("utf-8").replace("\n", "")
            chartS= "data:image/png;base64,%s"%s
        else:
            chartS=drawChartH(pid[0],season)
        
        return jsonify(select=render_template("match.html", matchs=datos_modificados), tablas= render_template('tablas.html',#"tablas.html",
        season=season, avgj=avgj,seasonname=seasonname, avgjs=avgjs[0] ), charts=render_template("charts.html",chartS=chartS)) 

@app.route('/match', methods=['GET', 'POST'])             
def ajaxm():
    if request.method == "POST":
        search_term = request.form
        season = search_term["season"]
        match = search_term["value"]
        print(match)
        search = search_term["pid"]
        seasonname=db.session.execute(f"SELECT DISTINCT c.competition_season_name AS season_name from competition c where c.competition_season_id={season}").first()[0]
        pid = db.session.execute(f"SELECT p.player_id FROM  player p WHERE  (p.player_name LIKE '%{search}%' or p.player_nickname LIKE '%{search}%')").first()
        avgj=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE  p.player_id = {pid[0]} AND a.avgstat_season_id = 0 ").first()
        avgjs=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE  p.player_id= {pid[0]} AND a.avgstat_season_id = {season} ").first(),
        datos_modificados = db.session.execute(f"SELECT m.match_id, t1.team_name as home, t2.team_name as away from `match` m join team t1 on m.match_home_team_id=t1.team_id join team t2 on t2.team_id=m.match_away_team_id where m.match_season_id={season} and (m.match_home_team_id=217 or m.match_away_team_id=217) ORDER BY m.match_id").fetchall()
        passes=db.session.execute(f"SELECT COUNT(*) as Total, SUM(CASE WHEN (p.ev_outcome IS NULL) THEN 1 ELSE 0 END) AS Good,SUM(CASE WHEN (p.ev_outcome='Incomplete') THEN 1 ELSE 0 END) AS Incomplete,SUM(CASE WHEN (p.ev_cross='1') THEN 1 ELSE 0 END) AS Cros,SUM(CASE WHEN (p.ev_goal_assist='1') THEN 1 ELSE 0 END) AS Asistencia FROM event e JOIN evpass p ON e.event_id=p.ev_id JOIN `match` m ON e.event_match_id=m.match_id  WHERE e.event_player_id = {pid[0]} AND m.match_id = {match}").first(),
        shots=db.session.execute(f"SELECT COUNT(*) as Total, SUM(CASE WHEN (p.ev_outcome= 'Goal') THEN 1 ELSE 0 END) AS Good, SUM(CASE WHEN (p.ev_outcome= 'Off T') THEN 1 ELSE 0 END) AS Off FROM event e JOIN evshot p ON e.event_id=p.ev_id JOIN `match` m ON e.event_match_id=m.match_id WHERE e.event_player_id = {pid[0]} AND m.match_id = {match}").first(),
        dribbles= db.session.execute(f"SELECT COUNT(*) as Total, SUM(CASE WHEN (p.ev_outcome = 'Complete') THEN 1 ELSE 0 END) AS Good FROM event e JOIN evdribble p ON e.event_id=p.ev_id  JOIN `match` m ON e.event_match_id=m.match_id  WHERE e.event_player_id = {pid[0]} AND m.match_id = {match} ").first(),
        recoveries= db.session.execute(f"SELECT COUNT(*) as Total FROM event e JOIN evballrecovery p ON e.event_id=p.ev_id  JOIN `match` m ON e.event_match_id=m.match_id  WHERE e.event_player_id = {pid[0]} AND m.match_id = {match}").first(),
        carry = db.session.execute(f"SELECT COUNT(*) as Total, ABS(e.event_location_x-p.ev_end_loc_x)+ABS(e.event_location_y-p.ev_end_loc_y) as Distancia FROM event e JOIN evcarry p ON e.event_id=p.ev_id  JOIN `match` m ON e.event_match_id=m.match_id  WHERE e.event_player_id = {pid[0]} AND m.match_id = {match} ").first(),
        matchname=db.session.execute(f"SELECT t1.team_name as home, t2.team_name as away from `match` m join team t1 on m.match_home_team_id=t1.team_id join team t2 on t2.team_id=m.match_away_team_id where m.match_id={match}").first()
        if (Path("static/"+str(pid)+"match"+str(match)+".png").is_file()):
            img=mpimg.imread("static/"+str(pid)+"match"+str(match)+".png")
            s = base64.b64encode(img).decode("utf-8").replace("\n", "")
            chartM= "data:image/png;base64,%s"%s
        else:
            chartM=drawChartM(pid,season,match)
        
        pases=checkSQL(passes)
        return jsonify(tablam = render_template("tablam.html",season=season, avgj=avgj, avgjs=avgjs[0],matchs=datos_modificados,matchname=matchname,seasonname=seasonname,
        passes=pases,shots=shots[0],dribbles=dribbles[0],recoveries=recoveries[0],carry=carry[0]), matchChart=render_template("matchChart.html",chartM=chartM),wait=render_template("wait.html"))

@app.route('/chart', methods=['GET', 'POST'])             
def loadChart():
    if request.method == "POST":
        search_term = request.form
        season = search_term["season"]
        match = search_term["value"]
        print(match)
        search = search_term["pid"]
        pid = db.session.execute(f"SELECT p.player_id FROM  player p WHERE  (p.player_name LIKE '%{search}%' or p.player_nickname LIKE '%{search}%')").first()

        if Path("static/"+str(pid[0])+"heatmapM"+str(match)+".png").is_file():
            img_array=plt.imread("static/"+str(pid[0])+"heatmapM"+str(match)+".png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            heatMapM= "data:image/png;base64,%s"%s
        else:
            heatMapM=drawHeatMap(pid,match)
        
        if Path("static/"+str(pid[0])+"heatmapS"+str(season)+".png").is_file():
            img_array=plt.imread("static/"+str(pid[0])+"heatmapS"+str(season)+".png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            heatMapS= "data:image/png;base64,%s"%s
        else:
            heatMapS=drawHeatMapSeason(pid[0],season)
        if Path("static/"+str(pid[0])+"shotM"+str(match)+".png").is_file():
            img_array=plt.imread("static/"+str(pid[0])+"shotM"+str(match)+".png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            goal= "data:image/png;base64,%s"%s
        else:
            goal=drawShots(pid[0],match)
        if Path("static/"+str(pid[0])+"shotS"+str(season)+".png").is_file():
            img_array=plt.imread("static/"+str(pid[0])+"shotS"+str(season)+".png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            goals= "data:image/png;base64,%s"%s
        else:
            goals=drawShotsSeason(pid[0],season)
        if Path("static/"+str(pid[0])+"actionM"+str(match)+".png").is_file():
            img_array=plt.imread("static/"+str(pid[0])+"actionM"+str(match)+".png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            action= "data:image/png;base64,%s"%s
        else:
            action=drawActionMap(pid[0],match)
        if Path("static/"+str(pid[0])+"actionS"+str(season)+".png").is_file():
            img_array=plt.imread("static/"+str(pid[0])+"actionS"+str(season)+".png") 
            plt.imshow(img_array)
            plt.axis('off')
            s = io.BytesIO()
            plt.savefig(s, format='png', bbox_inches="tight")
            plt.close()
            s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
            actions= "data:image/png;base64,%s"%s
        else:
            actions=drawActionMapSeason(pid[0],season)
        
        return render_template("chartm.html", heatMapS=heatMapS,goal=goal,action=action,actions=actions,goals=goals,heatMapM=heatMapM, 
        )

#Métodos de calculo
def drawChartH(pid,season):
    categories = ['Pases Intentados', 'Pases acertados', 'Goles', 'Asistencias', 'Tiros','Regates intentados', 'Regates acertados']
    avgj=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE p.player_id = {pid} AND a.avgstat_season_id = 0 ").first()
    avgjs=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE p.player_id = {pid} AND a.avgstat_season_id = {season} ").first() 
    maxj=[bigger(avgj.avgstat_pas,avgjs.avgstat_pas),bigger(avgj.avgstat_goodpass,avgjs.avgstat_goodpass),bigger(avgj.avgstat_goal,avgjs.avgstat_goal),bigger(avgj.avgstat_goalassist,avgjs.avgstat_goalassist),bigger(avgj.avgstat_shot,avgjs.avgstat_shot),bigger(avgj.avgstat_dribbles,avgjs.avgstat_dribbles),bigger(avgj.avgstat_gooddribbles,avgjs.avgstat_gooddribbles)]
    categories= [*categories, categories[0]]
    stats = [check(avgj.avgstat_pas,maxj[0],1)*10, check(avgj.avgstat_goodpass,maxj[1],1)*10, check(avgj.avgstat_goal,maxj[2],1)*10, check(avgj.avgstat_goalassist,maxj[3],1)*10, check(avgj.avgstat_shot,maxj[4],1)*10,check(avgj.avgstat_dribbles,maxj[5],1)*10,check(avgj.avgstat_gooddribbles,maxj[6],1)*10]
    stats= [*stats,stats[0]]
    stats1 = [check(avgjs.avgstat_pas,maxj[0],1)*10, check(avgjs.avgstat_goodpass,maxj[1],1)*10, check(avgjs.avgstat_goal,maxj[2],1)*10, check(avgjs.avgstat_goalassist,maxj[3],1)*10, check(avgjs.avgstat_shot,maxj[4],1)*10,check(avgjs.avgstat_dribbles,maxj[5],1)*10,check(avgjs.avgstat_gooddribbles,maxj[6],1)*10]
    stats1= [*stats1,stats1[0]]
    fig = go.Figure(
        data=[go.Scatterpolar(r=stats, theta=categories, fill='toself',name='Historico'),
        go.Scatterpolar(r=stats1, theta=categories, fill='toself', name='Temporada')],
        layout=go.Layout(
        title=go.layout.Title(text=''),
        polar={'radialaxis': {'visible': False}},
        showlegend=True,
        font_color="white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )
    )
    fig.update_layout(legend = dict(bgcolor = 'black'))
    img_bytes=fig.to_image(format="png", engine="kaleido")
    fig.write_image("static/"+str(pid)+"HS"+str(season)+".png")
    s = base64.b64encode(img_bytes).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s
    
    #fig.write_image( "static/"+str(pid)+"chartS"+str(season)+".png")
    
def drawChartM(pid,season,match):
    categories = ['Pases Intentados', 'Pases acertados', 'Goles', 'Asistencias', 'Tiros','Regates intentados', 'Regates acertados']
    passes=db.session.execute(f"SELECT COUNT(*) as Total, SUM(CASE WHEN (p.ev_outcome IS NULL) THEN 1 ELSE 0 END) AS Good,SUM(CASE WHEN (p.ev_outcome='Incomplete') THEN 1 ELSE 0 END) AS Incomplete,SUM(CASE WHEN (p.ev_cross='1') THEN 1 ELSE 0 END) AS Cros,SUM(CASE WHEN (p.ev_goal_assist='1') THEN 1 ELSE 0 END) AS Asistencia FROM event e JOIN evpass p ON e.event_id=p.ev_id JOIN `match` m ON e.event_match_id=m.match_id  WHERE e.event_player_id = {pid[0]} AND m.match_id = {match}").first(),
    shots=db.session.execute(f"SELECT COUNT(*) as Total, SUM(CASE WHEN (p.ev_outcome= 'Goal') THEN 1 ELSE 0 END) AS Good, SUM(CASE WHEN (p.ev_outcome= 'Off T') THEN 1 ELSE 0 END) AS Off FROM event e JOIN evshot p ON e.event_id=p.ev_id JOIN `match` m ON e.event_match_id=m.match_id WHERE e.event_player_id = {pid[0]} AND m.match_id = {match}").first(),
    dribbles= db.session.execute(f"SELECT COUNT(*) as Total, SUM(CASE WHEN (p.ev_outcome = 'Complete') THEN 1 ELSE 0 END) AS Good FROM event e JOIN evdribble p ON e.event_id=p.ev_id  JOIN `match` m ON e.event_match_id=m.match_id  WHERE e.event_player_id = {pid[0]} AND m.match_id = {match} ").first(),
    avgj=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE  p.player_id = {pid[0]} AND a.avgstat_season_id = 0 ").first()
    avgjs=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE p.player_id = {pid[0]} AND a.avgstat_season_id = {season} ").first() 
    maax=[bigger(avgj.avgstat_pas,avgjs.avgstat_pas),bigger(avgj.avgstat_goodpass,avgjs.avgstat_goodpass),bigger(avgj.avgstat_goal,avgjs.avgstat_goal),bigger(avgj.avgstat_goalassist,avgjs.avgstat_goalassist),bigger(avgj.avgstat_shot,avgjs.avgstat_shot),bigger(avgj.avgstat_dribbles,avgjs.avgstat_dribbles),bigger(avgj.avgstat_gooddribbles,avgjs.avgstat_gooddribbles)]
    maxj=[checkNumDen(passes[0].Total,maax[0]), checkNumDen(passes[0].Good,maax[1]), checkNumDen(shots[0].Good,maax[2]), checkNumDen(passes[0].Asistencia,maax[3]), checkNumDen(shots[0].Total,maax[4]),checkNumDen(dribbles[0].Total,maax[5]),checkNumDen(dribbles[0].Good,maax[6])]
    categories= [*categories, categories[0]]
    stats = [avgj.avgstat_pas/maxj[0], avgj.avgstat_goodpass/maxj[1], avgj.avgstat_goal/maxj[2], avgj.avgstat_goalassist/maxj[3], avgj.avgstat_shot/maxj[4],avgj.avgstat_dribbles/maxj[5],avgj.avgstat_gooddribbles/maxj[6]]
    stats= [*stats,stats[0]]
    stats1 =[avgjs.avgstat_pas/maxj[0], avgjs.avgstat_goodpass/maxj[1], avgjs.avgstat_goal/maxj[2], avgjs.avgstat_goalassist/maxj[3], avgjs.avgstat_shot/maxj[4],avgjs.avgstat_dribbles/maxj[5],avgjs.avgstat_gooddribbles/maxj[6]]
    stats1= [*stats1,stats1[0]]
    stats2 = [check1(passes[0].Total)/maxj[0], check1(passes[0].Good)/maxj[1], check1(shots[0].Good)/maxj[2], check1(passes[0].Asistencia)/maxj[3], check1(shots[0].Total)/maxj[4],check1(dribbles[0].Total)/maxj[5],check1(dribbles[0].Good)/maxj[6]]
    stats2= [*stats2,stats2[0]]


    fig = go.Figure(
        data=[go.Scatterpolar(r=stats, theta=categories, fill='toself',name='Historico'),
        go.Scatterpolar(r=stats1, theta=categories, fill='toself', name='Temporada'),
        go.Scatterpolar(r=stats2, theta=categories, fill='toself',name='Partido')],
        layout=go.Layout(
        title=go.layout.Title(text=''),
        polar={'radialaxis': {'visible': False}},
        showlegend=True,
        font_color="white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )
    )
    fig.update_layout(legend = dict(bgcolor = 'black'))
    img_bytes=fig.to_image(format="png", engine="kaleido")
    fig.write_image("static/"+str(pid[0])+"match"+str(match)+".png")
    s = base64.b64encode(img_bytes).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s
   
def drawChartComparative(p1,p2):
    categories = ['Pases Intentados', 'Pases acertados', 'Goles', 'Asistencias', 'Tiros','Regates intentados', 'Regates acertados']
    avgj1=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE p.player_id = {p1} AND a.avgstat_season_id = 0 ").first()
    avgj2=db.session.execute(f"SELECT * FROM avgstat a JOIN player p ON a.avgstat_player_id=p.player_id WHERE p.player_id = {p2} AND a.avgstat_season_id = 0 ").first()
    maxj3=[bigger(avgj1.avgstat_pas,avgj2.avgstat_pas),bigger(avgj1.avgstat_goodpass,avgj2.avgstat_goodpass),bigger(avgj1.avgstat_goal,avgj2.avgstat_goal),bigger(avgj1.avgstat_goalassist,avgj2.avgstat_goalassist),bigger(avgj1.avgstat_shot,avgj2.avgstat_shot),bigger(avgj1.avgstat_dribbles,avgj2.avgstat_dribbles),bigger(avgj1.avgstat_gooddribbles,avgj2.avgstat_gooddribbles)]
    playername1= db.session.execute(f"SELECT p.player_nickname from player p where p.player_id = {p1}").first()
    playername2= db.session.execute(f"SELECT p.player_nickname from player p where p.player_id = {p2}").first()

    categories= [*categories, categories[0]]
    stats1 = [check(avgj1.avgstat_pas,maxj3[0],1)*10, check(avgj1.avgstat_goodpass,maxj3[1],1)*10, check(avgj1.avgstat_goal,maxj3[2],1)*10, check(avgj1.avgstat_goalassist,maxj3[3],1)*10, check(avgj1.avgstat_shot,maxj3[4],1)*10,check(avgj1.avgstat_dribbles,maxj3[5],1)*10,check(avgj1.avgstat_gooddribbles,maxj3[6],1)*10]
    stats1= [*stats1,stats1[0]]
    stats2 = [check(avgj2.avgstat_pas,maxj3[0],1)*10, check(avgj2.avgstat_goodpass,maxj3[1],1)*10, check(avgj2.avgstat_goal,maxj3[2],1)*10, check(avgj2.avgstat_goalassist,maxj3[3],1)*10, check(avgj2.avgstat_shot,maxj3[4],1)*10,check(avgj2.avgstat_dribbles,maxj3[5],1)*10,check(avgj2.avgstat_gooddribbles,maxj3[6],1)*10]
    stats2= [*stats2,stats2[0]]
    fig = go.Figure(
        data=[go.Scatterpolar(r=stats1, theta=categories, fill='toself', name=playername1[0]),
            go.Scatterpolar(r=stats2, theta=categories, fill='toself', name=playername2[0]),
        ],
        layout=go.Layout(
        title=go.layout.Title(text='Estadisticas Historicas'),
        polar={'radialaxis': {'visible': False}},
        showlegend=True,
        font_color="white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )
    )
    fig.update_layout(legend = dict(bgcolor = 'black'))
    img_bytes=fig.to_image(format="png", engine="kaleido")
    fig.write_image("static/"+str(p1)+"VS"+str(p2)+".png")
    s = base64.b64encode(img_bytes).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s

def drawActionMap(pid,match):
    data = db.session.execute(f"SELECT COUNT(*) total, COUNT(CASE WHEN x>=0 and x<=15 and y>=0 and y<=20 THEN 1 END) as z1, COUNT(CASE WHEN x>=0 and x<=15 and y>=20 and y<=40 THEN 1 END) as z2,COUNT(CASE WHEN x>=0 and x<=15 and y>=40 and y<=60 THEN 1 END) as z3,COUNT(CASE WHEN x>=0 and x<=15 and y>=60 and y<=80 THEN 1 END) as z4, COUNT(CASE WHEN x>=15 and x<=30 and y>=0 and y<=20 THEN 1 END) as z5, COUNT(CASE WHEN x>=15 and x<=30 and y>=20 and y<=40 THEN 1 END) as z6,COUNT(CASE WHEN x>=15 and x<=30 and y>=40 and y<=60 THEN 1 END) as z7,COUNT(CASE WHEN x>=15 and x<=30 and y>=60 and y<=80 THEN 1 END) as z8,COUNT(CASE WHEN x>=30 and x<=45 and y>=0 and y<=20 THEN 1 END) as z9, COUNT(CASE WHEN x>=30 and x<=45 and y>=20 and y<=40 THEN 1 END) as z10,COUNT(CASE WHEN x>=30 and x<=45 and y>=40 and y<=60 THEN 1 END) as z11,COUNT(CASE WHEN x>=30 and x<=45 and y>=60 and y<=80 THEN 1 END) as z12,COUNT(CASE WHEN x>=45 and x<=60 and y>=0 and y<=20 THEN 1 END) as z13, COUNT(CASE WHEN x>=45 and x<=60  and y>=20 and y<=40 THEN 1 END) as z14,COUNT(CASE WHEN x>=45 and x<=60  and y>=40 and y<=60 THEN 1 END) as z15,COUNT(CASE WHEN x>=45 and x<=60  and y>=60 and y<=80 THEN 1 END) as z16,COUNT(CASE WHEN x>=60 and x<=75 and y>=0 and y<=20 THEN 1 END) as z17, COUNT(CASE WHEN x>=60 and x<=75 and y>=20 and y<=40 THEN 1 END) as z18,COUNT(CASE WHEN x>=60 and x<=75 and y>=40 and y<=60 THEN 1 END) as z19,COUNT(CASE WHEN x>=60 and x<=75 and y>=60 and y<=80 THEN 1 END) as z20, COUNT(CASE WHEN x>=75 and x<=90 and y>=0 and y<=20 THEN 1 END) as z21, COUNT(CASE WHEN x>=75 and x<=90 and y>=20 and y<=40 THEN 1 END) as z22,COUNT(CASE WHEN x>=75 and x<=90 and y>=40 and y<=60 THEN 1 END) as z23,COUNT(CASE WHEN x>=75 and x<=90 and y>=60 and y<=80 THEN 1 END) as z24,COUNT(CASE WHEN x>=90 and x<=105 and y>=0 and y<=20 THEN 1 END) as z25, COUNT(CASE WHEN x>=90 and x<=105 and y>=20 and y<=40 THEN 1 END) as z26,COUNT(CASE WHEN x>=90 and x<=105 and y>=40 and y<=60 THEN 1 END) as z27,COUNT(CASE WHEN x>=90 and x<=105 and y>=60 and y<=80 THEN 1 END) as z28,COUNT(CASE WHEN x>=105 and x<=120 and y>=0 and y<=20 THEN 1 END) as z29, COUNT(CASE WHEN x>=105 and x<=120  and y>=20 and y<=40 THEN 1 END) as z30,COUNT(CASE WHEN x>=105 and x<=120  and y>=40 and y<=60 THEN 1 END) as z31,COUNT(CASE WHEN x>=105 and x<=120  and y>=60 and y<=80 THEN 1 END) as z32 FROM (SELECT `event`.`event_location_x` as x,  `event`.`event_location_y` as y  FROM `event` WHERE `event_player_id` = {pid} and `event_match_id` = {match}) AS sq").fetchall()
    zones=[[percentage(data[0].z4,data[0].total),percentage(data[0].z8,data[0].total),percentage(data[0].z12,data[0].total),percentage(data[0].z16,data[0].total),percentage(data[0].z20,data[0].total),percentage(data[0].z24,data[0].total),percentage(data[0].z28,data[0].total),percentage(data[0].z32,data[0].total)],
    [percentage(data[0].z3,data[0].total),percentage(data[0].z7,data[0].total),percentage(data[0].z11,data[0].total),percentage(data[0].z15,data[0].total),percentage(data[0].z19,data[0].total),percentage(data[0].z23,data[0].total),percentage(data[0].z27,data[0].total),percentage(data[0].z31,data[0].total)],
    [percentage(data[0].z2,data[0].total),percentage(data[0].z6,data[0].total),percentage(data[0].z10,data[0].total),percentage(data[0].z14,data[0].total),percentage(data[0].z18,data[0].total),percentage(data[0].z22,data[0].total),percentage(data[0].z26,data[0].total),percentage(data[0].z30,data[0].total)],
    [percentage(data[0].z1,data[0].total),percentage(data[0].z5,data[0].total),percentage(data[0].z9,data[0].total),percentage(data[0].z13,data[0].total),percentage(data[0].z17,data[0].total),percentage(data[0].z21,data[0].total),percentage(data[0].z25,data[0].total),percentage(data[0].z29,data[0].total)]]
    #print(zones)
    labels=makeLabels(zones)
    l=["darkgreen","yellow","peru","orange","darkred"]
    heatmap=sns.heatmap(zones, cbar=False,xticklabels=False, yticklabels=False, annot=labels,fmt="",cmap=LinearSegmentedColormap.from_list('Greens',l, N=256,))
    map_img = mpimg.imread('static/terrenoT.png')
    heatmap.set_title('')
    heatmap.imshow(map_img,
          aspect = heatmap.get_aspect(),
          extent = heatmap.get_xlim() + heatmap.get_ylim(),
          zorder = 1) #put the map under the heatmap
    s = io.BytesIO()
    plt.savefig("static/"+str(pid)+"actionM"+str(match)+".png")    
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s

def drawActionMapSeason(pid,season):
    data = db.session.execute(f"SELECT COUNT(*) as total,COUNT(CASE WHEN x>=0 and x<=15 and y>=0 and y<=20 THEN 1 END) as z1, COUNT(CASE WHEN x>=0 and x<=15 and y>=20 and y<=40 THEN 1 END) as z2,COUNT(CASE WHEN x>=0 and x<=15 and y>=40 and y<=60 THEN 1 END) as z3,COUNT(CASE WHEN x>=0 and x<=15 and y>=60 and y<=80 THEN 1 END) as z4, COUNT(CASE WHEN x>=15 and x<=30 and y>=0 and y<=20 THEN 1 END) as z5, COUNT(CASE WHEN x>=15 and x<=30 and y>=20 and y<=40 THEN 1 END) as z6,COUNT(CASE WHEN x>=15 and x<=30 and y>=40 and y<=60 THEN 1 END) as z7,COUNT(CASE WHEN x>=15 and x<=30 and y>=60 and y<=80 THEN 1 END) as z8,COUNT(CASE WHEN x>=30 and x<=45 and y>=0 and y<=20 THEN 1 END) as z9, COUNT(CASE WHEN x>=30 and x<=45 and y>=20 and y<=40 THEN 1 END) as z10,COUNT(CASE WHEN x>=30 and x<=45 and y>=40 and y<=60 THEN 1 END) as z11,COUNT(CASE WHEN x>=30 and x<=45 and y>=60 and y<=80 THEN 1 END) as z12,COUNT(CASE WHEN x>=45 and x<=60 and y>=0 and y<=20 THEN 1 END) as z13, COUNT(CASE WHEN x>=45 and x<=60  and y>=20 and y<=40 THEN 1 END) as z14,COUNT(CASE WHEN x>=45 and x<=60  and y>=40 and y<=60 THEN 1 END) as z15,COUNT(CASE WHEN x>=45 and x<=60  and y>=60 and y<=80 THEN 1 END) as z16,COUNT(CASE WHEN x>=60 and x<=75 and y>=0 and y<=20 THEN 1 END) as z17, COUNT(CASE WHEN x>=60 and x<=75 and y>=20 and y<=40 THEN 1 END) as z18,COUNT(CASE WHEN x>=60 and x<=75 and y>=40 and y<=60 THEN 1 END) as z19,COUNT(CASE WHEN x>=60 and x<=75 and y>=60 and y<=80 THEN 1 END) as z20, COUNT(CASE WHEN x>=75 and x<=90 and y>=0 and y<=20 THEN 1 END) as z21, COUNT(CASE WHEN x>=75 and x<=90 and y>=20 and y<=40 THEN 1 END) as z22,COUNT(CASE WHEN x>=75 and x<=90 and y>=40 and y<=60 THEN 1 END) as z23,COUNT(CASE WHEN x>=75 and x<=90 and y>=60 and y<=80 THEN 1 END) as z24,COUNT(CASE WHEN x>=90 and x<=105 and y>=0 and y<=20 THEN 1 END) as z25, COUNT(CASE WHEN x>=90 and x<=105 and y>=20 and y<=40 THEN 1 END) as z26,COUNT(CASE WHEN x>=90 and x<=105 and y>=40 and y<=60 THEN 1 END) as z27,COUNT(CASE WHEN x>=90 and x<=105 and y>=60 and y<=80 THEN 1 END) as z28,COUNT(CASE WHEN x>=105 and x<=120 and y>=0 and y<=20 THEN 1 END) as z29, COUNT(CASE WHEN x>=105 and x<=120  and y>=20 and y<=40 THEN 1 END) as z30,COUNT(CASE WHEN x>=105 and x<=120  and y>=40 and y<=60 THEN 1 END) as z31,COUNT(CASE WHEN x>=105 and x<=120  and y>=60 and y<=80 THEN 1 END) as z32 FROM (SELECT  `event`.`event_location_x` as x,  `event`.`event_location_y` as y  FROM `event` JOIN `match` m ON event_match_id=m.match_id JOIN competition c ON c.competition_id=m.match_competition_id AND c.competition_season_id=m.match_season_id WHERE `event_player_id` = {pid} and c.competition_season_id = {season}) AS sq").fetchall()
    zones=[[percentage(data[0].z4,data[0].total),percentage(data[0].z8,data[0].total),percentage(data[0].z12,data[0].total),percentage(data[0].z16,data[0].total),percentage(data[0].z20,data[0].total),percentage(data[0].z24,data[0].total),percentage(data[0].z28,data[0].total),percentage(data[0].z32,data[0].total)],
    [percentage(data[0].z3,data[0].total),percentage(data[0].z7,data[0].total),percentage(data[0].z11,data[0].total),percentage(data[0].z15,data[0].total),percentage(data[0].z19,data[0].total),percentage(data[0].z23,data[0].total),percentage(data[0].z27,data[0].total),percentage(data[0].z31,data[0].total)],
    [percentage(data[0].z2,data[0].total),percentage(data[0].z6,data[0].total),percentage(data[0].z10,data[0].total),percentage(data[0].z14,data[0].total),percentage(data[0].z18,data[0].total),percentage(data[0].z22,data[0].total),percentage(data[0].z26,data[0].total),percentage(data[0].z30,data[0].total)],
    [percentage(data[0].z1,data[0].total),percentage(data[0].z5,data[0].total),percentage(data[0].z9,data[0].total),percentage(data[0].z13,data[0].total),percentage(data[0].z17,data[0].total),percentage(data[0].z21,data[0].total),percentage(data[0].z25,data[0].total),percentage(data[0].z29,data[0].total)]]
    labels=makeLabels(zones)
    l=["darkgreen","yellow","peru","orange","darkred"]
    heatmap=sns.heatmap(zones, cbar=False,xticklabels=False, yticklabels=False, annot=labels,fmt="",cmap=LinearSegmentedColormap.from_list('Greens',l, N=256,))
    map_img = mpimg.imread('static/terrenoT.png')
    heatmap.set_title('')
    heatmap.imshow(map_img,
          aspect = heatmap.get_aspect(),
          extent = heatmap.get_xlim() + heatmap.get_ylim(),
          zorder = 1) #put the map under the heatmap
    
    s = io.BytesIO()
    plt.savefig("static/"+str(pid)+"actionS"+str(season)+".png")
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s
    
    #plt.savefig("static/"+str(pid)+"actionS"+str(season)+".png")

def drawShots(pid,match):
    shots=db.session.execute(f"SELECT COUNT(*) total, COUNT(CASE WHEN y<36 and z>2.67 THEN 1 END) as z1, COUNT(CASE WHEN y>=36 and y<38 and  z>2.67 THEN 1 END) as z2, COUNT(CASE WHEN y>=38 and y<40 and  z>2.67 THEN 1 END) as z3, COUNT(CASE WHEN y>=40 and y<42 and z>2.67 THEN 1 END) as z4,COUNT(CASE WHEN y>=42 and y<=44 and z>2.67 THEN 1 END) as z5, COUNT(CASE WHEN y>44 and z>2.67 THEN 1 END) as z6,COUNT(CASE WHEN y<36 and z>1.33 and z<=2.67 THEN 1 END) as z7, COUNT(CASE WHEN y>=36 and y<38 and z>1.33 and z<=2.67 THEN 1 END) as z8, COUNT(CASE WHEN y>=38 and y<40 and z>1.33 and z<=2.67 THEN 1 END) as z9, COUNT(CASE WHEN y>=40 and y<42 and z>1.33 and z<=2.67 THEN 1 END) as z10,COUNT(CASE WHEN y>=42 and y<=44 and z>1.33 and z<=2.67 THEN 1 END) as z11, COUNT(CASE WHEN y>44 and z>1.33 and z<=2.67 THEN 1 END) as z12,COUNT(CASE WHEN y<36 and z<=1.33 THEN 1 END) as z13, COUNT(CASE WHEN y>=36 and y<38 and z<=1.33 THEN 1 END) as z14, COUNT(CASE WHEN y>=38 and y<40 and z<=1.33  THEN 1 END) as z15, COUNT(CASE WHEN y>=40 and y<42 and z<=1.33 THEN 1 END) as z16,COUNT(CASE WHEN y>=42 and y<=44 and z<=1.33 THEN 1 END) as z17, COUNT(CASE WHEN y>44 and z<=1.33 THEN 1 END) as z18 FROM (SELECT es.ev_end_loc_y as y, es.ev_end_loc_z as z FROM `event`e join `evshot` es ON e.event_id=es.ev_id WHERE e.event_match_id={match} and e.event_type='Shot' and e.event_player_id={pid}) as sq").fetchall()
    data = [[percentage(shots[0].z1,shots[0].total),percentage(shots[0].z2,shots[0].total),percentage(shots[0].z3,shots[0].total),percentage(shots[0].z4,shots[0].total),percentage(shots[0].z5,shots[0].total),percentage(shots[0].z6,shots[0].total)],
    [percentage(shots[0].z7,shots[0].total),percentage(shots[0].z8,shots[0].total),percentage(shots[0].z9,shots[0].total),percentage(shots[0].z10,shots[0].total),percentage(shots[0].z11,shots[0].total),percentage(shots[0].z12,shots[0].total)],
    [percentage(shots[0].z13,shots[0].total),percentage(shots[0].z14,shots[0].total),percentage(shots[0].z15,shots[0].total),percentage(shots[0].z16,shots[0].total),percentage(shots[0].z17,shots[0].total),percentage(shots[0].z18,shots[0].total)]]
    labels=makeLabels(data)
    heatmap=sns.heatmap(data,cbar=False, xticklabels=False, yticklabels=False, annot=labels,fmt="",cmap="binary")
    map_img = mpimg.imread('static/porteriaT.png')
    heatmap.set_title('')
    heatmap.imshow(map_img,
          aspect = heatmap.get_aspect(),
          extent = heatmap.get_xlim() + heatmap.get_ylim(),
          zorder = 1) #put the map under the heatmap
    s = io.BytesIO()
    plt.savefig("static/"+str(pid)+"shotM"+str(match)+".png")
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s

def drawShotsSeason(pid,season):
    shots=db.session.execute(f"SELECT COUNT(*) total, COUNT(CASE WHEN y<36 and z>2.67 THEN 1 END) as z1, COUNT(CASE WHEN y>=36 and y<38 and  z>2.67 THEN 1 END) as z2, COUNT(CASE WHEN y>=38 and y<40 and  z>2.67 THEN 1 END) as z3, COUNT(CASE WHEN y>=40 and y<42 and z>2.67 THEN 1 END) as z4,COUNT(CASE WHEN y>=42 and y<=44 and z>2.67 THEN 1 END) as z5, COUNT(CASE WHEN y>44 and z>2.67 THEN 1 END) as z6,COUNT(CASE WHEN y<36 and z>1.33 and z<=2.67 THEN 1 END) as z7, COUNT(CASE WHEN y>=36 and y<38 and z>1.33 and z<=2.67 THEN 1 END) as z8, COUNT(CASE WHEN y>=38 and y<40 and z>1.33 and z<=2.67 THEN 1 END) as z9, COUNT(CASE WHEN y>=40 and y<42 and z>1.33 and z<=2.67 THEN 1 END) as z10,COUNT(CASE WHEN y>=42 and y<=44 and z>1.33 and z<=2.67 THEN 1 END) as z11, COUNT(CASE WHEN y>44 and z>1.33 and z<=2.67 THEN 1 END) as z12,COUNT(CASE WHEN y<36 and z<=1.33 THEN 1 END) as z13, COUNT(CASE WHEN y>=36 and y<38 and z<=1.33 THEN 1 END) as z14, COUNT(CASE WHEN y>=38 and y<40 and z<=1.33  THEN 1 END) as z15, COUNT(CASE WHEN y>=40 and y<42 and z<=1.33 THEN 1 END) as z16,COUNT(CASE WHEN y>=42 and y<=44 and z<=1.33 THEN 1 END) as z17, COUNT(CASE WHEN y>44 and z<=1.33 THEN 1 END) as z18 FROM (SELECT es.ev_end_loc_y as y, es.ev_end_loc_z as z FROM `event`e join `evshot` es ON e.event_id=es.ev_id JOIN `match` m ON event_match_id=m.match_id JOIN competition c ON c.competition_id=m.match_competition_id AND c.competition_season_id=m.match_season_id WHERE `event_player_id` = {pid} and c.competition_season_id = {season}) as sq").fetchall()
    data = [[percentage(shots[0].z1,shots[0].total),percentage(shots[0].z2,shots[0].total),percentage(shots[0].z3,shots[0].total),percentage(shots[0].z4,shots[0].total),percentage(shots[0].z5,shots[0].total),percentage(shots[0].z6,shots[0].total)],
    [percentage(shots[0].z7,shots[0].total),percentage(shots[0].z8,shots[0].total),percentage(shots[0].z9,shots[0].total),percentage(shots[0].z10,shots[0].total),percentage(shots[0].z11,shots[0].total),percentage(shots[0].z12,shots[0].total)],
    [percentage(shots[0].z13,shots[0].total),percentage(shots[0].z14,shots[0].total),percentage(shots[0].z15,shots[0].total),percentage(shots[0].z16,shots[0].total),percentage(shots[0].z17,shots[0].total),percentage(shots[0].z18,shots[0].total)]]
    labels=makeLabels(data)
    heatmap=sns.heatmap(data, cbar=False,xticklabels=False, yticklabels=False, annot=labels,fmt="",cmap="binary")
    map_img = mpimg.imread('static/porteriaT.png')
    heatmap.set_title('')
    heatmap.imshow(map_img,
          aspect = heatmap.get_aspect(),
          extent = heatmap.get_xlim() + heatmap.get_ylim(),
          zorder = 1) #put the map under the heatmap
    
    s = io.BytesIO()
    plt.savefig("static/"+str(pid)+"shotS"+str(season)+".png")
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s
    
    #plt.savefig("static/"+str(pid)+"shotS"+str(season)+".png")

def drawShotsHistoric(pid):
    shots=db.session.execute(f"SELECT COUNT(*) total, COUNT(CASE WHEN y<36 and z>2.67 THEN 1 END) as z1, COUNT(CASE WHEN y>=36 and y<38 and  z>2.67 THEN 1 END) as z2, COUNT(CASE WHEN y>=38 and y<40 and  z>2.67 THEN 1 END) as z3, COUNT(CASE WHEN y>=40 and y<42 and z>2.67 THEN 1 END) as z4,COUNT(CASE WHEN y>=42 and y<=44 and z>2.67 THEN 1 END) as z5, COUNT(CASE WHEN y>44 and z>2.67 THEN 1 END) as z6,COUNT(CASE WHEN y<36 and z>1.33 and z<=2.67 THEN 1 END) as z7, COUNT(CASE WHEN y>=36 and y<38 and z>1.33 and z<=2.67 THEN 1 END) as z8, COUNT(CASE WHEN y>=38 and y<40 and z>1.33 and z<=2.67 THEN 1 END) as z9, COUNT(CASE WHEN y>=40 and y<42 and z>1.33 and z<=2.67 THEN 1 END) as z10,COUNT(CASE WHEN y>=42 and y<=44 and z>1.33 and z<=2.67 THEN 1 END) as z11, COUNT(CASE WHEN y>44 and z>1.33 and z<=2.67 THEN 1 END) as z12,COUNT(CASE WHEN y<36 and z<=1.33 THEN 1 END) as z13, COUNT(CASE WHEN y>=36 and y<38 and z<=1.33 THEN 1 END) as z14, COUNT(CASE WHEN y>=38 and y<40 and z<=1.33  THEN 1 END) as z15, COUNT(CASE WHEN y>=40 and y<42 and z<=1.33 THEN 1 END) as z16,COUNT(CASE WHEN y>=42 and y<=44 and z<=1.33 THEN 1 END) as z17, COUNT(CASE WHEN y>44 and z<=1.33 THEN 1 END) as z18 FROM (SELECT es.ev_end_loc_y as y, es.ev_end_loc_z as z FROM `event`e join `evshot` es ON e.event_id=es.ev_id WHERE `event_player_id` = {pid} ) as sq").fetchall()
    data = [[percentage(shots[0].z1,shots[0].total),percentage(shots[0].z2,shots[0].total),percentage(shots[0].z3,shots[0].total),percentage(shots[0].z4,shots[0].total),percentage(shots[0].z5,shots[0].total),percentage(shots[0].z6,shots[0].total)],
    [percentage(shots[0].z7,shots[0].total),percentage(shots[0].z8,shots[0].total),percentage(shots[0].z9,shots[0].total),percentage(shots[0].z10,shots[0].total),percentage(shots[0].z11,shots[0].total),percentage(shots[0].z12,shots[0].total)],
    [percentage(shots[0].z13,shots[0].total),percentage(shots[0].z14,shots[0].total),percentage(shots[0].z15,shots[0].total),percentage(shots[0].z16,shots[0].total),percentage(shots[0].z17,shots[0].total),percentage(shots[0].z18,shots[0].total)]]
    labels=makeLabels(data)
    heatmap=sns.heatmap(data, cbar=False,xticklabels=False, yticklabels=False, annot=labels,fmt="",cmap="binary")
    map_img = mpimg.imread('static/porteriaT.png')
    heatmap.set_title('')
    heatmap.imshow(map_img,
          aspect = heatmap.get_aspect(),
          extent = heatmap.get_xlim() + heatmap.get_ylim(),
          zorder = 1) #put the map under the heatmap
    
    s = io.BytesIO()
    plt.savefig("static/"+str(pid)+"shotH.png")
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s
    
    #plt.savefig("static/"+str(pid)+"shotS"+str(season)+".png")

def drawHeatMap(pid,match):
    x= db.session.execute(f"SELECT `event`.`event_location_x` as x FROM `event` WHERE `event_player_id` = {pid[0]} and `event_match_id` = {match}").fetchall()
    y= db.session.execute(f"SELECT  `event`.`event_location_y` as y FROM `event` WHERE `event_player_id` = {pid[0]} and `event_match_id` = {match}").fetchall()
    #print(x)
    #print(y)
    #DEFINE GRID SIZE AND RADIUS(h)
    grid_size=1
    h=10 
    #CONSTRUCT GRID
    x_grid=np.arange(0,120,grid_size)
    y_grid=np.arange(0,80,grid_size)
    x_mesh,y_mesh=np.meshgrid(x_grid,y_grid)
    #GRID CENTER POINT
    xc=x_mesh+(grid_size/2)
    yc=y_mesh+(grid_size/2)
    #FUNCTION TO CALCULATE INTENSITY WITH QUARTIC KERNEL
    def kde_quartic(d,h):
        dn=d/h
        P=(15/16)*(1-dn**2)**2
        return P
    #PROCESSING
    intensity_list=[]
    for j in range(len(xc)):
        intensity_row=[]
        for k in range(len(xc[0])):
            kde_value_list=[]
            for i in range(len(x)):
                #CALCULATE DISTANCE
                d=math.sqrt((check1(xc[j][k])-check1(x[i][0]))**2+(check1(yc[j][k])-check1(y[i][0]))**2) 
                if d<=h:
                    p=kde_quartic(d,h)
                else:
                    p=0
                kde_value_list.append(p)
            #SUM ALL INTENSITY VALUE
            p_total=sum(kde_value_list)
            intensity_row.append(p_total)
        intensity_list.append(intensity_row)

    #HEATMAP OUTPUT   
    img = plt.imread("static/terrenoTT.png")
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 120,0, 80], zorder = 1 ) 
    intensity=np.array(intensity_list)
    plt.pcolormesh(x_mesh,y_mesh,intensity)
    plt.set_cmap(LinearSegmentedColormap.from_list('Greens',["g","b", "y", "r"], N=256,))
    plt.axis('off')
    ax.set_title('')
    plt.savefig("static/"+str(pid[0])+"heatmapM"+str(match)+".png")
    s = io.BytesIO()
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s

def drawHeatMapSeason(pid,season):
    x= db.session.execute(f"SELECT `event`.`event_location_x` as x FROM `event` JOIN `match` m ON event_match_id=m.match_id JOIN competition c ON c.competition_id=m.match_competition_id AND c.competition_season_id=m.match_season_id WHERE `event_player_id` = {pid} and c.competition_season_id = {season}").fetchall()
    y= db.session.execute(f"SELECT `event`.`event_location_y` as y  FROM `event` JOIN `match` m ON event_match_id=m.match_id JOIN competition c ON c.competition_id=m.match_competition_id AND c.competition_season_id=m.match_season_id WHERE `event_player_id` = {pid} and c.competition_season_id = {season}").fetchall()
    #print(x)
    #print(y)
    #DEFINE GRID SIZE AND RADIUS(h)
    grid_size=1
    h=10 
    #CONSTRUCT GRID
    x_grid=np.arange(0,120,grid_size)
    y_grid=np.arange(0,80,grid_size)
    x_mesh,y_mesh=np.meshgrid(x_grid,y_grid)
    #GRID CENTER POINT
    xc=x_mesh+(grid_size/2)
    yc=y_mesh+(grid_size/2)
    #FUNCTION TO CALCULATE INTENSITY WITH QUARTIC KERNEL
    def kde_quartic(d,h):
        dn=d/h
        P=(15/16)*(1-dn**2)**2
        return P
    #PROCESSING
    intensity_list=[]
    for j in range(len(xc)):
        intensity_row=[]
        for k in range(len(xc[0])):
            kde_value_list=[]
            for i in range(len(x)):
                #CALCULATE DISTANCE
                d=math.sqrt((check1(xc[j][k])-check1(x[i][0]))**2+(check1(yc[j][k])-check1(y[i][0]))**2) 
                if d<=h:
                    p=kde_quartic(d,h)
                else:
                    p=0
                kde_value_list.append(p)
            #SUM ALL INTENSITY VALUE
            p_total=sum(kde_value_list)
            intensity_row.append(p_total)
        intensity_list.append(intensity_row)

    #HEATMAP OUTPUT   
    img = plt.imread("static/terrenoTT.png")
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 120,0, 80], zorder = 1 ) 
    intensity=np.array(intensity_list)
    plt.pcolormesh(x_mesh,y_mesh,intensity)
    plt.set_cmap(LinearSegmentedColormap.from_list('Greens',["g","b", "y", "r"], N=256,))
    plt.axis('off')
    ax.set_title('')
    plt.savefig("static/"+str(pid)+"heatmapS"+str(season)+".png")
    s = io.BytesIO()
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s

def drawHeatMapHistoric(pid):
    x= db.session.execute(f"SELECT `event`.`event_location_x` as x FROM `event`  WHERE `event_player_id` = {pid}").fetchall()
    y= db.session.execute(f"SELECT `event`.`event_location_y` as y  FROM `event` WHERE `event_player_id` = {pid} ").fetchall()
    #print(x)
    #print(y)
    #DEFINE GRID SIZE AND RADIUS(h)
    grid_size=1
    h=10 
    #CONSTRUCT GRID
    x_grid=np.arange(0,120,grid_size)
    y_grid=np.arange(0,80,grid_size)
    x_mesh,y_mesh=np.meshgrid(x_grid,y_grid)
    #GRID CENTER POINT
    xc=x_mesh+(grid_size/2)
    yc=y_mesh+(grid_size/2)
    #FUNCTION TO CALCULATE INTENSITY WITH QUARTIC KERNEL
    def kde_quartic(d,h):
        dn=d/h
        P=(15/16)*(1-dn**2)**2
        return P
    #PROCESSING
    intensity_list=[]
    for j in range(len(xc)):
        intensity_row=[]
        for k in range(len(xc[0])):
            kde_value_list=[]
            for i in range(len(x)):
                #CALCULATE DISTANCE
                d=math.sqrt((check1(xc[j][k])-check1(x[i][0]))**2+(check1(yc[j][k])-check1(y[i][0]))**2) 
                if d<=h:
                    p=kde_quartic(d,h)
                else:
                    p=0
                kde_value_list.append(p)
            #SUM ALL INTENSITY VALUE
            p_total=sum(kde_value_list)
            intensity_row.append(p_total)
        intensity_list.append(intensity_row)

    #HEATMAP OUTPUT   
    img = plt.imread("static/terrenoTT.png")
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 120,0, 80], zorder = 1 ) 
    intensity=np.array(intensity_list)
    plt.pcolormesh(x_mesh,y_mesh,intensity)
    plt.set_cmap(LinearSegmentedColormap.from_list('Greens',["g","b", "y", "r"], N=256,))
    plt.axis('off')
    ax.set_title('')
    plt.savefig("static/"+str(pid)+"heatmapH.png")
    s = io.BytesIO()
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,%s"%s

#Metodos auxiliares
def makeLabels(array):
    labels = list()
    for z in array:
        fila = list()
        for d in z:
            fila.append(str(d)+"%")
        labels.append(fila)
    return labels

def percentage(a,b):

    if(a== 0 or a == None or b == 0 or b == None):
        return 0
    else:
        return round(((a/b)*100),1)

def check(a,b,n):
    if(n==0):
        if(a == 0 or a == None ):
            return 0
        else:
            return a
    if(n==1):
        if(a == 0 or b ==0 or a == None or b == None):
            return 0
        else:
            return a/b
    if (n == 2):
        if(a == 0 or b ==0 or a == None or b == None):
            return 0
        else:
            return a-b

def check1(a):
    if(a == 0 or a == None ):
        return 0
    else:
        return a

def checkSQL(con):
    con  = dict(con[0])
    for k, v in con.items():
        if v == None:
            con[k] = 0
    #print(con)
    return con

app.jinja_env.globals.update(check=check)

def bigger(a,b):
    if a>=b:
        return a
    else:
        return b

#Metodo para comprobar si num<den para la grafica
def checkNumDen(a,b):
    if (a == 0 or a == None ):
         return b
    if(b == None or b == 0):
        return 0
    else:
        return bigger(a,b)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True) 

#SELECT DISTINCT l.lineup_player_id as Jugador,p.player_name ,c.competition_season_name as Season FROM `match` m JOIN lineup l ON l.lineup_match_id = m.match_id JOIN competition c ON m.match_competition_id=c.competition_id JOIN player p ON l.lineup_player_id=p.player_id WHERE l.lineup_team_id= 217 GROUP BY l.lineup_player_id, c.competition_season_id ORDER BY c.competition_season_id
#SELECT DISTINCT l.lineup_player_id as Jugador,p.player_name ,c.competition_season_name as Season FROM `match` m, lineup l ,competition c, player p WHERE l.lineup_team_id= 217 AND l.lineup_player_id=p.player_id AND m.match_competition_id=c.competition_id AND l.lineup_match_id = m.match_id GROUP BY l.lineup_player_id, c.competition_season_id ORDER BY c.competition_season_id

