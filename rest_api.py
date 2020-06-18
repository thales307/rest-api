import json

class RestAPI:
    def findUser(self, name):
        for person in self.database['users']:
            if person['name'] == name:
                return person

    def getUsers(self, data):
        insert_data = {"name": data['user'], "owes": {}, "owed_by": {}, "balance": 0.0}
        self.database['users'].append(insert_data)
        return json.dumps(insert_data)

    def sortOwes(self, person1, person2, amount, mode, altMode):
        if person1['name'] in person2[mode]:
            change = person2[mode][person1['name']] - amount
            if change <= 0:
                del person2[mode][person1['name']]
                change *= -1
            else:
                person2[mode][person1['name']] = change
                change = 0
        else:
            change = amount  
        if change != 0:
            person2[mode == 'owes' and 'owed_by' or 'owes'][person1['name']] = change

    def setIOU(self, data):
        lender = self.findUser(data['lender'])
        borrower = self.findUser(data['borrower'])
        amount = data['amount']
        
        self.sortOwes(borrower, lender, amount, 'owes', 'owed_by')
        self.sortOwes(lender, borrower, amount, 'owed_by','owes')
        
        lender['balance'] += amount
        borrower['balance'] -= amount
        return json.dumps({'users': sorted([lender, borrower], key = lambda i: i['name'])})

    def __init__(self, database=None):
        self.database = database

    def get(self, url, payload=None):
        if url == '/users':
            if not payload:
                return json.dumps({"users": self.database['users']})
            else:
                data = json.loads(payload)
                result = list(filter(lambda x: x['name'] in data['users'] ,self.database['users']))
                return json.dumps({'users': result})

    def post(self, url, payload=None):
        data = json.loads(payload)
        if url == '/add':
            return self.getUsers(data)
        if url == '/iou':
            return self.setIOU(data)
            