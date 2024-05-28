from enum import Enum

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Items API",
    description="We created an api for using items.",
    version="0.1.0",
)


class Category(Enum):
    """Category of an item"""

    TOOLS = "tools"
    CONSUMABLES = "consumables"


class Item(BaseModel):
    """Representation of an item in the system."""

    id: int = Field(description="Unique integer that specifies this item.")
    name: str = Field(description="Name of the item.")
    price: float = Field(description="Price of the item in Euro.")
    count: int = Field(description="Amount of instances of this item in stock.")
    category: Category = Field(description="Category this item belongs to.")


items = {
    1: Item(id=1, name="Hammer", price=9.99, count=20, category=Category.TOOLS),
    2: Item(id=2, name="Pliers", price=5.99, count=20, category=Category.TOOLS),
    3: Item(id=3, name="Nails", price=1.99, count=100, category=Category.CONSUMABLES),
}


@app.get("/")
def index():
    content = """
    <h1>Welcome to my API</h1>
    <p>Please check the <a href="http://127.0.0.1:8000/docs">documentation</a> page.</p>
    """
    return HTMLResponse(content)


@app.get("/items/all")
def get_items() -> dict[str, dict[int, Item]]:
    return {"items": items}


@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exist."
        )
    return items[item_id]


Selection = dict[str, str | int | float | Category | None]


@app.get("/items/")
def query_item_by_parameter(
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None,
) -> dict[str, Selection | list[Item]]:
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or name.lower() in item.name.lower(),
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category is category,
            )
        )

    selection = list(filter(check_item, items.values()))
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }


@app.post("/items/")
def add_item(item: Item) -> dict[str, Item]:
    if item.id in items:
        raise HTTPException(
            status_code=400, detail=f"Item with {item.id=} already exists."
        )

    items[item.id] = item
    return {"added": item}


# Path() : used for path string
# Query(): used for query string
@app.put("/items/{item_id}")
def update_item(
    item_id: int = Path(ge=0),
    name: str | None = Query(default=None, min_length=1, max_length=8),
    price: float | None = Query(default=None, gt=0.0),
    count: int | None = Query(default=None, gt=0),
) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exists."
        )
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for updates."
        )

    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return {"updated": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exists."
        )

    item = items.pop(item_id)
    return {"deleted": item}
