import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from DataTypes.DraftRecord import DraftRecord
from DataTypes.DraftedPlayer import DraftedPlayer

# import requests

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

#################################################
# DraftPlayers Table Methods
#################################################

def saveDraftPick(event, context):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('DraftedPlayers')

    body = event['body']
    print(str(body))
    print('type of body = ' + str(type(body)))
    records = table.scan()
    print('retrieved ' + str(len(records['Items'])) + ' from the database')

    record = DraftedPlayer(json.loads(body));

    # record = DraftedPlayer(body)
    record.draftOrder = len(records['Items']) + 1

    playerExistsInDB = False;
    if (len(records['Items']) != 0):
        for player in records['Items']:
            if player['playerName'] == record.playerName:
                playerExistsInDB = True
                break

    if (playerExistsInDB):
        print('Player ' + record.playerName + ' already exists in DB. Skipping')
    else:
        table.put_item(Item=record.__dict__)

    print('Done with save. Returning 200')
    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": "*" },
    }

def undoLastPick(event, context):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('DraftedPlayers')

    print(str(event))
    lastPlayerPicked = json.loads(event['body'])
    print(str(lastPlayerPicked))
    # lastPlayerPicked = DraftedPlayer(json.loads(body));

    # draftedPlayers = table.scan()['Items']
    # for player in draftedPlayers:
    #     if len(draftedPlayers) == player['draftOrder']:
    #         lastPlayerPicked = player

    print('Deleting ' + str(lastPlayerPicked))
    table.delete_item(Key = {
            'draftOrder': lastPlayerPicked['draftOrder'],
            'playerName': lastPlayerPicked['playerName']
        })
    return  getDraftedPlayers(event, context);

def getDraftedPlayers(event, context):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('DraftedPlayers')

    results = table.scan()['Items'];
    jsonData = json.dumps(results, default=decimal_default)
    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": "*" },
        "body": jsonData
    }

def getPlayerRankings (event, context):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('PlayerRankings')

    results = table.scan()['Items'];
    jsonData = json.dumps(results, default=decimal_default)
    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": "*" },
        "body": jsonData
    }

#################################################
# DraftStatus Table Methods
#################################################
def saveDraftInfo(event, context):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('DraftStatus')
    draftedPlayersTable = dynamodb.Table('DraftedPlayers')
    print("In saveDraftInfo")

    # Remove existing records
    records = table.scan()['Items']
    for record in records:
        table.delete_item(Key = {
            'ownerName': record['ownerName'],
            'teamName': record['teamName']
        })
    print("Records Removed from DraftStatus")

    # Clear out the current draft information
    records = draftedPlayersTable.scan()['Items']
    print('Deleting ' + str(len(records)) + ' records')
    for record in records:
        draftedPlayersTable.delete_item(Key={
            'draftOrder': record['draftOrder'],
            'playerName': record['playerName']
        })
    print("Records Removed from DraftedPlayers")

    body = json.loads(event['body'])
    print('body = ' + str(body))
    draftname = body['draftName']
    budget = body['budget']
    leagueSize = body['leagueSize']
    ownerRecords = body['teams']

    print("Adding new records")
    for record in ownerRecords:
        itemToStore = DraftRecord(draftname, budget, record)
        itemToStore.draftName = draftname
        itemToStore.budget = budget

        table.put_item(Item=itemToStore.__dict__)

    print('Returning a 200')
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        }
    }

def getDraftInfo(event, context):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('DraftStatus')
    records = table.scan()['Items']
    jsonData = json.dumps(records, default=decimal_default)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": jsonData
    }

#################################################
# DraftStatus Table Methods
#################################################
def getPlayers(event, context):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('PlayerStats')

    records = table.scan(AttributesToGet=['playerName', 'NFLTeam', 'byeWeek', 'fantasyPoints',
                                           'position', 'percentOwn', 'percentStart'])['Items']
    jsonData = json.dumps(records, default=decimal_default)
    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": "*" },
        "body": jsonData
    }



