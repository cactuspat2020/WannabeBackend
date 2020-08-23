import csv
import boto3
import json
import decimal
# from DataTypes.DefenseStats import DefenseStats
from DataTypes.KickerStats import KickerStats
from DataTypes.DefenseStats import DefenseStats
from DataTypes.PlayerStats import PlayerStats
from DataTypes.DraftedPlayer import DraftedPlayer
# from DataTypes.PlayerStats import PlayerStats


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def loadPlayers(playerType):

    dyndb = boto3.client('dynamodb', region_name='us-west-2')

    statFileName = 'Stats/' + playerType + '.csv'

    statFile = open(statFileName)
    reader = csv.reader(statFile, delimiter=',', quotechar='"')
    counter = 0
    linesProcessed = 0
    for row in reader:
        counter = counter + 1

        if counter > 3 and row[0].find("Report") == -1 and row[1].find('|') > 0:
            player = {
                'Kickers': lambda row: KickerStats(row),
                'Offense': lambda row: PlayerStats(row),
                'Defense': lambda row: DefenseStats(row)
            }[playerType](row)

            dyndb.put_item()
            response = dyndb.put_item(
                TableName='PlayerStats',
                Item=player.createDdbItem()
            )
            linesProcessed = linesProcessed + 1;
            print(str(linesProcessed) + ' Loaded: ' + str(player.playerName) +", " +str(player.NFLTeam) )
            # print('Response = ' + str(response)

def clearDatabase(tableName, partitionKey, sortKey):
    dyndb = boto3.client('dynamodb', region_name='us-west-2')
    records = dyndb.scan(TableName=tableName)['Items']

    for record in records:
        jsonData = record.items()
        dyndb.delete_item(
            TableName=tableName,
            Key={partitionKey: record[partitionKey], sortKey: record[sortKey] }
        )


def restoreFromSpreadsheet(filename):
    dyndb = boto3.client('dynamodb', region_name='us-west-2')

    statFileName = 'Stats/' + filename + '.csv'

    statFile = open(statFileName)
    reader = csv.reader(statFile, delimiter=',', quotechar='"')
    counter = 0
    linesProcessed = 0
    for row in reader:
        counter = counter + 1

        if counter == 1 :
            continue
        elif counter == 2:
            keys = row;
        else :
            player_dict = {}

            for i in range(0, len(keys)-1) :
                player_dict[keys[i]] = row[i]

            player = DraftedPlayer(player_dict)
            player.draftOrder = linesProcessed + 1

            # dyndb.put_item()
            item = player.createDdbItem()
            response = dyndb.put_item(
                TableName='DraftedPlayers',
                Item=item
            )
            linesProcessed = linesProcessed + 1;
            print(str(linesProcessed) + ' Loaded: ' + str(player.playerName) +", " +str(player.NFLTeam) )
            # print('Response = ' + str(response)




clearDatabase('DraftedPlayers', 'draftOrder', 'playerName')
restoreFromSpreadsheet('2019Draft')

# loadPlayers('Kickers')
# loadPlayers('Defense')
# loadPlayers('Offense')
