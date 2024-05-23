-- TRIGGER to calculate Amount paid in transaction according to row inserted in ORDERS
DELIMITER //

CREATE TRIGGER set_total_amount
AFTER INSERT ON ORDERS
FOR EACH ROW
BEGIN
    DECLARE Amount DECIMAL(10,2);
    
    SELECT SUM(items.Quantity * prod.Price - NEW.discount ) INTO Amount
    FROM OrderItems items
    INNER JOIN Products prod ON items.Product_ID = prod.Product_ID
    WHERE items.Order_ID = NEW.Order_ID;

    UPDATE TRANSACTIONS T
    SET T.Amount_paid = Amount 
    WHERE order_id = NEW.order_id;
END;
//

DELIMITER ;

-- Trigger2: including the cart items into the order_items table 
-- to link the products ordered with the order_id of the order just placed by the user
DELIMITER // 
CREATE TRIGGER update_order_items_table
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
  INSERT INTO orderItems (Order_ID, Product_ID, Quantity)
  SELECT NEW.Order_ID, C.Product_ID, C.Quantity
  FROM cart C
  WHERE C.Customer_ID = NEW.Customer_ID;

  DELETE FROM Cart C
  WHERE C.Customer_ID = NEW.Customer_ID;
END;
//
DELIMITER ;
    