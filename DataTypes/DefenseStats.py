from decimal import Decimal

class DefenseStats:
    def __init__(self, values):
        teamLine = values[1].strip().split(' ')
        self.wannabeOwner = 'none'
        self.wannabeDraftPick = -1
        self.wannabePrice = -1
        self.NFLTeam = teamLine[len(teamLine) - 1]
        self.position = teamLine[len(teamLine) - 3]
        self.playerName = values[1][:values[1].find(self.position)].strip()
        self.avail = values[0]
        self.opponent = values[2]
        self.ovp = int(values[3])
        self.byeWeek = int(values[4])
        self.percentOwn = int(values[5])
        self.percentStart = int(values[6])
        self.fantasyPoints = float(values[17])

        self.sacks = float(values[7])
        self.fumbles = int(values[8])
        self.interceptions = int(values[9])
        self.touchdowns = float(values[10])
        self.safeties = int(values[11])
        self.yardsAgainst = int(values[13])
        self.pointsAgainst = int(values[15])

    def createJson(self):
        Item={
            'wannabeOwner': self.wannabeOwner,
            'wannabeDraftPick': self.wannabeDraftPick,
            'wannabePrice': self.wannabePrice,
            'playerName': self.playerName,
            'NFLTeam': self.NFLTeam,
            'position': self.position,
            'owner' : self.avail,
            'ovp' : self.ovp,
            'opponent': self.opponent,
            'byeWeek': self.byeWeek,
            'percentOwn': self.percentOwn,
            'percentStart': self.percentStart,
            'fantasyPoints': Decimal(str(self.fantasyPoints)),
            'sacks': Decimal(str(self.sacks)),
            'fumbles': self.fumbles,
            'interceptions': self.interceptions,
            'touchdowns': Decimal(str(self.touchdowns)),
            'safeties': self.safeties,
            'yardsAgainst': self.yardsAgainst,
            'pointsAgainst': self.pointsAgainst
        }
        return Item;

    def createDdbItem(self):
        item = {
            "pointsAgainst": { "N": str(self.pointsAgainst) },
            "playerName": { "S": str(self.playerName) },
            "percentStart": { "N": str(self.percentStart) },
            "NFLTeam": { "S": str(self.NFLTeam) },
            "touchdowns": { "N": str(self.touchdowns) },
            "fumbles": { "N": str(self.fumbles) },
            "safeties": { "N": str(self.safeties) },
            "ovp": { "N": str(self.ovp) },
            "sacks": { "N": str(self.sacks) },
            "interceptions": { "N": str(self.interceptions) },
            "fantasyPoints": { "N": str(self.fantasyPoints) },
            "percentOwn": { "N": str(self.percentOwn) },
            "yardsAgainst": { "N": str(self.yardsAgainst) },
            "opponent": { "S": str(self.opponent) },
            "byeWeek": { "N": str(self.byeWeek) },
            "position": { "S": str(self.position) }
        }
        return item

# statString = 'W ,Jaguars DST | JAC ,@NYG,9,18,1,52,647,15,21,5,282,2896,1788,4684,2,117.00'
# stat = DefenseStats(statString.split(','))
#
# stat.avail
