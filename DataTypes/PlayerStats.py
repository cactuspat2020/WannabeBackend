from decimal import Decimal

class PlayerStats:
    def __init__(self, values):
        playerLine = values[1].strip().split(' ')
        self.NFLTeam = playerLine[len(playerLine)-1]
        self.position = playerLine[len(playerLine)-3]
        self.playerName = values[1][:values[1].find(self.position)].strip()
        self.opponent = values[2]
        self.ovp = values[3]
        self.byeWeek = int(values[4])
        self.percentOwn = int(values[5])
        self.percentStart = int(values[6])
        self.fantasyPoints = int(values[21])

        self.passingAttempts = int(values[7])
        self.completed = int(values[8])
        self.passingyards = int(values[9])
        self.passingTDs = int(values[10])
        self.passingINTs = int(values[11])
        self.rushingAttempts = int(values[12])
        self.rushingYards = int(values[13])
        self.rushingTDs = int(values[14])
        self.receivingTargets = int(values[15])
        self.receivingReceptions = int(values[16])
        self.receivingYards = int(values[17])
        self.receivingTDs = int(values[18])
        self.fumblesLost = int(values[19])

    def createJson(self):
        Item={
            'playerName': self.playerName,
            'NFLTeam': self.NFLTeam,
            'position': self.position,
            'owner' : self.avail,
            'ovp' : self.ovp,
            'opponent': self.opponent,
            'byeWeek': self.byeWeek,
            'percentOwn': Decimal(str(self.percentOwn)),
            'percentStart': Decimal(str(self.percentStart)),
            'fantasyPoints': Decimal(str(self.fantasyPoints)),
            'passingAttempts': Decimal(str(self.passingAttempts)),
            'completed': Decimal(str(self.completed)),
            'passingyards': Decimal(str(self.passingyards)),
            'passingTDs': Decimal(str(self.passingTDs)),
            'passingINTs': Decimal(str(self.passingINTs)),
            'rushingAttempts': Decimal(str(self.rushingAttempts)),
            'rushingYards': Decimal(str(self.rushingYards)),
            'rushingTDs': Decimal(str(self.rushingTDs)),
            'receivingTargets': Decimal(str(self.receivingTargets)),
            'receivingReceptions': Decimal(str(self.receivingReceptions)),
            'receivingYards': Decimal(str(self.receivingYards)),
            'receivingTDs': Decimal(str(self.receivingTDs)),
            'fumblesLost': Decimal(str(self.fumblesLost))
        }
        return Item;

# statString = 'W ,Russell Wilson QB | SEA,@DEN,7,553,339,3983,34,11,95,586,6.2,3,0,0,0,0.0,0,3,266.00'
# stat = PlayerStats(statString)
#
# stat.avail;
