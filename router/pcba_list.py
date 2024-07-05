from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from db import (
    get_pcba_list,
)

router = APIRouter()


@router.get(
    "/get",
    response_model=List[Dict],  # Use a more generic response model
    response_description="Retrieve the PCBA list",
)
async def get_pcba_list(collection=Depends(get_pcba_list)):
    # Directly exclude the '_id' field in the query
    pcba_list = await collection.find({}, {"_id": 0}).sort("index", 1).to_list(None)
    if not pcba_list:
        raise HTTPException(status_code=404, detail="List not found")
    return pcba_list
