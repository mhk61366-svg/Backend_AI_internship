from fastapi import FastAPI, HTTPException
from service import UserService
from postgres_repository import PostgresUserRepository
from schemas import UserCreate, UserUpdate, UserResponse, UsersListResponse, DeleteResponse
from auth_routes import router as auth_router
from llm_routes import router as llm_router

repo = PostgresUserRepository()
service = UserService(repo)

app = FastAPI()
app.include_router(auth_router)
app.include_router(llm_router)

@app.get("/get_users", response_model=UsersListResponse)
def get_users():
    return service.get_all_users()

@app.get("/get_user/{id}", response_model=UserResponse)
def get_user_by_id(id: int):
    result = service.get_user_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="user not found")
    return result

@app.post("/create_user", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate):
    return service.create_user(user_data.model_dump())

@app.put("/update_user/{id}", response_model=UserResponse)
def update_user(id: int, user_data: UserUpdate):
    result = service.update_user(id, user_data.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="user not found")
    return result

@app.delete("/delete_user/{id}", response_model=DeleteResponse)
def delete_user(id: int):
    result = service.delete_user(id)
    if not result:
        raise HTTPException(status_code=404, detail="user not found")
    return result