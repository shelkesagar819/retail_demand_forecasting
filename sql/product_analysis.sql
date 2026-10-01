SELECT
    Product_ID,
    AVG(Inventory_Level) AS Average_Inventory,
    SUM(Units_Sold) AS Total_Units_Sold,
    SUM(Units_Ordered) AS Total_Units_Ordered
FROM sales_data
GROUP BY Product_ID
ORDER BY Total_Units_Sold DESC
LIMIT 10;