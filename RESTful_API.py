"""Here we start with the construction of our FASTapi server. This server
will be designed to add items to, delete items from, and retrieve a
given list of items. """

from fastapi import FastAPI
from pydantic import (
    BaseModel,
)

""" Turns FastAPI into a function that we can pull commands from."""
app = (
    FastAPI()
)


""" Make an item class for the API to work with."""


class Item(BaseModel):
    name: str
    item_characteristics: str


""" Make a list of items to work with."""


my_list = [
    ["name", "components"]
]


"""Now we have a list to work with, let's make our necessary endpoints
that work with it."""


""" Adds a new item to the list.


This function allows the user to specify details of an item
they would want added to the list, adds those items to the
list, and then returns the list's most recent addition. """


@app.post("/new-item")
def new_item(item: Item):
    my_list.append(item)
    return my_list[-1]


""" Returns the list and the items in it."""


@app.get("/get-list")
def get_list():
    return my_list


""" Deletes a given item from a list.


This function deletes an item with the specified index from
the list. If the item index is not in the list, the user is
told so. If it does, the corresponding item is deleted from
the list and the user is told so. """


@app.delete("/delete/{index}")
def delete_item(item_num):
    if item_num not in my_list:
        return {"Error": "Item does not exist."}

    del my_list[item_num]
    return {"Success": "Item deleted."}
