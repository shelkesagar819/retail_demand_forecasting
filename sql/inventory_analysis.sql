SELECT
    Product_ID,
    AVG(Inventory_Level) AS Average_Inventory,
    AVG(Demand_Forecast) AS Average_Demand,
    AVG(Inventory_Level) - AVG(Demand_Forecast) AS Inventory_Demand_Gap
FROM sales_data
GROUP BY Product_ID
ORDER BY Inventory_Demand_Gap ASC
LIMIT 10;