from decimal import Decimal

class DraftedPlayer:
    def __init__(self, values):
        print('type of values = ' + str(type(values)))
        self.playerName = values['playerName']
        self.position = values['position']
        self.NFLTeam = values['NFLTeam']
        self.byeWeek = values['byeWeek']
        self.fantasyPoints = int(values['fantasyPoints'])
        self.ownerName = values['ownerName']
        self.price = values['price']
        self.draftOrder = 0
