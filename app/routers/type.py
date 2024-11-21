from typing import List
from fastapi import APIRouter
from ..data import get_data

router = APIRouter(prefix="/pokemons")

#===========================GET============================
@router.get("/types")
def get_all_types() -> List[str]:
    types = set()
    for pokemon in get_data():
        types.update(pokemon["types"])
    return sorted(types)
