#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlmodel import SQLModel, create_engine, Session, select, Field
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

CONNECTION_URI = "sqlite:///database.db"

# connect
engine = create_engine(CONNECTION_URI, echo=True)


# model 정의
class Hero(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


# model create or reflect
SQLModel.metadata.create_all(engine)

# insert/update
hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", age=33)
with Session(engine) as session:
    session.add(hero_1)  # execution wait: insert stmt
    session.commit()

    hero_1.age = 34
    session.add(hero_1)  # execution wait: update stmt
    session.commit()

    session.refresh(hero_1)  # reload (expired init)
    print("Updated hero:", hero_1)

# select
with Session(engine) as session:
    heroes = session.exec(select(Hero)).all()
    print("All heroes:", heroes)

    hero = session.exec(select(Hero)).first()
    print("First hero:", hero)

    hero = session.exec(select(Hero).where(Hero.name == "Deadpond")).first()
    print("Filtered hero:", hero)

    hero = session.exec(select(Hero).filter_by(name="Deadpond")).first()
    print("Filtered by hero:", hero)


@app.get("/heroes")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
