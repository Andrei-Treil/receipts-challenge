import pytest
from pathlib import Path
from server import app
import json

app.config.update({
    "TESTING": True
})

examplesPath = Path(__file__).parent.parent / "examples"

client = app.test_client()

examples = []

for file in examplesPath.iterdir():
    examples.append(json.loads(file.read_text()))

@pytest.mark.parametrize("receipt", examples)
def testExamples(receipt):
    response = client.post("receipts/process", json=receipt)
    assert response.status_code == 200
    assert "id" in response.json

    response = client.get(f"receipts/{response.json['id']}/points")
    assert response.status_code == 200
    assert response.json["points"] == receipt["points"]

@pytest.mark.parametrize("id", ['1','2','3'])
def testBadId(id):
    response = client.get(f"receipts/{id}/points")
    assert response.status_code == 404

@pytest.mark.parametrize("json",[{ "badKey": 1010},
                        {"badderKey": True,"worseKey": ""}])

def testBadJson(json):
    response = client.post("receipts/process", json=json)
    assert response.status_code == 400