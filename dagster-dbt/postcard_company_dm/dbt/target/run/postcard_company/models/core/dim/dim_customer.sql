
  
    

    create  table
      "datamart"."postcard_company_core"."dim_customer__dbt_tmp"
    as (
      

select customer_key, customer_first_name, customer_last_name, customer_email, sales_agent_key
from "datamart"."postcard_company_staging"."staging_customers"
    );
  