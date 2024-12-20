from fastapi import APIRouter, Depends

from ..auth import get_current_active_user
from ..data import get_data
from .. import main_logger
from ..models import User


router = APIRouter(prefix="/pokemons")


#===========================GET============================
@router.get("/types")
async def get_all_types(current_user: User = Depends(get_current_active_user)) -> list[str]:
    main_logger.info(f"User {current_user.username} accessed all types")
    types = set()
    for pokemon in get_data():
        types.update(pokemon.types)
    return sorted(types)
