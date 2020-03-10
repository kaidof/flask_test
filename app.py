import werkzeug
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_uuid import FlaskUUID
from product import Product
from order import Order

app = Flask(__name__, static_url_path='/static', static_folder='public', instance_relative_config=False)
FlaskUUID(app)

app.config.from_object('config.Config')
db = SQLAlchemy()


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/product/<uuid:product_id>', methods=['GET'])
def product_get(product_id):
    prod = Product.query.get(product_id)

    if prod is None:
        return jsonify({'error': 'Product not found'}), 404

    return prod.serialize()


@app.route('/products', methods=['GET'])
def products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        product_list = Product.query.paginate(page=page, per_page=per_page)
        return jsonify([item.serialize() for item in product_list.items])
    except werkzeug.exceptions.NotFound:
        return jsonify({'error': 'Orders not found'}), 404


@app.route('/order/<uuid:order_id>', methods=['GET'])
def order(order_id):
    item: Order = Order.query.get(order_id)

    if item is None:
        return jsonify({'error': 'Order not found'}), 404

    item.load_items()
    return item.serialize()


@app.route('/orders', methods=['GET'])
def orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        order_list = Order.query.paginate(page=page, per_page=per_page)
        return jsonify([item.load_items().serialize() for item in order_list.items])
    except werkzeug.exceptions.NotFound:
        return jsonify({'error': 'Orders not found'}), 404


@app.route("/related_products/<uuid:product_id>", methods=["GET"])
def related(product_id):
    result = db.session.execute("SELECT product_id, COUNT(*) AS c FROM order_item WHERE order_id IN "
                                "(SELECT order_id FROM order_item WHERE product_id = :id) "
                                "AND product_id <> :id "
                                "GROUP BY 1 ORDER BY 2 DESC", {
                                    "id": product_id
                                })

    if not result.rowcount:
        return jsonify([])

    return jsonify([dict(row)["product_id"] for row in result])


@app.route('/product/<uuid:product_id>', methods=['PATCH'])
def product_patch(product_id):
    item: Product = Product.query.get(product_id)

    if item is None:
        return jsonify({'error': 'Product not found'}), 404

    if 'name' in request.json.keys():
        item.name = request.json['name']

    if 'price' in request.json.keys():
        item.price = float(request.json['price'])

    db.session.merge(item)
    db.session.flush()
    db.session.commit()

    return item.serialize()


if __name__ == '__main__':
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000)
