
-- install extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE product
(
    id UUID NOT NULL DEFAULT uuid_generate_v1(),
    name TEXT,
    in_stock INT NOT NULL DEFAULT 0,
    price NUMERIC(8,3) NOT NULL DEFAULT 0,
    CONSTRAINT product_pkey PRIMARY KEY (id)
);


CREATE TABLE "order"
(
    id UUID NOT NULL DEFAULT uuid_generate_v1(),
    time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    CONSTRAINT order_pkey PRIMARY KEY (id)
);


CREATE TABLE order_item
(
    id SERIAL PRIMARY KEY,
    order_id UUID NOT NULL REFERENCES "order"(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES product(id) ON DELETE CASCADE,
    quantity INT NOT NULL,
    price NUMERIC(8,3),
    amount NUMERIC(8,3) NOT NULL DEFAULT 0
);

CREATE INDEX order_item_product_id_index ON order_item (product_id);


CREATE OR REPLACE FUNCTION calculate_order_item_amount() RETURNS TRIGGER AS
$$
DECLARE
    diff INT := 0;
BEGIN

    IF NEW.price IS NULL THEN
        -- Get item price
        NEW.price = (SELECT price FROM product WHERE id = NEW.product_id);
    END IF;

    -- Calculate amount
    NEW.amount := NEW.quantity * NEW.price;

    -- Update item in stock
    IF (TG_OP = 'DELETE') THEN
        UPDATE product SET in_stock = in_stock + OLD.quantity WHERE id = OLD.product_id;
    ELSIF (TG_OP = 'UPDATE') THEN
        diff = NEW.quantity - OLD.quantity;
        UPDATE product SET in_stock = in_stock - diff WHERE id = NEW.product_id;
    ELSE
        -- INSERT
        UPDATE product SET in_stock = in_stock - NEW.quantity WHERE id = NEW.product_id;
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER calculate_order_item_amount_trigger BEFORE INSERT OR UPDATE OR DELETE
ON order_item FOR EACH ROW EXECUTE PROCEDURE calculate_order_item_amount();
