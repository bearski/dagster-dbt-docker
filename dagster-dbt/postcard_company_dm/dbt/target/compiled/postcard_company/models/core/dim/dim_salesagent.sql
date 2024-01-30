


SELECT
    reseller_id AS sales_agent_key,
    reseller_id AS original_reseller_id,
    reseller_name,
    commission_pct
FROM
    "datamart"."postcard_company_staging"."staging_resellers"
UNION ALL
SELECT
    0 AS sales_agent_key,
    NULL AS original_reseller_id,
    'Direct Sales' AS reseller_name,
    NULL AS commission_pct