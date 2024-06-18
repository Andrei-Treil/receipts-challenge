from schemas.item import Item
from schemas.receipt import Receipt
from flask import request, Flask
import uuid

app = Flask(__name__)

# Store receipts mapping ID -> receipt
RECEIPTS = {}

@app.route('/receipts/process', methods=['POST'])
def submitReceipt():
    '''
    Submits a receipt for processing

    Example receipt:
    {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "total": "1.25",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
        ]
    }

    Response:
        - 200 (success): returns the ID assigned to the receipt, EX:
            {
                "id": "adb6b560-0eef-42bc-9d16-df48f30e89b2"
            }
        - 400 (failure): The receipt is invalid
    '''

    try:
        content = request.get_json()
        receipt = Receipt(retailer=content['retailer'],purchaseDate=content['purchaseDate'],
                          purchaseTime=content['purchaseTime'],items=content['items'],
                          total=content['total'])
        new_id = str(uuid.uuid4())
        RECEIPTS[new_id] = receipt
        return {'id': new_id}, 200
    except Exception as e:
        return {'ERROR': f'{e}', 'Message': 'Invlaid Receipt'},400
    
@app.route('/receipts/<id>/points', methods=['GET'])
def getPoints(id):
    '''
    Gets the points for the receipt associated with `id`, returns 404 if no receipt is found

    Response:
        - 200 (sucesss): returns the points of the receipt associated with `id`, EX:
            {
                "points": 100
            }
        - 404 (failure): No receipt associated with `id`
    '''
    try:
        return {'points': RECEIPTS[id].points}, 200

    except KeyError as e:
        return {'ERROR': f'No receipt associated with id: {id}'}, 404
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)