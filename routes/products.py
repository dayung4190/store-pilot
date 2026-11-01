from flask import Blueprint, jsonify, request
from bson import ObjectId
from database import products_collection

products_bp = Blueprint("products", __name__)


# GET: Retrieve all products
@products_bp.route("/", methods=["GET"])
def get_products():
    products = list(products_collection.find())

    for product in products:
        product["_id"] = str(product["_id"])

    return jsonify(products), 200


# GET: Retrieve one product by its MongoDB ID
@products_bp.route("/<product_id>", methods=["GET"])
def get_product(product_id):
    if not ObjectId.is_valid(product_id):
        return jsonify({"error": "Invalid product ID"}), 400

    product = products_collection.find_one({
        "_id": ObjectId(product_id)
    })

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    product["_id"] = str(product["_id"])
    return jsonify(product), 200
# POST: Add a new product with validation
@products_bp.route("/", methods=["POST"])
def add_product():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send product data as a JSON object"
        }), 400

    required_fields = ["name", "sku", "quantity", "price"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({
            "error": "Product name must be a non-empty string"
        }), 400

    if not isinstance(data["sku"], str) or not data["sku"].strip():
        return jsonify({
            "error": "SKU must be a non-empty string"
        }), 400

    sku = data["sku"].strip().upper()

    if products_collection.find_one({"sku": sku}):
        return jsonify({
            "error": "A product with this SKU already exists"
        }), 409

    if type(data["quantity"]) is not int or data["quantity"] < 0:
        return jsonify({
            "error": "Quantity must be a whole number greater than or equal to zero"
        }), 400

    if (
        isinstance(data["price"], bool)
        or not isinstance(data["price"], (int, float))
        or data["price"] < 0
    ):
        return jsonify({
            "error": "Price must be a number greater than or equal to zero"
        }), 400

    product = {
        "name": data["name"].strip(),
        "sku": sku,
        "quantity": data["quantity"],
        "price": data["price"]
    }

    result = products_collection.insert_one(product)

    return jsonify({
        "message": "Product added successfully",
        "product_id": str(result.inserted_id)
    }), 201
# PUT: Update an existing product
@products_bp.route("/<product_id>", methods=["PUT"])
def update_product(product_id):
    if not ObjectId.is_valid(product_id):
        return jsonify({"error": "Invalid product ID"}), 400

    existing_product = products_collection.find_one({
        "_id": ObjectId(product_id)
    })

    if existing_product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send product data as a JSON object"
        }), 400

    allowed_fields = ["name", "sku", "quantity", "price"]
    updates = {}

    for field in allowed_fields:
        if field in data:
            updates[field] = data[field]

    if not updates:
        return jsonify({
            "error": "Please provide at least one field to update"
        }), 400

    if "name" in updates:
        if not isinstance(updates["name"], str) or not updates["name"].strip():
            return jsonify({
                "error": "Product name must be a non-empty string"
            }), 400

        updates["name"] = updates["name"].strip()

    if "sku" in updates:
        if not isinstance(updates["sku"], str) or not updates["sku"].strip():
            return jsonify({
                "error": "SKU must be a non-empty string"
            }), 400

        updates["sku"] = updates["sku"].strip().upper()

        duplicate_sku = products_collection.find_one({
            "sku": updates["sku"],
            "_id": {"$ne": ObjectId(product_id)}
        })

        if duplicate_sku:
            return jsonify({
                "error": "Another product already uses this SKU"
            }), 409

    if "quantity" in updates:
        if type(updates["quantity"]) is not int or updates["quantity"] < 0:
            return jsonify({
                "error": "Quantity must be a whole number greater than or equal to zero"
            }), 400

    if "price" in updates:
        price = updates["price"]

        if (
            isinstance(price, bool)
            or not isinstance(price, (int, float))
            or price < 0
        ):
            return jsonify({
                "error": "Price must be a number greater than or equal to zero"
            }), 400

    products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": updates}
    )

    updated_product = products_collection.find_one({
        "_id": ObjectId(product_id)
    })

    updated_product["_id"] = str(updated_product["_id"])

    return jsonify({
        "message": "Product updated successfully",
        "product": updated_product
    }), 200
# DELETE: Remove a product by its MongoDB ID
@products_bp.route("/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    if not ObjectId.is_valid(product_id):
        return jsonify({"error": "Invalid product ID"}), 400

    product = products_collection.find_one({
        "_id": ObjectId(product_id)
    })

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    products_collection.delete_one({
        "_id": ObjectId(product_id)
    })

    return jsonify({
        "message": "Product deleted successfully",
        "product_id": product_id
    }), 200