-- ОСНОВНОЙ SQL 
SELECT
  "month",
  "category",
  "amount",
  "cashback",

  CASE
    WHEN "amount" < 0 THEN TRUE ELSE FALSE
  END AS is_expense,

  CASE
    WHEN "amount" < 0 THEN ABS("amount") ELSE 0
  END AS abs_amount

FROM "20260413_20260425125530";

-- АНАЛИЗ КЭШБЕКА ПО КАТЕГОРИЯМ
SELECT
  "category",
  SUM(CAST(REPLACE("cashback", '+', '') AS DOUBLE)) AS total_cashback
FROM "20260413_20260425125530"
GROUP BY "category"
ORDER BY total_cashback DESC;


-- ДОХОД / РАСХОД
SELECT
  "month",
  SUM(CASE WHEN "amount" > 0 THEN "amount" ELSE 0 END) AS income,
  SUM(CASE WHEN "amount" < 0 THEN "amount" ELSE 0 END) AS expenses,
  SUM("amount") AS net
FROM "20260413_20260425125530"
GROUP BY "month"
ORDER BY "month";


-- СРЕДНЕМЕСЯЧНЫЕ РАСХОДЫ 
SELECT
  AVG(month_expenses) AS avg_monthly_expenses
FROM (
  SELECT
    "month",
    SUM(CASE WHEN "amount" < 0 THEN "amount" ELSE 0 END) AS month_expenses
  FROM "20260413_20260425125530"
  GROUP BY "month"
) t;


-- ТРАТЫ ПО КАТЕГОРИЯМ 
SELECT
  "category",
  SUM(abs_amount) AS total_expenses
FROM "20260413_20260425125530"
WHERE amount < 0
GROUP BY "category"
ORDER BY total_expenses DESC;


-- КАТЕГОРИЯ -> МЕСЯЦ
SELECT
  "category" AS source,
  "month" AS target,
  SUM(CASE WHEN "amount" < 0 THEN ABS("amount") ELSE 0 END) AS value
FROM "20260413_20260425125530"
GROUP BY "category", "month"
ORDER BY value DESC;


-- ДВИЖЕНИЕ СРЕДСТВ ПО МЕСЯЦАМ
WITH monthly AS (
  SELECT
    "month",
    SUM("amount") AS net
  FROM "20260413_20260425125530"
  GROUP BY "month"
)

SELECT
  "month",
  net,
  SUM(net) OVER (ORDER BY "month") AS cumulative_cashflow
FROM monthly
ORDER BY "month";


-- ДВИЖЕНИЕ СРЕДСТВ ПО КВАРТАЛАМ
WITH prepared AS (
  SELECT
    "month",
    SUBSTRING("month", 1, 4) AS yr,
    CASE
      WHEN CAST(SUBSTRING("month", 6, 2) AS INT) BETWEEN 1 AND 3 THEN 1
      WHEN CAST(SUBSTRING("month", 6, 2) AS INT) BETWEEN 4 AND 6 THEN 2
      WHEN CAST(SUBSTRING("month", 6, 2) AS INT) BETWEEN 7 AND 9 THEN 3
      WHEN CAST(SUBSTRING("month", 6, 2) AS INT) BETWEEN 10 AND 12 THEN 4
    END AS q,
    "amount"
  FROM "20260413_20260425125530"
)

SELECT
  yr || '-Q' || q AS period,
  SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) AS expenses,
  SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS income,
  SUM(amount) AS net
FROM prepared
GROUP BY yr, q
ORDER BY period;