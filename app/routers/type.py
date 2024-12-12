from fastapi import APIRouter
from ..data import get_data


router = APIRouter(prefix="/pokemons")


#===========================GET============================
@router.get("/types")
async def get_all_types() -> list[str]:
    types = set()
    for pokemon in get_data():
        types.update(pokemon["types"])
    return sorted(types)
