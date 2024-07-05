from typing import Optional, List, Dict, Union
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class PCBAModel(BaseModel):
    """
    Container for a hardware settings record.
    """

    # The primary key for the PCBAModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    pcba_sn: str = Field(...)
    settings: List[Dict[str, Union[str, List[Dict[str, str]]]]]

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "pcba_sn": "PCBA123456",
                "settings": [
                    {
                        "$formkit": "select",
                        "name": "phase",
                        "label": "Phase",
                        "options": [
                            {"value": "three-phase", "label": "三相(Three-phase)"}
                        ],
                    },
                    {
                        "$formkit": "select",
                        "name": "mcu",
                        "label": "MCU",
                        "options": [
                            {
                                "value": "FU6832N",
                                "label": "FU6832N",
                            }
                        ],
                    },
                    {
                        "$formkit": "select",
                        "name": "frame_size",
                        "label": "Frame Size",
                        "options": [
                            {
                                "value": "4CM",
                                "label": "4CM",
                            }
                        ],
                    },
                    {
                        "$formkit": "select",
                        "name": "MOSFET",
                        "label": "MOSFET",
                        "options": [
                            {
                                "value": "QH8MA2",
                                "label": "ROHM/QH8MA2/30V/Nch=4.5A/Pch=3.5A",
                            },
                            {
                                "value": "QH8MA4",
                                "label": "ROHM/QH8MA4/30V/Nch=9.0A/Pch=8.0A",
                            },
                        ],
                    },
                ],
            }
        },
    )
