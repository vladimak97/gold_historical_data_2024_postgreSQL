**NASDAQ Gold (GCCMX) Historical Data for 2024**

This dataset offers intermediate-level exercises in PostgreSQL, using NASDAQ Gold (GCCMX) Historical Data from 2024.

**1. Find the date with the highest volatility, defined as the difference between the highest (High) and lowest (Low) prices for a single day.**

'SELECT Date, (High - Low) AS Volatility'
FROM goldhistoricaldata
ORDER BY Volatility DESC
LIMIT 1;

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F17427131%2Fb8d2c1df39004258f2c53652f97b24ab%2Fimage_2024-07-01_132702659.png?generation=1719833223404021&alt=media)

**2. Calculate the average daily trading volume for days where the closing price is within 5% of the highest closing price in the dataset.**

&gt;SELECT AVG(Volume) AS AvgVolume
FROM goldhistoricaldata
WHERE CloseLast &gt;= (SELECT MAX(CloseLast) * 0.95 FROM goldhistoricaldata);

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F17427131%2F10728d906915232e516bb8d7267afd55%2F2.png?generation=1719833286506706&alt=media)

**3. Identify dates where the opening price was lower than the closing price by more than $50.**

&gt;SELECT Date, Open, CloseLast, (CloseLast - Open) AS PriceDifference
FROM goldhistoricaldata
WHERE (Open - CloseLast) &gt; 50;

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F17427131%2F0ad30544168334e633d9c34ff2bc8e8f%2F3.png?generation=1719833332255048&alt=media)

**4. Find the date with the highest total trading volume in a single day.**

&gt;SELECT Date, SUM(Volume) AS TotalVolume
FROM goldhistoricaldata
GROUP BY Date
ORDER BY TotalVolume DESC
LIMIT 1;

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F17427131%2F0105c1f9a7ab62bab6bd3514d5e39367%2F4.png?generation=1719833418785741&alt=media)

**5. Calculate the percentage change in the average closing price between the first and last 10 days of available data.**

&gt;WITH AvgClosing AS (
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

![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F17427131%2F28e15718cc260cc2b650d6cb7fa59d6d%2F5.png?generation=1719833769210664&alt=media)
