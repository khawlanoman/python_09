from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from datetime import datetime
from typing import List


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def check_validate(self):
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        found = False
        for member in self.crew:
            if member.rank == Rank.commander or member.rank == Rank.captain:
                found = True
        if not found:
            raise ValueError("Mission must have at"
                             "least one Commander or Captain")

        if self.duration_days > 365:
            experience_count = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experience_count += 1

            total = experience_count / len(self.crew)
            if total < 0.5:
                raise ValueError("Long missions (> 365 days)"
                                 "need 50% experienced crew (5+ years)")

        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")
        return self


print("Space Mission Crew Validation")
print("=========================================")
try:

    crew_list = [CrewMember(member_id="CM001",
                            name="Sarah Connor",
                            rank="commander",
                            age=40,
                            specialization="Mission Command",
                            years_experience=15,
                            is_active=True),
                 CrewMember(member_id="CM002",
                            name="John Smith",
                            rank="lieutenant",
                            age=35,
                            specialization="Navigation",
                            years_experience=8,
                            is_active=True),
                 CrewMember(member_id="CM003",
                            name="Alice Johnson",
                            rank="officer",
                            age=30,
                            specialization="Engineering",
                            years_experience=5,
                            is_active=True)]

    station = SpaceMission(mission_id="M2024_MARS",
                           mission_name="Mars Colony Establishment",
                           destination=" Mars",
                           launch_date=datetime.now(),
                           duration_days=900,
                           crew=crew_list,
                           mission_status="planned",
                           budget_millions=2500.0)

    print("Valid mission created:")
    print(f"Mission: {station.mission_name}")
    print(f"ID: {station.mission_id}")
    print(f"Destination: {station.destination}")
    print(f"Duration: {station.duration_days} days")
    print(f"Budget: ${station.budget_millions}M")
    print(f"Crew size: {len(crew_list)}")
    print("Crew members:")
    for member in station.crew:
        print(f"- {member.name} ({member.rank.value})"
              f" - {member.specialization}")


except ValidationError as e:
    msg = str(e.errors()[0]['msg']).split("Value error, ")[-1]
    print(msg.split("\n")[0])


print("\n=========================================")
try:

    crew_list = [CrewMember(member_id="CM002",
                            name="John Smith",
                            rank="lieutenant",
                            age=35,
                            specialization="Navigation",
                            years_experience=8,
                            is_active=True),
                 CrewMember(member_id="CM003",
                            name="Alice Johnson",
                            rank="officer",
                            age=30,
                            specialization="Engineering",
                            years_experience=5,
                            is_active=True)]

    station = SpaceMission(mission_id="M2024_MARS",
                           mission_name="Mars Colony Establishment",
                           destination=" Mars",
                           launch_date=datetime.now(),
                           duration_days=900,
                           crew=crew_list,
                           mission_status="planned",
                           budget_millions=2500.0)

    print(f"\nMission: {station.mission_name}")
    print(f"ID: {station.mission_id}")
    print(f"Destination: {station.destination}")
    print(f"Duration: {station.duration_days} days")
    print(f"Budget: ${station.budget_millions}M")
    print(f"Crew size: {len(crew_list)}")
    print("Crew members:")
    for member in station.crew:
        print(f"- {member.name} ({member.rank.value})"
              f" - {member.specialization}")


except ValidationError as e:
    print("Expected validation error:")
    msg = str(e.errors()[0]['msg']).split("Value error, ")[-1]
    print(msg.split("\n")[0])
