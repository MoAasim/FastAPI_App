from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['productdb']
collection = db['products']


# Product Schema
class Product(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


# Create Product
@app.post('/products/')
async def create_product(product: Product):
    product = dict(product)
    result = collection.insert_one(product)
    product['_id'] = str(result.inserted_id)
    return product


# Read All Products
@app.get('/products/')
async def get_products():
    products = []
    for product in collection.find():
        product['_id'] = str(product['_id'])
        products.append(product)
    return products


# Read Single Product
@app.get('/products/{product_id}')
async def get_product(product_id: str):
    try:
      product = collection.find_one({'_id': ObjectId(product_id)})
      if product:
          product['_id'] = str(product['_id'])
          return product
      else:
          return {'error': 'Product not found'}
    except:
        return {'error': 'Invalid request'}


# Update Product
@app.put('/products/{product_id}')
async def update_product(product_id: str, product: Product):
    product = dict(product)
    result = collection.update_one({'_id': ObjectId(product_id)}, {'$set': product})
    if result.modified_count == 1:
        product['_id'] = product_id
        return product
    else:
        return {'error': 'Product not found'}


# Delete Product
@app.delete('/products/{product_id}')
async def delete_product(product_id: str):
    result = collection.delete_one({'_id': ObjectId(product_id)})
    if result.deleted_count == 1:
        return {'message': 'Product deleted'}
    else:
        return {'error': 'Product not found'}
