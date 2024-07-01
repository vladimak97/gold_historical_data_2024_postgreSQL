
-- 1. Find the date with the highest volatility, defined as the difference 
-- between the highest (High) and lowest (Low) prices for a single day.

SELECT Date, (High - Low) AS Volatility
FROM goldhistoricaldata
ORDER BY Volatility DESC
LIMIT 1;

-- 2. Calculate the average daily trading volume for days where the closing price 
-- is within 5% of the highest closing price in the dataset.

SELECT AVG(Volume) AS AvgVolume
FROM goldhistoricaldata
WHERE CloseLast >= (SELECT MAX(CloseLast) * 0.95 FROM goldhistoricaldata);

-- 3. Identify dates where the opening price was lower than the 
-- closing price by more than $50.

SELECT Date, Open, CloseLast, (CloseLast - Open) AS PriceDifference
FROM goldhistoricaldata
WHERE (Open - CloseLast) > 50;

-- 4. Find the date with the highest total trading volume in a single day.

SELECT Date, SUM(Volume) AS TotalVolume
FROM goldhistoricaldata
GROUP BY Date
ORDER BY TotalVolume DESC
LIMIT 1;

-- 5. Calculate the percentage change in the average closing price 
-- between the first and last 10 days of available data.

WITH AvgClosing AS (
    SELECT
        (SELECT AVG(CloseLast) FROM (
            SELECT CloseLast
            FROM goldhistoricaldata
            ORDER BY Date ASC
            LIMIT 10
        )) AS First10AvgClose,
        (SELECT AVG(CloseLast) FROM (
            SELECT CloseLast
            FROM goldhistoricaldata
            ORDER BY Date DESC
            LIMIT 10
        )) AS Last10AvgClose
)
SELECT 
    ((AvgClosing.Last10AvgClose - AvgClosing.First10AvgClose) / AvgClosing.First10AvgClose) * 100 AS PercentageChange
FROM AvgClosing;