debugEvent = json.loads('{\"body\":{\"price\":23,\"ownerName\":\"Gunslingers\",\"playerName\":\"Patrick Mahomes\",\"NFLTeam\":\"KC\",\"byeWeek\":12,\"fantasyPoints\":272,\"position\":\"QB\"}}')
draftedPlayerEvent = json.loads('{ \"body\": { \"position\": \"QB\", \"playerName\": \"Aaron Rodgers\",\"NFLTeam\": \"Packers\",\"byeWeek\": 10,\"fantasyPoints\": 123.3,\"ownerName\": \"Gunslingers\",\"price\":24}}')
draftedPlayerEvent2 = json.loads('{ \"body\": { \"position\": \"RB\", \"playerName\": \"Barry Sanders\",\"NFLTeam\": \"Packers\",\"byeWeek\": 10,\"fantasyPoints\": 123.3,\"ownerName\": \"Gunslingers\",\"price\":93}}')
testEvent = json.loads('{ \"queryStringParameters\": { \"position\": \"RB\", \"playerList\": \"available\" }}')
testDraftEvent = json.loads('{ \"body\": { \"position\": \"QB\", \"playerName\": \"Aaron Rodgers\",\"owner\": \"Gunslingers\",\"price\":24  }}')
testDraftSetupEvent = json.loads("{ \"body\": {\"draftName\":\"2019 Draft\",\"budget\":200,\"leagueSize\":12,\"teams\":[" \
           "{\"ownerName\":\"Pat Vessels\",\"teamName\":\"Gunslingers\",\"remainingBudget\":200,\"draftOrder\":1,\"isAdmin\":true}," \
           "{\"ownerName\":\"Wayne Bryan\",\"teamName\":\"Smack\",\"remainingBudget\":200,\"draftOrder\":2,\"isAdmin\":true}," \
           "{\"ownerName\":\"Tim Bryan\",\"teamName\":\"Diablos\",\"remainingBudget\":200,\"draftOrder\":3,\"isAdmin\":false}," \
           "{\"ownerName\":\"Dan Mayer \",\"teamName\":\"Bud Light Man\",\"remainingBudget\":200,\"draftOrder\":4,\"isAdmin\":false}," \
           "{\"ownerName\":\"Max Fregoso\",\"teamName\":\"Corn Bread\",\"remainingBudget\":200,\"draftOrder\":5,\"isAdmin\":false}," \
           "{\"ownerName\":\"Ed Garcia\",\"teamName\":\"Davids Revenge\",\"remainingBudget\":200,\"draftOrder\":6,\"isAdmin\":false}," \
           "{\"ownerName\":\"Weston Bryant\",\"teamName\":\"En Vogue\",\"remainingBudget\":200,\"draftOrder\":7,\"isAdmin\":false}," \
           "{\"ownerName\":\"Jeff Fregoso \",\"teamName\":\"SKOL\",\"remainingBudget\":200,\"draftOrder\":8,\"isAdmin\":false}," \
           "{\"ownerName\":\"David Turner\",\"teamName\":\"Boss Man II\",\"remainingBudget\":200,\"draftOrder\":9,\"isAdmin\":false}," \
           "{\"ownerName\":\"Randy Fregoso\",\"teamName\":\"Smokey\",\"remainingBudget\":200,\"draftOrder\":10,\"isAdmin\":false}," \
           "{\"ownerName\":\"Scott Mayer\",\"teamName\":\"Bud Heavy\",\"remainingBudget\":200,\"draftOrder\":11,\"isAdmin\":false}," \
           "{\"ownerName\":\"Lee Bryan\",\"teamName\":\"Big Daddy\",\"remainingBudget\":200,\"draftOrder\":12,\"isAdmin\":false}]}}");


# data = getPlayers(testEvent, "null")
# y = json.loads(data['body'])
# print(y)

# highestPick = getCurrentDraftPosition()
# print('Highest Pick = ' + str(highestPick))
# saveDraftPick(debugEvent,"null")
# saveDraftPick(draftedPlayerEvent2,"null")
# print(getDraftedPlayers("dummy","dummy"))
# undoLastPick("dummy","dummy")
# print(getDraftedPlayers("dummy","dummy"))
# undoLastPick("null", "null")

# highestPick = getCurrentDraftPosition()
# print('Highest Pick = ' + str(highestPick))

# response = saveDraftInfo(testDraftSetupEvent,"null")
