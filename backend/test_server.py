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