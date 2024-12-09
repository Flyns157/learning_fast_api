from fastapi import APIRouter, HTTPException, Path
from ..data import get_data, get_pokemon, put_pokemon, del_pokemon
from ..models.pokemon import Pokemon

router = APIRouter(prefix="/pokemon")


#===========================GET============================
@router.get("/total")
async def get_total_pokemons() -> dict:
    return {"total": len(get_data())}

@router.get("/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int = Path(ge=1)) -> Pokemon:
    if id not in get_data():
        raise HTTPException(status_code=404, detail="Ce pokemon n'existe pas")
    
    return Pokemon(**get_pokemon(id))

#===========================POST============================
@router.post("/", response_model=Pokemon)
async def create_pokemon(pokemon: Pokemon) -> Pokemon:
    if pokemon.id in get_pokemon():
        raise HTTPException(status_code=404, detail=f"Le pokemon {pokemon.id} existe déjà !")
    
    put_pokemon(pokemon.id, pokemon.dict())
    return pokemon

#===========================PUT============================
@router.put("/{id}", response_model=Pokemon)
async def update_pokemon(pokemon: Pokemon, id: int = Path(ge=1)) -> Pokemon:
    if id not in get_data():
        raise HTTPException(status_code=404, detail=f"Le pokemon {id} n'existe pas.")
    
    put_pokemon(id, pokemon.model_dump())
    return pokemon

#===========================DELETE============================
@router.delete("/{id}", response_model=Pokemon)
async def delete_pokemon(id: int = Path(ge=1)) -> Pokemon:
    if id in get_data():
        pokemon = Pokemon(**get_pokemon(id))
        del_pokemon(id)
        return pokemon
    
    raise HTTPException(status_code=404, detail=f"Le pokemon {id} n'existe pas.")
