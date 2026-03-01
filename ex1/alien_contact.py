from pydantic import BaseModel, model_validator, Field, ValidationError
from datetime import datetime
from typing import Optional
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
    signal_strength: float =Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge= 1, le=1440)
    witness_count: int = Field(ge=1 , le=100)
    message_received: Optional[str] = Field(max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def check_validate(self):
        if  not self.contact_id.startswith("AC"):
            raise ValueError(f'Contact ID must start with "AC"')
        if  self.contact_type == ContactType.physical and self.is_verified == False:
            raise ValueError(f" Physical contact reports must be verified")
        if self.contact_type == ContactType.telepathic and self.witness_count < 3:
            raise ValueError(f"Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(f" Strong signals (> 7.0) should include received messages")
        
try :
    valid_contact = AlienContact(contact_id="AC_2024_001",
                                 timestamp= datetime.now(),
                                 location=" Area 51, Nevada",
                                 contact_type="raido",
                                 signal_strength= 8.5,
                                 duration_minutes= 45,
                                 witness_count= 2,
                                 message_received= "Greetings from Zeta Reticuli",
                                 is_verified= True)


    Print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    print(f"ID: {valid_contact.contact_id}")
    print(f"Type: {valid_contact.contact_type}")
    print(f"Location: {valid_contact.location}")
    print(f"Signal: {valid_contact.signal_strength}/10")
    print(f"Duration: {valid_contact.duration_minutes} minutes")
    print(f"Witnesses: {valid_contact.witness_count}")
    print(f"Message: {valid_contact.message_received}")

except ValidationError as e:
    print (e)

try :
    error_contact = AlienContact(contact_id="AC_2024_001",
                                 timestamp= datetime.now(),
                                 location=" Area 51, Nevada",
                                 contact_type="raido",
                                 signal_strength= 8.5,
                                 duration_minutes= 45,
                                 witness_count= 5,
                                 message_received= "Greetings from Zeta Reticuli",
                                 is_verified= True)


    Print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    print(f"ID: {error_contact.contact_id}")
    print(f"Type: {error_contact.contact_type}")
    print(f"Location: {error_contact.location}")
    print(f"Signal: {error_contact.signal_strength}/10")
    print(f"Duration: {error_contact.duration_minutes} minutes")
    print(f"Witnesses: {error_contact.witness_count}")
    print(f"Message: {error_contact.message_received}")

except ValidationError as e:
    print (e)
