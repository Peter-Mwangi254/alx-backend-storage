-- Creates a trigger that decreases the quantity
-- of an item after adding a new order
-- New is a MySQL extension to triggers
-- enabling access to columns in the rows affected by a trigger

DELIMITER //

CREATE TRIGGER decrease_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - NEW.number
	WHERE name = NEW.item_name;
END;
//

DELIMITER ;
