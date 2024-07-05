from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from db import (
    get_customer_settings,
)

router = APIRouter()


@router.get(
    "/customer/{customer}",
    response_model=Dict,  # Adjusted response model to a more generic Dict
    response_description="Get customer settings by customer",
)
async def get_customer_settings_by_customer(
    customer: str, collection=Depends(get_customer_settings)
):
    """
    Get the settings for a specific customer, looked up by `customer`.
    """
    cursor = collection.aggregate(
        [
            {"$match": {"customer": customer}},
            {
                "$project": {
                    "_id": 0,
                    "keyValue": {
                        "$arrayToObject": [[{"k": "$specification", "v": "$setting"}]]
                    },
                }
            },
            {"$group": {"_id": None, "allSettings": {"$mergeObjects": "$keyValue"}}},
            {"$project": {"_id": 0, "customer_settings": "$allSettings"}},
        ]
    )
    query_result = await cursor.to_list(None)
    if not query_result:
        raise HTTPException(status_code=404, detail="Customer settings are not found")
    # Extracting the 'customer_settings' directly from the first item in the list
    customer_settings = query_result[0].get("customer_settings", {})
    return customer_settings
