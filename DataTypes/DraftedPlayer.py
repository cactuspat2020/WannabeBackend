from decimal import Decimal

class DraftedPlayer:
    def __init__(self, values):
        print('type of values = ' + str(type(values)))
        self.playerName = values['playerName']
        self.position = values['position']
        self.draftOrder = values['draftOrder']
        self.NFLTeam = values['NFLTeam']
        self.byeWeek = values['byeWeek']
        self.fantasyPoints = int(values['fantasyPoints'])
        self.ownerName = values['ownerName']
        self.price = values['price']

    def createDdbItem(self):
        item = {
            "playerName": { "S": str(self.playerName) },
            "position": { "S": str(self.position) },
            "draftOrder": {"N": str(self.draftOrder)},
            "NFLTeam": { "S": str(self.NFLTeam) },
            "fantasyPoints": { "N": str(self.fantasyPoints) },
            "byeWeek": { "N": str(self.byeWeek) },
            "ownerName": { "S": str(self.ownerName) },
            "price": {"N": str(self.price)}
        }
        return item