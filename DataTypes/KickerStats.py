from decimal import Decimal

class KickerStats:
    def __init__(self, values):
        playerLine = values[1].strip().split(' ')
        self.wannabeOwner = 'none'
        self.wannabeDraftPick = -1
        self.wannabePrice = -1
        self.NFLTeam = playerLine[len(playerLine)-1]
        self.position = playerLine[len(playerLine)-3]
        self.playerName = values[1][:values[1].find(self.position+' |')].strip()
        self.avail = values[0]
        self.opponent = values[2]
        self.ovp = values[3]
        self.byeWeek = int(values[4])
        self.percentOwn = int(values[5])
        self.percentStart = int(values[6])
        self.fantasyPoints = int(values[23])

        self.totalFieldGoalsMade = int(values[8])
        self.totalFieldGoalsAttempts = int(values[9])
        self.fieldGoalAttempts20 = float(values[12])
        self.fieldGoalsMade20 = float(values[13])
        self.fieldGoalAttempts30 = float(values[14])
        self.fieldGoalsMade30 = float(values[15])
        self.fieldGoalAttempts40 = float(values[16])
        self.fieldGoalsMade40 = float(values[17])
        self.fieldGoalAttempts50 = float(values[18])
        self.fieldGoalsMade50 = float(values[19])
        self.extraPointsMade = float(values[20])
        self.extraPointAttempts = int(values[21])

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
            'fantasyPoints': self.fantasyPoints,
            'totalFieldGoalsMade': self.totalFieldGoalsMade,
            'totalFieldGoalsAttempts': self.totalFieldGoalsAttempts,
            'fieldGoalAttempts20': Decimal(str(self.fieldGoalAttempts20)),
            'fieldGoalsMade20': Decimal(str(self.fieldGoalsMade20)),
            'fieldGoalAttempts30': Decimal(str(self.fieldGoalAttempts30)),
            'fieldGoalsMade30': Decimal(str(self.fieldGoalsMade30)),
            'fieldGoalAttempts40': Decimal(str(self.fieldGoalAttempts40)),
            'fieldGoalsMade40': Decimal(str(self.fieldGoalsMade40)),
            'fieldGoalAttempts50': Decimal(str(self.fieldGoalAttempts50)),
            'fieldGoalsMade50': Decimal(str(self.fieldGoalsMade50)),
            'extraPointsMade': Decimal(str(self.extraPointsMade)),
            'extraPointAttempts': self.extraPointAttempts
        }
        return Item;

    def createDdbItem(self):
        Item = {
            "playerName": { "S": str(self.playerName) },
            "percentStart": { "N": str(self.percentStart) },
            "NFLTeam": { "S": str(self.NFLTeam) },
            "fieldGoalsMade40": { "S": str(self.fieldGoalsMade40) },
            "fieldGoalsMade30": { "S": str(self.fieldGoalsMade40) },
            "fieldGoalsMade20": { "S": str(self.fieldGoalsMade20) },
            "extraPointsMade": { "S": str(self.extraPointsMade) },
            "ovp": { "S": str(self.ovp) },
            "fieldGoalsMade50": { "S": str(self.fieldGoalsMade50) },
            "fieldGoalAttempts40": { "S": str(self.fieldGoalAttempts40) },
            "fieldGoalAttempts30": { "S": str(self.fieldGoalAttempts30) },
            "fantasyPoints": { "S": str(self.fantasyPoints) },
            "fieldGoalAttempts50": { "S": str(self.fieldGoalAttempts50) },
            "percentOwn": { "S": str(self.percentOwn) },
            "opponent": { "S": str(self.opponent) },
            "fieldGoalAttempts20": { "S": str(self.fieldGoalAttempts20) },
            "totalFieldGoalsAttempts": { "S": str(self.totalFieldGoalsAttempts) },
            "totalFieldGoalsMade": { "S": str(self.totalFieldGoalsMade) },
            "byeWeek": { "S": str(self.byeWeek) },
            "extraPointAttempts": { "S": str(self.extraPointAttempts) },
            "position": { "S": str(self.position) }
        }
        return Item


# statString = 'W ,Stephen Gostkowski K | NE ,HOU,11,40.2,35.6,0,45.8,45.8,0,2,148.00'
# stat = KickerStats(statString)
#
# stat.avail;