
  
    

    create  table
      "datamart"."postcard_company_staging"."staging_transactions__dbt_tmp"
    as (
      


SELECT * FROM "datamart"."postcard_company_staging"."staging_transactions_main"

UNION ALL

SELECT * FROM "datamart"."postcard_company_staging"."staging_transactions_resellers_csv"

UNION ALL

SELECT * FROM "datamart"."postcard_company_staging"."staging_transactions_resellers_json"
    );
  