from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ... import schemas
from . import crud

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)

@router.get("/{category_id}")
async def find_category(category_id: int, db: Session = Depends(get_db)):
    return crud.get_category_by_id(db, category_id)

@router.post("/")
async def create_category(category: schemas.Category, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already registered")
    return crud.create_category(db, category)

@router.put("/{category_id}")
async def update_category(category_id: int, new_category: schemas.Category, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db, category_id)
    if db_category:
        return crud.update_category(db, category_id, new_category)
    raise HTTPException(status_code=400, detail="Category doesn't exists")

@router.delete("/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_id(db, category_id)
    if db_category:
        crud.delete_category(db, category_id)
        return {"detail": "Category deleted successfully!"}
    raise HTTPException(status_code=400, detail="Category doesn't exists")