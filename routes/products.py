"""
Products routes.
"""
from flask import Blueprint, jsonify, request
from services.products import create_product, list_products

bpProducts = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)


@bpProducts.route("", methods=["POST"])
def create_product_route():
    payload = request.get_json(silent=True) or {}

    try:
        result = create_product(payload)
        return jsonify({
            "success": True,
            "data": result
        }), 201
    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400
    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@bpProducts.route("", methods=["GET"])
def list_products_route():
    try:
        products = list_products()
        return jsonify({
            "success": True,
            "data": products
        }), 200
    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500
