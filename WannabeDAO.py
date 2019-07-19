import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr
from DataTypes.DraftRecord import DraftRecord

# import requests

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError


def getCurrentDraftPosition():
    draftIndex=[]

    for item in queryPlayers('all','drafted'):
        draftIndex.append(item['wannabeDraftPick'])

    maxPick = max(draftIndex)
    return maxPick

def saveDraftPick(event, context):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('players')
    body = event['body']
    position = body['position']
    name = body['playerName']
    owner = body['owner']
    price = body['price']
    record = table.get_item(
        Key = {
            'position': position,
            'playerName': name
        }
    )['Item']

    record['wannabeOwner'] = owner
    record['wannabeDraftPick'] = getCurrentDraftPosition() + 1
    record['wannabePrice'] = price

    table.put_item(Item = record, ConditionExpression = Attr('wannabePrice').eq(-1))
    # table.put_item(Item=record)

def saveDraftInfo(event, context):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('DraftStatus')
    print("In saveDraftInfo")
    print(event)

    # Remove existing records
    records = table.scan()['Items']
    for record in records:
        table.delete_item(Key = {
            'ownerName': record['ownerName'],
            'teamName': record['teamName']
        })

    print("Records Removed")

    body = event['body']
    draftname = body['draftName']
    budget = body['budget']
    leagueSize = body['leagueSize']
    ownerRecords = body['teams']

    print("Adding new records")
    for record in ownerRecords:
        itemToStore = DraftRecord(draftname, record)
        itemToStore.draftName = draftname
        itemToStore.budget = budget

        table.put_item(Item=record)

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

# Get Players. Gets a set of players
#
# Body Parameters:
#   - position (all, QB, RB, TE, WR, DST, K)
#   - playerList (all, drafted, available)
def getPlayers(event, context):
    position = event['queryStringParameters']['position']
    playerList = event['queryStringParameters']['playerList']
    print('request = ', position, playerList)

    # players = queryPlayers(position, playerList)
    players = sorted(queryPlayers(position, playerList), key=lambda x: x['fantasyPoints'], reverse=True)
    jsonData = json.dumps(players, default=decimal_default)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": jsonData
    }

def queryPlayers(position, playerList):
    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('players')

    if position == 'all':
        positionAttribute = Attr('position').between('AAA','ZZZ)')
    else:
        positionAttribute = Attr('position').eq(position)

    if playerList == 'drafted':
        filterAttribute = Attr('wannabeDraftPick').gt(0)
    if playerList == 'available':
        filterAttribute = Attr('wannabeDraftPick').eq(-1)
    if playerList == 'all':
        filterAttribute = Attr('wannabeDraftPick').gt(-2)

    pointsAttribute = Attr('fantasyPoints').gt(0)

    response = table.scan(
        IndexName='position-fantasyPoints-index',
        FilterExpression=filterAttribute & positionAttribute & pointsAttribute,
    )
    players = response['Items']
    return players

def undoLastPick(event, context):
    highestPick = getCurrentDraftPosition()

    draftedPlayers = queryPlayers('all', 'drafted')
    for player in draftedPlayers:
        if highestPick == player['wannabeDraftPick']:
            lastPlayerPicked = player

    lastPlayerPicked['wannabeOwner'] = 'none'
    lastPlayerPicked['wannabeDraftPick'] = -1
    lastPlayerPicked['wannabePrice'] = -0


    dynamodb = boto3.resource(service_name='dynamodb', region_name='us-west-2')
    table = dynamodb.Table('players')
    table.put_item(Item=lastPlayerPicked)

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
# saveDraftPick(testDraftEvent,"null")
# undoLastPick("null", "null")

# highestPick = getCurrentDraftPosition()
# print('Highest Pick = ' + str(highestPick))

# response = saveDraftInfo(testDraftSetupEvent,"null")
