import os
from datetime import date, datetime

from pydantic import AliasChoices, Field, field_validator

from slopfactory.schema import BaseModel


class Contact(BaseModel):
    email: str | None = None
    phone: str | None = Field(validation_alias=AliasChoices("phone", "mobile"))
    website: str | None = Field(validation_alias=AliasChoices("website", "portfolio"))


class Period(BaseModel):
    start: str | date
    end: str | date | None = None

    @field_validator("start", "end")
    def str_to_datetime(cls, v) -> str | date | None:
        if not v:
            return v

        if v == "Present":
            return None

        try:
            return datetime.strptime(v, os.getenv("DATETIME_FORMAT", "%m/%Y")).date()
        except:
            return v


class HasNoun(BaseModel):
    name: str
    description: str | None = None


class HasContact(BaseModel):
    contact: Contact | None = None
    location: str | None = None


class Company(HasNoun, HasContact):
    pass


class Role(BaseModel):
    role: str = Field(validation_alias=AliasChoices("role", "title"))
    period: Period
    responsibilities: list[str]
    location: str | None = None


class History(BaseModel):
    company: Company
    roles: list[Role]


class Personal(HasNoun, HasContact):
    pronouns: str | None = None
    title: str | None = None


class Resume(BaseModel):
    personal: Personal
    history: list[History] = Field(default_factory=list)
