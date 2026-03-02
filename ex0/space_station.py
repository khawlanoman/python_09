from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime = Field(default=None)
    is_operational: bool = Field(default=True)
    notes:  Optional[str] = Field(max_length=200)


def main():

    space_stations1 = SpaceStation(station_id="ISS001",
                                   name="International Space Station",
                                   crew_size=6,
                                   power_level=85.5,
                                   oxygen_level=92.3,
                                   last_maintenance="2026-02-28T10:30:00",
                                   is_operational=True,
                                   notes="Operational")

    print("\nSpace Station Data Validation")
    print("========================================")
    print("Valid station created:")
    print(f"ID:{space_stations1.station_id}")
    print(f"Name: {space_stations1.name}")
    print(f"Crew: {space_stations1.crew_size} people")
    print(f"Power: {space_stations1.power_level:.1f}%")
    print(f"Oxygen: {space_stations1.oxygen_level:.1f}%")
    print(f"Status: {space_stations1.notes}")

    try:
        space_stations2 = SpaceStation(station_id="ISS001",
                                       name="International Space Station",
                                       crew_size=40,
                                       power_level=85.5,
                                       oxygen_level=92.3,
                                       last_maintenance="2026-02-28T10:30:00",
                                       is_operational=True,
                                       notes="Operational")

        print(f"ID:{space_stations2.station_id}")
        print(f"Name: {space_stations2.name}")
        print(f"Crew: {space_stations2.crew_size} people")
        print(f"Power: {space_stations2.power_level:.1f}%")
        print(f"Oxygen: {space_stations2.oxygen_level:.1f}%")
        print(f"Status: {space_stations2.notes}")

    except ValidationError as e:
        print("\n========================================")
        print("Expected validation error:")
        for err in e.errors():
            message = err["msg"]
            print(message)


main()
