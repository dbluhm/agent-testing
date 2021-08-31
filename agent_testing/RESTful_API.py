"""Here we start with the construction of our FASTapi server. This server
will be designed to add items to, delete items from, and retrieve a
given list of items. """

from fastapi import FastAPI
from pydantic import (
    BaseModel,
)

# Turns FastAPI into a function that we can pull commands from.
app = (
    FastAPI()
)


# Make an item class for the API to work with.


class Item(BaseModel):
    name: str
    item_characteristics: str


# Make a list of items to work with.


my_list = [
    {"name": "item1", "components": "feature1"}
]


# Now we have a list to work with, let's make
# our necessary endpoints that work with it.


@app.post("/new-item")
def new_item(item: Item):

    """ Adds a new item to the list.


    This function allows the user to specify details of an item
    they would want added to the list, adds those items to the
    list, and then returns the list's most recent addition. 
    """
    my_list.append(item)
    return my_list[-1]


@app.get("/get-list")
def get_list():

    """ Returns the list and the items in it.
    """
    return my_list


@app.delete("/delete/")
def delete_item(item_num: int):

    """ Deletes a given item from a list.


    This function deletes an item with the specified index from
    the list. If the item index is not in the list, the user is
    told so. If it does, the corresponding item is deleted from
    the list and the user is told so. 
    """
    if int(item_num) > len(my_list):
        return {"Error": "Item does not exist."}

    del my_list[int(item_num)-1]
    return {"Success": "Item deleted."}
