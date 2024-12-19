from fastapi import APIRouter, HTTPException, Path
from ..data import add_pokemon, get_pokemon, put_pokemon, del_pokemon
from ..models.pokemon import Pokemon

router = APIRouter(prefix="/pokemon")


#===========================GET============================
@router.get("/{id}", response_model=Pokemon)
async def get_pokemon_by_id(id: int = Path(ge=1)) -> Pokemon:
    pokemon = get_pokemon(id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Ce pokemon n'existe pas")
    return pokemon


#===========================POST============================
@router.post("/", response_model=Pokemon)
async def create_pokemon(pokemon: Pokemon) -> Pokemon:
    if add_pokemon(pokemon):
        raise HTTPException(status_code=404, detail=f"Le pokemon {pokemon.id} existe déjà !")
    return pokemon


#===========================PUT============================
@router.put("/{id}", response_model=Pokemon)
async def update_pokemon(pokemon: Pokemon, id: int = Path(ge=1)) -> Pokemon:
    if not put_pokemon(pokemon):
        raise HTTPException(status_code=404, detail=f"Le pokemon {id} n'existe pas.")
    return pokemon


#===========================DELETE============================
@router.delete("/{id}", response_model=Pokemon)
async def delete_pokemon(id: int = Path(ge=1)) -> Pokemon:
    pokemon = del_pokemon(id)
    if pokemon is None:
        raise HTTPException(status_code=404, detail=f"Le pokemon {id} n'existe pas.")
    return pokemon
