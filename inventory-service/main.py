from fastapi import FastAPI

app = FastAPI(title="Inventory Service")

inventory = [
    {"id": 1, "name": "Laptop", "quantity": 10},
    {"id": 2, "name": "Monitor", "quantity": 5},
    {"id": 3, "name": "Keyboard", "quantity": 20}
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/inventory")
def get_inventory():
    return {"inventory": inventory}


@app.get("/inventory/{item_id}")
def get_item(item_id: int):
    for item in inventory:
        if item["id"] == item_id:
            return item

    return {"error": "Item not found"}