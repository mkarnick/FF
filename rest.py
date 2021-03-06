from fantasyObjects import team, matchupScore, teamRoster, player
#!/usr/bin/env python
import numpy as np
import os, sys, re
import MySQLdb as mdb 
sys.path.insert(1,'/usr/local/lib/python2.7/site-packages/')
sys.path.insert(1,'/Library/Python/2.7/site-packages/') 
sys.path.insert(1,'/root/Site_ff/')
sys.path.insert(1,'/Users/karnick/Development/Django/FFSITE/')
sys.path.insert(1,'/root/FF/')
os.environ["DJANGO_SETTINGS_MODULE"] = "FFSITE.settings"

# sys.path.insert(1,'/Users/karnick/Development/Angular/')
import django
django.setup()
from FFAPP.models import Subdomain, ChatText, User
from django.core import serializers

from bs4 import BeautifulSoup
import urllib2

import web
import xml.etree.ElementTree as ET
# from mattyballapp.models_top import Players
# from mattyballapp.models import ViewAllAvgranksandcounts, CheckUniqueTeamsInPlayerstable
import json
import mail

# tree = ET.parse('user_data.xml')
# root = tree.getroot()

urls = (
    #ROOT 
    '/','home',
    # Return subdomain used
    '/getsub','getsub',
    # POST for subdomain signup
    '/signup','signup',

    '/logintest','Index',
    '/login','Login',
    '/logout','Logout',

    # Login form??
    '/userinfo/(.*)', 'userinfo',
    # Login form??
    '/users/(.*)', 'login_class',

    # Standings in league
    '/(.*)/(.*)/teamlist','ff_teams',
    # Scoreboard with default set to team 1
    '/(.*)/scores','ff_scores',
    # Scoreboard for entered team number
    '/(.*)/scores/(.*)','ff_scores',
    # Scoreboard with default set to team 1
    '/(.*)/roster/(.*)/(.*)','ff_teamRoster',
    '/(.*)/roster/(.*)','ff_teamRoster',

    '/chat/submit','chat_submit',
    '/chat/get/(.*)','chat_get',

    # Serve content from filesystem
    '/(.*)', 'files',

)  
web.config.debug = False
app = web.application(urls,globals())

session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'userId': 0})


class Login:
    def GET(self):
        session.userId = 1
        return str(session.userId)
    def POST(self):
        i = web.input()
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        #print web.data()
        d = json.loads(web.data())
        #print d
        print "Checking for existing user %s/%s" %(d['username'], d['password'])
        existing = User.objects.filter(username=d['username'], password=d['password'])

        if len(existing) == 0:
            print "No user found with that combo"
            session.userId = 0                
            raise web.internalerror("Loggin Error")
        else:
            print "Username found."
            thisUser = existing[0]
            session.userId = thisUser.idx
            session.username = thisUser.username
            session.firstName = thisUser.firstName
            session.lastName = thisUser.lastName
            raise web.seeother('/')

        # except:
        #     print "Something fucked up. Bailing out"
        #     raise web.internalerror("webb internal error son")
class Logout:
    def GET(self):
        session.userId = 0
        # session.kill()
        return 0

class Index:
    def GET(self):
        try:
            if session.userId==0:
                return "You are not logged in"
            elif session.userId==1:
                return "You ARE logged in!"
            else:
                return "Couldn't read your userId"
        except:
            return "Faulted. You probably aren't logged in"
class getsub:
    def GET(self):
        ctx = web.ctx
        subname= ctx.home.replace('.leaguedashboard.com','').replace('http://','')
        FoundSub = Subdomain.objects.filter(subname=subname)
        return serializers.serialize("json", FoundSub)
        
#        return "%s %s %s or %s %s" %(ctx.home, ctx.path, ctx.query, ctx.home, ctx.fullpath)


class home:
    def GET(self):
        ctx = web.ctx
        subname= ctx.home.replace('leaguedashboard.com','').replace('http://','')
        if subname == 'www.' or subname == '':
            with open ("index.html", "r") as myfile:
                data=myfile.read().replace('\n', '')
                ctx = web.ctx
            return data
        else:
            raise web.seeother('/dash.html')


class files:
    def GET(self, filename):
        if re.compile('(.*).js').match(filename):   
            web.header('Content-Type','text/javascript')
        elif re.compile('(.*).css').match(filename):
            web.header('Content-Type', 'text/css')
        elif re.compile('(.*).html').match(filename):
            web.header('Content-Type', 'text/html')
        else:
            web.header('Content-Type', 'application/json')
        with open (filename, "r") as myfile:
            data=myfile.read()#.replace('\n', '')
            ctx = web.ctx
        return data

	
class ff_teams:
    def GET(self, inLeague, inYear):
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')        # return 1
        url = 'http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=%s' %(inLeague, inYear)
#        url = 'http://games.espn.go.com/ffl/standings?leagueId=716644&seasonId=2014'
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        # found = soup.find(class_="tableBody").findChildren('tr')
        found = soup.findChildren('table')[0].findChildren('tr', class_='tableBody')
        resultList = []
        objList = []
        xi=0
        for e in found:
            xi+=1
            resultList.append(e.td.string)

            es = str(e)
            teamIdLen = es[es.find('teamId')+len('teamId')+1:].find('&amp')
            teamId = es[es.find('teamId')+len('teamId')+1:][0:teamIdLen]

            teamObj = team(id=teamId, name=e.find_all('td')[0].string,wins=e.find_all('td')[1].string,losses=e.find_all('td')[2].string)
            objList.append(teamObj.__dict__)
        return json.dumps(objList)



