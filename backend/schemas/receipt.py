from schemas.item import Item
import re
import math
from datetime import datetime

class Receipt:
    def __init__(self, retailer: str, purchaseDate: str, purchaseTime: str, items: list[Item], total: str):
        '''
        Object representing a receipt, calculates points according to the following rules:
        - One point for every alphanumeric character in the retailer name.
        - 50 points if the total is a round dollar amount with no cents.
        - 25 points if the total is a multiple of 0.25.
        - 5 points for every two items on the receipt.
        - If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
        - 6 points if the day in the purchase date is odd.
        - 10 points if the time of purchase is after 2:00pm and before 4:00pm.

        ARGS:

        `retailer`:
            description: The name of the retailer or store the receipt is from.
            type: string
            pattern: "^[\\w\\s\\-&]+$"
            example: "M&M Corner Market"

        `purchaseDate`:
            description: The date of the purchase printed on the receipt.
            type: string
            format: date
            example: "2022-01-01"

        `purchaseTime`:
            description: The time of the purchase printed on the receipt. 24-hour time expected.
            type: string
            format: time
            example: "13:01"

        `items`:
            type: array
            minItems: 1
            items:
                $ref: "#/components/schemas/Item"

        `total`:
            description: The total amount paid on the receipt.
            type: string
            pattern: "^\\d+\\.\\d{2}$"
            example: "6.49"
        '''
        self.retailer = retailer
        self.purchaseDate = datetime.strptime(purchaseDate, "%Y-%m-%d").date()
        self.purchaseTime = datetime.strptime(purchaseTime, "%H:%M").time()

        # Convert item JSON to Item objects
        self.items = []
        for item in items:
            self.items.append(Item(shortDescription=item['shortDescription'],price=item['price']))

        self.total = total
        self.points = 0

        # Calculate points and assign to this receipt
        self.points += len(re.findall(r"[a-zA-Z0-9]", retailer)) # 1 point for every alphanumeric char in retailer

        if total[-2:] == "00": # 50 points if total is a round dollar amount
            self.points += 50

        if int(total[-2:]) % 25 == 0: # 25 points if total is a multiple of 0.25
            self.points += 25

        self.points += 5 * (len(items) // 2) # 5 points for every 2 items

        for item in self.items:
            trimDesc = item.shortDescription.strip() # removing leading and trailing whitespace
            if len(trimDesc) % 3 == 0: # if trimmed length is a mult of 3, add price * 0.2, round up
                self.points += math.ceil(float(item.price) * 0.2)

        if self.purchaseDate.day % 2 != 0: # 6 points if purchase day is odd
            self.points += 6

        if (self.purchaseTime > datetime.strptime("14:00", "%H:%M").time() and 
            self.purchaseTime < datetime.strptime("16:00", "%H:%M").time()):
            # 10 points if purchase time is after 2pm and before 4pm
            self.points += 10
