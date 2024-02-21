from product import Product
from datetime import date, datetime
import json

"""
Functions to facilitate working with the JSON data for the products.
"""

data_file = "example_data.json"

def _date_to_json(date:date):
    """
    Takes in a date object and converts it to a string
    to be able to store in a JSON file
    """
    return date.__str__()

def _json_to_date(date:str):
    """
    Takes in a string of the format YYYY-MM-DD 
    (that was stored in a JSON file)
    and converts it to a datetime object
    """
    return datetime.strptime(date, "%Y-%m-%d").date()

def _product_to_dict(product:Product):
    """
    Takes in a Product object and returns its attributes as a dictionary
    """

    d = {product.name : {
        "dates" : [_date_to_json(i) for i in product.dates],
        "avg_duration" : product.avg_duration,
        "ending" : _date_to_json(product.ending),
        "price" : product.price,
        "price_per_month" : product.price_per_month,
        "c_volume" : product.c_volume
    }}

    return d

def _dict_to_product(d:dict, product_name:str):
    """
    Takes in a (properly formatted) dictionary and returns a Product object from the dictionary
    """
    product = Product(
        name=product_name, 
        dates=[_json_to_date(i) for i in d[product_name]["dates"]],
        price=d[product_name]["price"],
        c_volume = d[product_name]["c_volume"]
    )

    return product

def pull_products():

    with open(data_file, "r") as infile:
        d = json.load(infile)

    return d

def add_product(name:str, dates=[date.today()], price=0, c_volume=0):
    """
    Adds a new product to the JSON file 
    or replaces the product with the same name.
    """
    d = _product_to_dict(Product(name, dates, price, c_volume))

    with open(data_file, "r") as file:
        json_dict = json.load(file)
        json_dict.update(d)

    with open(data_file, "w") as outfile:
        json.dump(json_dict, outfile, indent=4)

def delete_product(name:str):
    """Removes a product from the JSON file."""

    with open(data_file, 'r') as infile:
        json_dict = json.load(infile)
        if name in json_dict:
            del json_dict[name]

    with open(data_file, "w") as outfile:
        json.dump(json_dict, outfile, indent=4)

def start_new_container(product_name, date=date.today()):
        d_org = pull_products() # Get a dictionary of all the JSON data

        product = _dict_to_product(d_org, product_name) # Convert the nested dict into a Product object
        product.add_date(date)
        d = _product_to_dict(product) # Convert the Product object back to a dict

        with open(data_file, "r") as infile:
            json_dict = json.load(infile)
            json_dict.update(d)

        with open(data_file, "w") as outfile:
            json.dump(json_dict, outfile, indent=4)


if __name__ == "__main__":
    print(pull_products())
    #JsonData().delete_product("Toothpaste")
    #print(JsonData().pull_products())