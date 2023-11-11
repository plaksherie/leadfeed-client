from pydantic import BaseModel


class LeadFeed(BaseModel):
    login: str
    password: str
    sesid: str


class Selenium(BaseModel):
    delay_sign_in: int


class Config(BaseModel):
    leadfeed: LeadFeed
    selenium: Selenium
