import os
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import numpy as np

from dagster_dbt import dbt_cli_resource, dbt_test_op, dbt_assets, load_assets_from_dbt_project, DbtCliResource, get_asset_key_for_model
from dagster import Definitions, file_relative_path, job, MetadataValue, AssetExecutionContext, asset


DBT_PROJECT_PATH = file_relative_path(__file__, "../dbt")
DBT_PROFILES = file_relative_path(__file__, "../dbt/config")
DBT_MANIFEST_PATH = file_relative_path(__file__, "../dbt/target/manifest.json")

dbt_resource = dbt_cli_resource.configured(
        {
            "project_dir": DBT_PROJECT_PATH,
            "profiles_dir": DBT_PROFILES,
        }
    )

model_resources = {
    "dbt": dbt_resource
}


@dbt_assets(manifest=DBT_MANIFEST_PATH)
def dag_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

@asset(
    compute_kind="python",
    deps=get_asset_key_for_model([dag_dbt_assets], "fact_sales")
)
def mean_transactions_per_month(context: AssetExecutionContext):
    duckdb_database_path = file_relative_path(__file__, "../../../../shared/db/datamart.duckdb")
    connection = duckdb.connect(os.fspath(duckdb_database_path))

    #  get sales data into Pandas DataFrame
    sales = connection.sql("select bought_date_key, product_price, qty, total_amount, transaction_id from datamart.postcard_company_core.fact_sales").df()
    print(sales)
    sales['bought_date_key'] = pd.to_datetime(sales['bought_date_key'], format='%Y%m%d')
    sales['tran_month'] = sales['bought_date_key'].dt.strftime('%Y%m')
    sales['actual_product_price'] = sales['product_price'] * sales['qty']

    # aggregate sales
    grouped_sales = sales.groupby(['tran_month'])
    # total transaction amount, 
    total_sales_per_month = grouped_sales['total_amount'].sum()
    # product price and 
    product_price_per_month = grouped_sales['actual_product_price'].sum()
    # number of transactions
    tran_count_per_month = grouped_sales['transaction_id'].count()

    #  calc which months were profitable
    sales_profit = sales[sales['total_amount'] > sales['actual_product_price']]
    months_with_profit = sales_profit.groupby(['tran_month'])['transaction_id'].count()

    # merge aggregated data
    sales_prod_compare = pd.merge(total_sales_per_month, product_price_per_month, on='tran_month').merge(tran_count_per_month,on='tran_month')    

    # compare aggregrated data to profitable sales
    compare = pd.merge(sales_prod_compare, months_with_profit, on='tran_month', how='outer').rename(columns={"transaction_id_x": "total_transactions", "transaction_id_y": "profitable_transactions"})

    #  calc mean
    compare['mean'] = np.where(compare['total_amount'] > compare['actual_product_price'], (compare['profitable_transactions']/compare['total_transactions'])*100, 0)
    compare_reset_index = compare.reset_index()
    mean = compare_reset_index[compare_reset_index['mean'] > 0][['tran_month', 'mean']]

    # create a plot of number of orders by customer and write it out to an HTML file
    fig = px.histogram(mean, x="tran_month")
    fig.update_layout(bargap=0.2)
    save_chart_path = duckdb_database_path.parent.joinpath("tran_month_mean_chart.html")
    fig.write_html(save_chart_path, auto_open=True)

    # tell Dagster about the location of the HTML file,
    # so it's easy to access from the Dagster UI
    context.add_output_metadata(
        {"plot_url": MetadataValue.url("file://" + os.fspath(save_chart_path))}
    )


@job(resource_defs={'dbt': dbt_resource})
def run_dbt_test_job():
    dbt_test_op()


defs = Definitions(
    assets=[dag_dbt_assets, mean_transactions_per_month],
    resources=model_resources, 
    jobs=[run_dbt_test_job]
)
