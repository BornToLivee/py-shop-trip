import datetime
import json
from app.customer import Customer
from app.shop import Shop


def shop_trip() -> None:
    for customer in customers:
        all_shops_cost = {}
        print(f"{customer.name} has {customer.money} dollars")
        for shop in shops:
            lap = ((customer.location[0] - shop.location[0]) ** 2
                   + (customer.location[1] - shop.location[1]) ** 2) ** 0.5
            costs = (customer.product_cart["milk"] * shop.products["milk"]
                     + customer.product_cart["bread"] * shop.products["bread"]
                     + customer.product_cart["butter"]
                     * shop.products["butter"])
            destination_cost = ((lap * customer.car["fuel_consumption"] / 100)
                                * 2 * all_data["FUEL_PRICE"])
            total_cost = round(destination_cost + costs, 2)
            print(f"{customer.name}'s trip to the {shop.name}"
                  f" costs {total_cost}")
            all_shops_cost[shop] = total_cost

        cheapest_shop = min(all_shops_cost, key=all_shops_cost.get)
        if all_shops_cost[cheapest_shop] > customer.money:
            print(f"{customer.name} doesn't have enough money"
                  f" to make a purchase in any shop")
            continue

        milk_price = (customer.product_cart["milk"]
                      * cheapest_shop.products["milk"])
        bread_price = (customer.product_cart["bread"]
                       * cheapest_shop.products["bread"])
        butter_price = (customer.product_cart["butter"]
                        * cheapest_shop.products["butter"])
        products_cost = milk_price + bread_price + butter_price
        money_left = customer.money - all_shops_cost[cheapest_shop]

        print(f"{customer.name} rides to {cheapest_shop.name}\n\n"
              f"Date: "
              f"{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n"
              f"Thanks, {customer.name}, for your purchase!\n"
              "You have bought:\n"
              f"{customer.product_cart["milk"]} milks for "
              f"{milk_price} dollars\n"
              f"{customer.product_cart["bread"]} breads for "
              f"{int(bread_price)} dollars\n"
              f"{customer.product_cart["butter"]} butters for "
              f"{butter_price} dollars\n"
              f"Total cost is {products_cost} dollars\n"
              "See you again!\n\n"
              f"{customer.name} rides home\n"
              f"{customer.name} now has {money_left} dollars\n")


with open("app/config.json") as data_file:
    all_data = json.load(data_file)

customers = []
for customer_data in all_data["customers"]:
    name = customer_data["name"]
    product_cart = customer_data["product_cart"]
    location = customer_data["location"]
    money = customer_data["money"]
    car = customer_data["car"]
    customer = Customer(name, product_cart, location, money, car)
    customers.append(customer)
shops = []
for shop_data in all_data["shops"]:
    name = shop_data["name"]
    location = shop_data["location"]
    products = shop_data["products"]
    shop = Shop(name, location, products)
    shops.append(shop)

if __name__ == "__main__":
    shop_trip()
