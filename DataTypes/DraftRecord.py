
class DraftRecord:
    def __init__(self, draftName, values):
        self.draftName = draftName
        self.ownerName = values['ownerName']
        self.teamName = values['teamName']
        self.budget = int(values['budget'])
        self.draftOrder = int(values['draftOrder'])
        self.isAdmin = bool(values['isAdmin'])

    def createJson(self):
        Item={
            'draftName' : self.draftName,
            'ownerName' : self.ownerName,
            'teamName' : self.teamName,
            'remainingBudget' : self.remainingBudget,
            'draftOrder' : self.draftOrder,
            'isAdmin' : self.isAdmin
        }
