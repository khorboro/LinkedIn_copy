from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title='LinkedIn'
)


class User(BaseModel):
    username: str
    name: str
    age: int


DB = []


@app.post("/users")
async def register_user(username: User):
    """Register a new user if it doesn't exist yet."""
    if username in DB:
        raise HTTPException(409, f"User with username '{username}' is already exists.")

    DB.append(username)
    return {"message": "User registered successfully"}


@app.get("/users")
async def get_user(username: str):
    found_user = [x for x in DB if x.username == username]
    if not found_user:
        raise HTTPException(404, f"User with username '{username}' does not exist.")
    return found_user[0]


@app.put("/users")
async def change_age(username: str, new_age: int):
    """Change user age."""
    user = next((user for user in DB if user.username == username), None)
    if user is None:
        raise HTTPException(404, f"User with username '{username}' does not exist.")

    user.age = new_age
    return {"message": f"Age for user '{username}' updated successfully"}


@app.delete("/users")
async def delete_user(username):
    """Delete existing user."""
    user = next((user for user in DB if user.username == username), None)
    if user is None:
        raise HTTPException(404, f"User with username '{username}' does not exist.")

    DB.remove(user)
    return {"message": f"User '{username}' deleted successfully"}
