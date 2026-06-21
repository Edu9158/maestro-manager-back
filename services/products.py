"""
Products business logic.
"""
from datetime import datetime
from database.mongo_client import Db


def serialize_document(document):
    """
    Convert Mongo documents into JSON-serializable dictionaries.
    """
    if document is None:
        return None

    serialized = dict(document)
    serialized["_id"] = str(serialized["_id"])
    return serialized


def create_product(payload):
    """
    Validate and save a new product to the database.
    """
    if not isinstance(payload, dict):
        raise ValueError("The request body must be a JSON object.")

    required_fields = ["sku", "name"]
    missing_fields = [field for field in required_fields if not payload.get(field)]
    if missing_fields:
        raise ValueError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )

    try:
        price = float(payload.get("price", 0))
        current_stock = int(payload.get("current_stock", 0))
    except (TypeError, ValueError):
        raise ValueError("price and current_stock must be numeric values.")

    product_data = {
        "sku": str(payload["sku"]).strip(),
        "name": str(payload["name"]).strip(),
        "category": payload.get("category", ""),
        "color": payload.get("color", ""),
        "brand": payload.get("brand", ""),
        "price": price,
        "weight": payload.get("weight", ""),
        "current_stock": current_stock,
        "unit": payload.get("unit", "un"),
        "load_date": payload.get("load_date") or datetime.utcnow().isoformat(),
    }

    db = Db()
    inserted_id = db.insert_one_document("product", product_data)

    if not inserted_id:
        raise RuntimeError("Failed to create product in the database.")

    response_product = dict(product_data)
    response_product.pop("_id", None)

    return {
        "id": str(inserted_id),
        "product": response_product,
    }


def list_products():
    """
    List all products from the database.
    """
    db = Db()
    products = db.db["product"].find({})
    return [serialize_document(product) for product in products]

