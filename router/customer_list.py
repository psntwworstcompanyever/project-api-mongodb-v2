from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from db import (
    get_customer_list,
)

router = APIRouter()


@router.get(
    "/get",
    response_model=List[Dict],  # Use a more generic response model
    response_description="Retrieve the customer list",
)
async def get_customer_list(collection=Depends(get_customer_list)):
    # Directly exclude the '_id' field in the query
    customer_list = await collection.find({}, {"_id": 0}).sort("index", 1).to_list(None)
    if not customer_list:
        raise HTTPException(status_code=404, detail="List not found")
    return customer_list
