from setuptools import find_packages, setup

setup(
    name="postcard_company_dm",
    packages=find_packages(),
    install_requires=[
        "dagster==1.6.0",        
        "dagster-dbt==0.22.0",        
        "duckdb==0.8.1",
        "dbt-core==1.7.0",        
        "dbt-duckdb==1.7.0",        
        "dagster-duckdb==0.22.0",        
        "declxml",
        "pyarrow",
        "names",
        "numpy",
        "pandas<2.1.0",
        "psycopg2-binary",
        "pendulum<3.0"                                      #  https://github.com/dagster-io/dagster/discussions/18783#discussioncomment-7881162
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
