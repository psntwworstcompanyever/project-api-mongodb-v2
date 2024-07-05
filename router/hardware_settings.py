from fastapi import APIRouter, Depends, HTTPException
from db import (
    get_hw_settings,
)

router = APIRouter()


@router.get(
    "/pcba/{pcba_sn}",
    response_description="Get PCBA settings by PCBA SN",
    response_model_by_alias=False,
)
async def get_pcba_settings_by_sn(pcba_sn: str, collection=Depends(get_hw_settings)):
    """
    Get the settings for a specific PCBA, looked up by `pcba_sn`.
    """
    query_result = await collection.find_one({"pcba_sn": pcba_sn})
    if not query_result:
        raise HTTPException(status_code=404, detail="PCBA settings are not found")
    pcba_settings = [
        {"$el": "h2", "children": ["Hardware Settings"]},
        {
            "$el": "div",
            "attrs": {
                "style": "border: 1px solid #ccc; padding: 20px; margin-bottom: 20px;"
            },
            "children": query_result["settings"],
        },
    ]
    return pcba_settings
