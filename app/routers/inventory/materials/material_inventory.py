from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ....dependencies import get_db
from .... import schemas
from . import crud
from ...material.crud import get_material_by_title

router = APIRouter(
    prefix="/material/inventory",
    tags=["material inventory"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_inventory(db: Session = Depends(get_db)):
    return crud.list_inventory(db)

@router.get("/{material_id}")
async def find_inventory(material_id: int, db: Session = Depends(get_db)):
    return crud.get_material_inventory(db, material_id)

@router.post("/")
async def save_inventory(inventory: schemas.MaterialInventory, db: Session = Depends(get_db)):
    db_material = get_material_by_title(db, inventory.material.title)
    if not db_material:
        raise HTTPException(status_code=400, detail="Material doesn't exists")
    db_inventory = crud.get_material_inventory(db, db_material.id)
    if db_inventory:
        return crud.update_stock_inventory(db, db_material.id, inventory)
    return crud.create_inventory(db, inventory)

@router.put("/{material_id}")
async def update_inventory(material_id: int, new_inventory: schemas.MaterialInventory, db: Session = Depends(get_db)):
    db_inventory = crud.get_material_inventory(db, material_id)
    if db_inventory:
        return crud.update_inventory(db, material_id, new_inventory)
    raise HTTPException(status_code=400, detail="Inventory doesn't exists")

@router.delete("/{material_id}")
async def delete_inventory(material_id: int, db: Session = Depends(get_db)):
    db_inventory = crud.get_material_inventory(db, material_id)
    if db_inventory:
        crud.delete_inventory(db, material_id)
        return {"detail": "Inventory deleted successfully!"}
    raise HTTPException(status_code=400, detail="Inventory doesn't exists")