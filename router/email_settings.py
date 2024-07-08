from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from db import (
    get_email_settings,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[Dict],  # Use a more generic response model
    response_description="Get the software settings",
)
async def get_email_settings(collection=Depends(get_email_settings)):
    """
    Get the settings for the specification.
    """
    specs = await collection.find({}, {"_id": 0}).sort("index", 1).to_list(None)
    if not specs:
        raise HTTPException(status_code=404, detail="Email settings are not found")
    return specs
