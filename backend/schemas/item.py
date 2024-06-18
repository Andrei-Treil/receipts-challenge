class Item:
    def __init__(self, shortDescription: str, price: str):
        '''
        Object representing a receipt item

        `shortDescription`:
            description: The Short Product Description for the item.
            type: string
            pattern: "^[\\w\\s\\-]+$"
            example: "Mountain Dew 12PK"
        `price`:
            description: The total price payed for this item.
            type: string
            pattern: "^\\d+\\.\\d{2}$"
            example: "6.49"
        '''
        self.shortDescription = shortDescription
        self.price = price