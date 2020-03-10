

insert into product (id, name, in_stock, price) values
('fbbf6840-5ba4-11ea-a188-0242c0a83003', 'Liilia', 10, 3.75),
('fbbf7290-5ba4-11ea-a188-0242c0a83003', 'Krüsanteemid', 20, 1.99),
('fbbf7344-5ba4-11ea-a188-0242c0a83003' ,'Ülane', 30, .37)
;

insert into "order" (id) VALUES
('54d070b0-5bc7-11ea-9577-0242c0a8e003'),
('54d3722e-5bc7-11ea-9577-0242c0a8e003'),
('54d4fff4-5bc7-11ea-9577-0242c0a8e003')
;

insert into order_item (order_id, product_id, quantity) values
('54d070b0-5bc7-11ea-9577-0242c0a8e003', 'fbbf6840-5ba4-11ea-a188-0242c0a83003', 3),
('54d070b0-5bc7-11ea-9577-0242c0a8e003', 'fbbf7290-5ba4-11ea-a188-0242c0a83003', 7),
('54d070b0-5bc7-11ea-9577-0242c0a8e003', 'fbbf7344-5ba4-11ea-a188-0242c0a83003', 1),
('54d3722e-5bc7-11ea-9577-0242c0a8e003', 'fbbf7290-5ba4-11ea-a188-0242c0a83003', 9)
;
