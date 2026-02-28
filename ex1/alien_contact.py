from pydantic import BaseModel, model_validator
from datetime import datetime
from enum import Enum

class ContactType(str, Enum):
    radio= "radio"
    visual= "visual"
    physical= "physical"
    telepathic= "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5 , max_length=15)
    timestamp: datetime 
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float =Field(ge=0, le=10)
    duration_minutes: int = Field(ge= 1, le= 1440)
    witness_count: int
    message_received: str
    is_verified: bool = False

    @model_validator(mode='after')
    def check_validate(cls):
        if  not model.contact_id.startwith("AC"):
            
