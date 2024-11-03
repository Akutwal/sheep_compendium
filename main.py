# main.py
from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep

app = FastAPI()


@app.get(path="/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    return db.get_sheep(id)


@app.post(path="/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    # Check if the sheep ID already exists to avoid duplicates
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

    # Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep


@app.delete(path="/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    # Check if sheep exists
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")

    # Delete the sheep
    del db.data[id]
    return None


@app.put(path="/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep: Sheep):
    # Check if sheep exists
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")

    # Verify ID in path matches sheep ID
    if id != sheep.id:
        raise HTTPException(status_code=400, detail="Path ID does not match sheep ID")

    # Update the sheep
    db.data[id] = sheep
    return sheep


@app.get(path="/sheep/", response_model=list[Sheep])
def read_all_sheep():
    # Return all sheep as a list
    return list(db.data.values())