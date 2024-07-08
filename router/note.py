from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict
from db import (
    get_spec_note,
    get_customer_settings,
)

router = APIRouter()


@router.get(
    "/get",
    response_model=List[Dict],  # Use a more generic response model
    response_description="Retrieve the spec and customer note.",
)
async def get_note(
    spec: str = Query(..., description="The specification parameter"),
    customer: str = Query(..., description="The customer parameter"),
    collection_spec_note=Depends(get_spec_note),
    collection_customer_note=Depends(get_customer_settings),
):
    query_spec_note = await collection_spec_note.find_one({"name": spec})
    if query_spec_note is None:
        query_spec_note = {"note": "API find no record."}
    query_customer_note = await collection_customer_note.find_one(
        {"specification": spec, "customer": customer}
    )
    if query_customer_note is None:
        query_customer_note = {"note": "API find no record."}

    return [
        {
            "illustration": query_spec_note["note"],
        },
        {
            "recommendation": query_customer_note["note"],
        },
    ]
