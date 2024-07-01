import sqlite3

# Connect to database
conn = sqlite3.connect('goldhistoricaldata.db')
cursor = conn.cursor()

# 1. Find the date with the highest volatility, defined as the difference 
# between the highest (High) and lowest (Low) prices for a single day.

query1 = """
SELECT Date, (High - Low) AS Volatility
FROM goldhistoricaldata
ORDER BY Volatility DESC
LIMIT 1;
"""
cursor.execute(query1)
result1 = cursor.fetchone()
print("Date with highest volatility: {} Volatility: {}".format(result1[0], result1[1]))

# 2. Calculate the average daily trading volume for days where the closing price
# is within 5% of the highest closing price in the dataset.

query2 = """
SELECT AVG(Volume) AS AvgVolume
FROM goldhistoricaldata
WHERE CloseLast >= (SELECT MAX(CloseLast) * 0.95 FROM goldhistoricaldata);
"""
cursor.execute(query2)
result2 = cursor.fetchone()
print("\nAverage daily trading volume for days with close price within 5% of highest: {:.2f}".format(result2[0]))

# 3. Identify dates where the opening price was lower than the closing price by more than $50.

query3 = """
SELECT Date, Open, CloseLast, (CloseLast - Open) AS PriceDifference
FROM goldhistoricaldata
WHERE (Open - CloseLast) > 50;
"""
cursor.execute(query3)
result3 = cursor.fetchall()
print("\nDates where opening price was more than $50 lower than closing price:")
for row in result3:
    print("Date: {} Open: {:.2f} CloseLast: {:.2f} PriceDifference: {:.2f}".format(row[0], row[1], row[2], row[3]))

# 4. Find the date with the highest total trading volume in a single day.

query4 = """
SELECT Date, SUM(Volume) AS TotalVolume
FROM goldhistoricaldata
GROUP BY Date
ORDER BY TotalVolume DESC
LIMIT 1;
"""
cursor.execute(query4)
result4 = cursor.fetchone()
print("\nDate with highest total trading volume in a single day:", result4[0], "TotalVolume:", result4[1])

# 5. Calculate the percentage change in the average closing price between the first and last 10 days of available data.

query5 = """
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
"""
cursor.execute(query5)
result5 = cursor.fetchone()
print("\nPercentage change in average closing price between first and last 10 days: {:.2f}%".format(result5[0]))

# Close the cursor and connection
cursor.close()
conn.close()