import datetime
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData, Column, String, Integer, Text, insert
from loguru import logger

# Get current date
current_date = datetime.datetime.now().strftime('%d_%m_%Y')

# Database connections
bb_engine = create_engine('mysql+pymysql://root:actowiz@localhost:3306/big_basket_screenshot', echo=True)
amazon_engine = create_engine('mysql+pymysql://root:actowiz@localhost:3306/amazon_fresh_screenshot', echo=True)

# File paths
bb_filepath = fr"D:\Nirav Chauhan\code\big_basket_screenshot\Output\{current_date}\{current_date}.csv"
amazon_filepath = fr"D:\Nirav Chauhan\code\gorkhnath_sir_amazon_ss\amazon_screnshot\Output\{current_date}\{current_date}.csv"

# Read CSV files
big_basket_df = pd.read_csv(bb_filepath)
amazon_df = pd.read_csv(amazon_filepath)


def _big_basket():
    # Select & rename columns
    big_basket_columns = ['Name Of the Brand', 'Category', 'Name of the Product', 'Quantity of the Product',
                          'Single Pack', 'Bundle Pack', 'Quantity', 'Packaging of the product', 'Bigbasket',
                          'BigBasket --  Approved/ Not Approved', 'City', 'Pincode']
    new_df = big_basket_df.loc[:, big_basket_columns]
    new_df.columns = [
        'Name_Of_the_Brand', 'Category', 'Name_of_the_Product', 'Quantity_of_the_Product',
        'Single_Pack', 'Bundle_Pack', 'Quantity', 'Packaging_of_the_product', 'big_basket',
        'big_basket_approve_not_approve', 'City_Name', 'zipcode'
    ]

    # Add extra columns
    new_df['Status'] = "Pending"
    new_df['quantity_caping'] = None

    # Replace NaNs with None
    new_df = new_df.astype(object).where(pd.notnull(new_df), None)

    logger.info(f"Preparing to insert {len(new_df)} rows into BigBasket table")
    logger.debug(new_df.head())

    meta = MetaData()

    try:
        results = Table(f'pdp_link_table_{current_date}', meta,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('Name_Of_the_Brand', String(100)),
                        Column('Category', String(100)),
                        Column('Name_of_the_Product', String(500)),
                        Column('Quantity_of_the_Product', String(100)),
                        Column('Single_Pack', String(50)),
                        Column('Bundle_Pack', String(50)),
                        Column('Quantity', String(50)),
                        Column('Packaging_of_the_product', String(255)),
                        Column('big_basket', String(255)),
                        Column('big_basket_approve_not_approve', String(30)),
                        Column('City_Name', String(30)),
                        Column('zipcode', String(10)),
                        Column('Status', String(30)),
                        Column('quantity_caping', String(10)),
                        )
        logger.success("BigBasket table structure created.")
    except Exception as e:
        logger.error(f"Table Creation Failed: {e}")
        return

    try:
        meta.create_all(bb_engine)
        with bb_engine.begin() as conn:
            conn.execute(insert(results), new_df.to_dict(orient='records'))
        logger.success("BigBasket data inserted successfully.")
    except Exception as e:
        logger.error(f"Insert Failed: {e}")


def _amazon_fresh():
    amazon_fresh_columns = ['Name Of the Brand', 'Category', 'Name of the Product', 'Quantity of the Product',
                            'Single Pack', 'Bundle Pack', 'Quantity', 'Packaging of the product', 'Amazon Fresh',
                            'Amazon Fresh --  Approved/ Not Approved', 'City', 'Pincode']
    new_df = amazon_df.loc[:, amazon_fresh_columns]
    new_df.columns = [
        'Name Of the Brand', 'Category', 'Name of the Product', 'Quantity of the Product',
        'Single Pack', 'Bundle Pack', 'Quantity', 'Packaging of the product', 'Amazon Fresh',
        'amazon_approve_not_approve', 'City Name', 'zipcode'
    ]

    new_df['status'] = "Pending"
    new_df = new_df.astype(object).where(pd.notnull(new_df), None)

    logger.info(f"Preparing to insert {len(new_df)} rows into Amazon Fresh table")
    logger.debug(new_df.head())

    meta = MetaData()

    try:
        results = Table(f'pdp_link_table_{current_date}', meta,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('Name Of the Brand', String(100)),
                        Column('Category', String(100)),
                        Column('Name of the Product', String(500)),
                        Column('Quantity of the Product', String(100)),
                        Column('Single Pack', String(50)),
                        Column('Bundle Pack', String(50)),
                        Column('Quantity', String(50)),
                        Column('Packaging of the product', String(255)),
                        Column('Amazon Fresh', Text),
                        Column('amazon_approve_not_approve', String(30)),
                        Column('City Name', String(30)),
                        Column('zipcode', String(10)),
                        Column('status', String(30)),
                        )
        logger.success("Amazon Fresh table structure created.")
    except Exception as e:
        logger.error(f"Table Creation Failed: {e}")
        return

    try:
        meta.create_all(amazon_engine)
        with amazon_engine.begin() as conn:
            conn.execute(insert(results), new_df.to_dict(orient='records'))
        logger.success("Amazon Fresh data inserted successfully.")
    except Exception as e:
        logger.error(f"Insert Failed: {e}")


if __name__ == '__main__':
    _big_basket()
    _amazon_fresh()  # Uncomment to run Amazon Fresh import
