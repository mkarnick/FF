

class team:
    def __init__(self, name, wins=0,losses=0, roster=[], realName='', id=0):
        self.name=name
        self.wins=wins
        self.losses=losses
        self.roster=roster
        self.realName = realName
        self.id = id
class player:
	def __init__(self, name, slot, position='NP?'):
		self.name=name
		self.position=position
		self.slot=slot
class matchupScore:
    def __init__(self, ateam, bteam, ascore, bscore, url=''):
        self.ateam = ateam
        self.bteam = bteam
        self.ascore = ascore
        self.bscore = bscore
        self.url = url
    def getTotal(self):
        return self.ascore + self.bscore

class teamRoster:
	def __init__(self, player):
		self.player = player


