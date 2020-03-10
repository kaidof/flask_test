#!/usr/bin/python3

import sys
from sqlalchemy import create_engine
import random
import time
from datetime import datetime
from sqlalchemy.sql import text
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)


def main(argv):
    # Output help text if no params
    if len(argv) is 0:
        txt = "\n".join([
            '',
            '*' * 20,
            '*  Data generator  *',
            '*' * 20,
            '',
            'Usage: gen.py [OPTIONS] [COUNT]',
            '',
            'Options are',
            '  -p, --product    generate new products',
            '  -o, --order      generate new orders',
            '  COUNT            99 is max records at a time, default is 20',
            '',
            'Examples:',
            '  $ python gen.py -p 50',
            '    will generate 50 new products',
            '',
        ])

        print(txt)
        return

    # Product generation
    if ("-p" or "--product") in argv:
        how_many = get_how_many(argv)
        print("  Product generation, {} items...".format(how_many))

        name_parts = ["al", "ver", "to", "ur", "la", "mar"]
        with engine.connect() as con:
            statement = text("INSERT INTO product (name, in_stock, price) VALUES(:name, :in_stock, :price)")

            transaction = con.begin()
            for _ in range(how_many):
                fake_name = "".join(random.choice(name_parts) for _ in range(random.randint(2, 8)))
                fake_in_stock = random.randint(0, 100)
                fake_price = round(random.uniform(0.1, 10), 2)

                con.execute(statement, {"name": fake_name, "in_stock": fake_in_stock, "price": fake_price})

            try:
                transaction.commit()
            except Exception:
                transaction.rollback()
                raise

        print("  Done!\n")

    # Order generation
    if ("-o" or "--order") in argv:
        how_many = get_how_many(argv)
        print("  Order generation, {} items...".format(how_many))

        current_timestamp = int(time.time())
        max_past_sec = 365 * 24 * 3600  # 1 year back

        with engine.connect() as con:
            for _ in range(how_many):
                transaction = con.begin()

                items_in_order = random.randint(1, 9)

                try:
                    # select new order product id's
                    product_rs = con.execute("SELECT id FROM product ORDER BY random() LIMIT {}".format(items_in_order))

                    if not product_rs.rowcount:
                        print("No PRODUCT's in table! Generate products first.")
                        return

                    # Create order
                    order_time = datetime.fromtimestamp(current_timestamp - random.randint(0, max_past_sec)).isoformat()
                    order_statement = text('INSERT INTO "order" (time) VALUES (:time) RETURNING id')
                    rs = con.execute(order_statement, {"time": order_time})

                    order_id = dict(list(rs).pop(0))["id"]

                    for row in product_rs:
                        product_id = dict(row)["id"]
                        items_quantity = random.randint(1, 15)
                        print('  id: {}, items: {}'.format(product_id, items_quantity))
                        order_item_statement = text('INSERT INTO order_item (order_id, product_id, quantity) VALUES '
                                                    '(:order_id, :product_id, :quantity)')
                        con.execute(order_item_statement, {
                            "order_id": order_id,
                            "product_id": product_id,
                            "quantity": items_quantity
                        })

                    transaction.commit()
                except Exception:
                    transaction.rollback()
                    raise

        print("  Done!\n")


def get_how_many(argv):
    """Return how many new items to insert"""
    how_many = 20  # default is 20 items

    if argv and len(argv) > 1 and argv[1].isdigit() and int(argv[1]):
        how_many = int(argv[1])
        if how_many > 99:
            how_many = 99

    return how_many


if __name__ == "__main__":
    main(sys.argv[1:])
