from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ....dependencies import get_db
from .... import schemas
from . import crud
from ...product.crud import get_product_by_title

router = APIRouter(
    prefix="/product/inventory",
    tags=["product inventory"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_inventory(db: Session = Depends(get_db)):
    return crud.list_inventory(db)

@router.get("/{product_id}")
async def find_inventory(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product_inventory(db, product_id)

@router.post("/")
async def save_inventory(inventory: schemas.ProductInventory, db: Session = Depends(get_db)):
    db_product = get_product_by_title(db, inventory.product.title)
    if not db_product:
        raise HTTPException(status_code=400, detail="Product doesn't exists")
    db_inventory = crud.get_product_inventory(db, db_product.id)
    if db_inventory:
        return crud.update_stock_inventory(db, db_product.id, inventory)
    return crud.create_inventory(db, inventory)

@router.put("/{product_id}")
async def update_inventory(product_id: int, new_inventory: schemas.ProductInventory, db: Session = Depends(get_db)):
    db_inventory = crud.get_product_inventory(db, product_id)
    if db_inventory:
        return crud.update_inventory(db, product_id, new_inventory)
    raise HTTPException(status_code=400, detail="Inventory doesn't exists")

@router.delete("/{product_id}")
async def delete_inventory(product_id: int, db: Session = Depends(get_db)):
    db_inventory = crud.get_product_inventory(db, product_id)
    if db_inventory:
        crud.delete_inventory(db, product_id)
        return {"detail": "Inventory deleted successfully!"}
    raise HTTPException(status_code=400, detail="Inventory doesn't exists")