class ff_scores:
    def GET(self, inLeague, week=1):
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')        # return 1
        url = 'http://games.espn.go.com/ffl/scoreboard?leagueId=%s&matchupPeriodId=%s' %(inLeague, week)
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        # soup.find(id='scoreboardMatchups').find_all('table',class_='ptsBased matchup')[0].find_all(class_='score')[0].string
        # soup.find(id='scoreboardMatchups').find_all('table',class_='ptsBased matchup')[0].find_all('a')[0].string
        matchupList=[]
        for m in soup.find(id='scoreboardMatchups').find_all('table',class_='ptsBased matchup'):
            teamAname = m.find_all('a')[0].string
            teamAscore = m.find_all(class_='score')[0].string
            teamBname = m.find_all('a')[1].string
            teamBscore = m.find_all(class_='score')[1].string
            thisMatchupObj = matchupScore(ateam=teamAname, bteam=teamBname, ascore=teamAscore, bscore=teamBscore, url=url)
            matchupList.append(thisMatchupObj.__dict__)
        return json.dumps(matchupList)

class ff_teamRoster:
    def GET(self, inLeague, inYear, inTeam=0):
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')        # return 1
        #http://games.espn.go.com/ffl/clubhouse?leagueId=716644&teamId=5&seasonId=2014
        foundTeamRosters=[]
        if inTeam==0:
            inds = range(1,12)
        else:
            inds = [];inds.append(inTeam)
         
        for teamId in inds:
            url = 'http://games.espn.go.com/ffl/clubhouse?leagueId=%s&teamId=%s&seasonId=%s' %(inLeague, teamId, inYear)
            # return url
            soup = BeautifulSoup(urllib2.urlopen(url).read())
            # found = soup.findChildren('table')[0].findChildren('td', class_='playertablePlayerName')
            found = soup.findChildren('table')[0].findChildren('tr', class_='pncPlayerRow')
            foundPlayers=[]
            foundPositions=[]
            teamName = soup.findChildren('table')[0].findChildren(class_='team-name')[0].text
            realName = soup.findChildren('table')[0].findChildren(class_='per-info')[0].text
            for f in found:
                try:
                    fullString = str(f.findChildren('td')[1]).replace('\xa0',' ').replace('\xc2',' ')
                    posString = BeautifulSoup(fullString.replace(str(BeautifulSoup(fullString).a),'')).body.string.replace(', ','')

                    thisPlayerName = f.a.string
                    thisPlayerSlot = f.findChildren('td')[0].string
                    posStr = fullString.find('</td>')

                    strLen = len(fullString)
                    aLoc = fullString.find('</a>')
                    subString = fullString[strLen-7:strLen]
                    pos = subString[0:2]
                    #print fullString
                    #print subString
                    objPlayer = player(name=thisPlayerName, position=pos, slot=thisPlayerSlot)
                    #print pos
                    foundPlayers.append(objPlayer.__dict__)

                except:
                    pass
            foundTeamRosters.append(team(name=teamName, roster=foundPlayers,  realName=realName).__dict__) 

        return json.dumps(foundTeamRosters) 

# class ff_allTeamRosters:
#     found = soup.findChildren('table')[0].findChildren('td', class_='playertablePlayerName')

#     for range(1,12):
#         url = 'http://games.espn.go.com/ffl/clubhouse?leagueId=%s&teamId=%s&seasonId=%s'

        
class userinfo:
    def GET(self, username):
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        userData = User.objects.filter(username=username)
        return serializers.serialize("json", userData)
class signup:
    def POST(self):
        i = web.input()
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        #print web.data()
        d = json.loads(web.data())
        #print d
        print "Checking for existing obj %s" %(d['subname'])
        existing = Subdomain.objects.filter(subname=d['subname'])
        try:
            if len(existing) == 0:
                newSignup = Subdomain(subname=d['subname'], leagueId=int(d['leagueId']), email=d['email']) 
                newSignup.save()
                mail.email(d['email'])
            else:
                print "Object exists. Bailing out."
                raise web.internalerror("webb internal error son")

        except:
            print "Something fucked up. Bailing out"
            raise web.internalerror("webb internal error son")
        print "Saved to ORM"
        raise web.seeother('/')
        
        #return "Form Done"
        #return "This is the login form result: %s, %s" %(i.subname, i.leagueId)

class chat_submit:
    def POST(self):
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')

        timePattern ='%I:%M%p'
        from datetime import datetime, timedelta
        from pytz import timezone
        import pytz
        utc = pytz.utc
        eastern = timezone('US/Eastern')
        estnow = datetime.now(eastern)
        tstamp = estnow.strftime(timePattern)
        # #print web.data()
        d = json.loads(web.data())
        # import datetime, time
        # ts = time.time()
        # tstamp = datetime.datetime.now().strftime(timePattern)
        #actualtstamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        NewChat = ChatText(parentLeague=d['subname'], author=d['author'], timestamp=tstamp, commentText=d['chatText']) 
        NewChat.save()
        raise web.seeother('/') 
class chat_get:
    def GET(self, inSub):

        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        chatSize = len(ChatText.objects.filter(parentLeague=inSub))
        if chatSize < 10:
            chatE=chatSize
            chatS=0
        else:
            chatS=chatSize-10
            chatE=chatSize
        chatData = ChatText.objects.filter(parentLeague=inSub)[chatS:chatE]

        return serializers.serialize("json", chatData)
if __name__ == '__main__':
    def internalerror():
        return web.internalerror("Bad, bad server. No donut for you.")
    app.internalerror = internalerror
    app.run()
