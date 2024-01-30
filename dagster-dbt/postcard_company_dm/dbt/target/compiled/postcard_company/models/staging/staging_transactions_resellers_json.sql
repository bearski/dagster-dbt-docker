

WITH 

  

trans_json AS (
  SELECT
    
    
md5(cast(coalesce(cast('reseller-id' as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(transactionId as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS customer_key,
    "reseller-id" AS reseller_id,
    transactionId AS transaction_id,
    productName AS product_name,
    totalAmount AS total_amount,
    qty AS no_purchased_postcards,
    "date" AS bought_date,
    salesChannel AS sales_channel,
    seriesCity AS office_location,
    loaded_timestamp
  FROM
    "datamart"."postcard_company_raw"."raw_resellers_json"


  



)


SELECT
  t.customer_key,
  transaction_id,
  e.product_key,
  C.channel_key,
  t.reseller_id,
  bought_date AS bought_date_key,
  total_amount::numeric,
  no_purchased_postcards,
  e.product_price::numeric,
  e.geography_key,
  s.commission_pct * total_amount::numeric AS commisionpaid,
  s.commission_pct,
  loaded_timestamp
FROM
  trans_json t
  JOIN "datamart"."postcard_company_core"."dim_product"
  e
  ON t.product_name = e.product_name
  JOIN "datamart"."postcard_company_core"."dim_channel" C
  ON t.sales_channel = C.channel_name
  JOIN "datamart"."postcard_company_core"."dim_customer"
  cu
  ON t.customer_key = cu.customer_key
  JOIN "datamart"."postcard_company_core"."dim_salesagent"
  s
  ON t.reseller_id = s.original_reseller_id