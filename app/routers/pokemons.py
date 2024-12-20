from fastapi import APIRouter, HTTPException, Depends
import math

from ..auth import get_current_active_user
from ..models import Pokemon, User
from ..data import get_data
from .. import main_logger


router = APIRouter(prefix="/pokemons")


#===========================GET============================
@router.get("/total")
async def get_total_pokemons(current_user: User = Depends(get_current_active_user)) -> dict:
    main_logger.info(f"User {current_user.username} is requesting the total number of pokemons")
    return {"total": len(get_data())}


@router.get("", response_model=list[Pokemon])
async def get_all_pokemons1(current_user: User = Depends(get_current_active_user)) -> list[Pokemon]:
    main_logger.info(f"User {current_user.username} is requesting all pokemons")
    return get_data()


@router.get("/", response_model=list[Pokemon])
async def get_all_pokemons(page: int = 1, items: int = 10, current_user: User = Depends(get_current_active_user)) -> list[Pokemon]:
    items = min(items, 20)
    max_page = math.ceil(len(get_data()) / items)
    current_page = min(page, max_page)
    start = (current_page - 1) * items
    stop = start + items
    main_logger.info(f"User {current_user.username} is requesting page {current_page} of pokemons with {items} items")
    return get_data()[start:stop]


@router.get("search/", response_model=list[Pokemon] | None)
async def search_pokemons(
    types: str | None = None,
    evo: str | None = None,
    totalgt: int | None = None,
    totallt: int | None = None,
    sortby: str | None = None,
    order: str | None = None,
    current_user: User = Depends(get_current_active_user)
) -> list[Pokemon] | None:
    main_logger.info(f"User {current_user.username} is searching for pokemons with types {types}, evo {evo}, totalgt {totalgt}, totallt {totallt}, sortby {sortby}, order {order}")

    filtered_list = []
    data = [pokemon.model_dump() for pokemon in get_data()]

    #On filtre les types
    if types is not None :
        for pokemon in data :
            if set(types.split(",")).issubset(pokemon["types"]) :
                filtered_list.append(pokemon)

    #On filtre les evolutions
    if evo is not None :
        tmp = filtered_list if filtered_list else data
        new = []

        for pokemon in tmp :
            if evo == "true" and "evolution_id" in pokemon:
                new.append(pokemon)
            if evo == "false" and "evolution_id" not in pokemon:
                new.append(pokemon)

        filtered_list = new

    #On filtre sur greater than total
    if totalgt is not None :
        tmp = filtered_list if filtered_list else data
        new = []

        for pokemon in tmp :
            if pokemon["total"] > totalgt:
                new.append(pokemon)

        filtered_list = new

    #On filtre sur less than total
    if totallt is not None :
        tmp = filtered_list if filtered_list else data
        new = []

        for pokemon in tmp :
            if pokemon["total"] < totallt:
                new.append(pokemon)

        filtered_list = new

    #On gére le tri
    if sortby is not None and sortby in ["id","name","total"] :
        filtered_list = filtered_list if filtered_list else data
        sorting_order = False
        if order == "asc" : sorting_order = False
        if order == "desc" : sorting_order = True

        filtered_list = sorted(filtered_list, key=lambda d: d[sortby], reverse=sorting_order)

    if filtered_list:
        return [Pokemon(**pokemon) for pokemon in filtered_list]
    
    raise HTTPException(status_code=404, detail="Aucun Pokemon ne répond aux critères de recherche")
