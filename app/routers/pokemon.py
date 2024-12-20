from fastapi import APIRouter, HTTPException, Path, Depends
from ..data import add_pokemon, get_pokemon, put_pokemon, del_pokemon
from ..models import Pokemon, User
from ..auth import get_current_active_user
from .. import main_logger

router = APIRouter(prefix="/pokemon")


#===========================GET============================
@router.get("/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int = Path(ge=1), current_user: User = Depends(get_current_active_user)) -> Pokemon:
    pokemon = get_pokemon(id)
    if not pokemon:
        main_logger.warning(f"Pokemon {id} non trouvé par {current_user.username}")
        raise HTTPException(status_code=404, detail="Ce pokemon n'existe pas")
    main_logger.info(f"Pokemon {id} récupéré par {current_user.username}")
    return pokemon


#===========================POST============================
@router.post("/", response_model=Pokemon)
async def create_pokemon(pokemon: Pokemon, current_user: User = Depends(get_current_active_user)) -> Pokemon:
    if add_pokemon(pokemon):
        main_logger.info(f"Pokemon {pokemon.id} créé par {current_user.username}")
        return pokemon
    main_logger.warning(f"Pokemon {pokemon.id} non créé par {current_user.username} car il existe déjà")
    raise HTTPException(status_code=404, detail=f"Le pokemon {pokemon.id} existe déjà !")


#===========================PUT============================
@router.put("/{id}", response_model=Pokemon)
async def update_pokemon(pokemon: Pokemon, id: int = Path(ge=1), current_user: User = Depends(get_current_active_user)) -> Pokemon:
    if put_pokemon(pokemon):
        main_logger.info(f"Pokemon {id} mis à jour par {current_user.username}")
        return pokemon
    main_logger.warning(f"Pokemon {id} non mis à jour par {current_user.username} car il n'existe pas")
    raise HTTPException(status_code=404, detail=f"Le pokemon {id} n'existe pas.")


#===========================DELETE============================
@router.delete("/{id}", response_model=Pokemon)
async def delete_pokemon(id: int = Path(ge=1), current_user: User = Depends(get_current_active_user)) -> Pokemon:
    pokemon = del_pokemon(id)
    if pokemon:
        main_logger.info(f"Pokemon {id} supprimé par {current_user.username}")
        return pokemon
    main_logger.warning(f"Pokemon {id} non supprimé par {current_user.username} car il n'existe pas")
    raise HTTPException(status_code=404, detail=f"Le pokemon {id} n'existe pas.")
