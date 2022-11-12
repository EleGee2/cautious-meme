from fastapi import FastAPI, Body, Depends
import schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session

    finally:
        session.close()


app = FastAPI()

fakeDatabase = {
    1: {"task": "Learn FastAPI"},
    2: {"task": "Learn Docker"},
    3: {"task": "Learn Kubernetes"},
}


@app.get("/")
async def get_items(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get("/{id}")
async def get_item(id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).filter(models.Item.id == id).first()
    return item


@app.post("/")
def add_item(item: schemas.Item, session: Session = Depends(get_session)):
    db_item = models.Item(task=item.task)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


# @app.post("/")
# def add_item(task: str):
#     new_id = len(fakeDatabase) + 1
#     fakeDatabase[new_id] = {"task": task}
#     return fakeDatabase


# @app.post("/")
# def add_item(body=Body()):
#     new_id = len(fakeDatabase) + 1
#     fakeDatabase[new_id] = {"task": body["task"]}
#     return fakeDatabase


@app.put("/{id}")
def update_item(id: int, item: schemas.Item, session: Session = Depends(get_session)):
    db_item = session.query(models.Item).filter(models.Item.id == id).first()
    db_item.task = item.task
    session.commit()
    session.refresh(db_item)
    return db_item


@app.delete("/{id}")
def delete_item(id: int, session: Session = Depends(get_session)):
    db_item = session.query(models.Item).filter(models.Item.id == id).first()
    session.delete(db_item)
    session.commit()
    session.close()
    return {"message": "Item deleted successfully!"}
