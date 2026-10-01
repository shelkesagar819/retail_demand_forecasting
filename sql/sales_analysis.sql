SELECT
    Weather_Condition,
    SUM(Units_Sold) AS Total_Units_Sold
FROM sales_data
GROUP BY Weather_Condition
ORDER BY Total_Units_Sold DESC;