#!/usr/bin/env python
# coding: utf-8

# In[6]:


pip install fastapi


# In[21]:


'''Here we start with the construction of our FASTapi server. This server
   will be designed to add items to, delete items from, and retrieve a 
   given list of items. '''

# Start with importing the necessary libraries/files

from fastapi import FastAPI     # Import FastAPI, the basis for this API.
from pydantic import BaseModel  # Import BaseModel, so that we can make a JSON-friendly item class.

app = FastAPI()    # Turns FastAPI into a function that we can pull commands from, like .post and .get. 

class Item(BaseModel):            # Here we make the item class (inherited from BaseModel) 
    name: str                     # that this API will work with, given generic features
    item_characteristics: str     # such as an item's name and characteristics.

list = {1: {"name": "feature1", "parts" : "cool stuff"}}      # A short list containing one item.


'''Now we have a list to work with, let's make our necessary endpoints that work with it.'''
    
# New-item endpoint. This will allow the user to add a new item to the list.
@app.post('/new-item/{item_id}')
def new_item(item_id:int, item: Item):
    if item[item_id] in list:                      # Checks if an item with the desired ID already exists.
        return ("That item already exists.")       # If it does, the user is told so.
    
    list[item_id] = item                           # If the desired ID is not already in the list, a new 
    return list[item_id]                           # item is made. 

# List-return endpoint. Returns the list and the items in it. 
@app.get('/get-list/{list_name}')
def get_list(list): 
    return list 

# Delete-item endpoint. Deletes a given item from a list. 
@app.delete('/delete/{index}')
def delete_item(item_id:int = Query(..., description = "ID of item to be deleted.")):      
    if item_id not in list:                                 # Checks if the provided item ID is in the list.
        return {"Error": "Item does not exist."}            # If not, the user is told so.
    
    del list[item_id]                                       # If the item ID is in the list, the item is deleted. 
    return {"Success": "Item deleted."}


# In[ ]:





# In[ ]:




