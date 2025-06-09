from fastapi import APIRouter

games_router = APIRouter()

@games_router.post("/create")
async def create_game(name: str):
    return {"message": f"Game {name} created"}
