from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ...dependencies import get_db
from ... import schemas
from . import crud

router = APIRouter(
    prefix="/materials",
    tags=["materials"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_materials(db: Session = Depends(get_db)):
    return crud.list_materials(db)

@router.get("/{material_id}")
async def find_material(material_id: int, db: Session = Depends(get_db)):
    return crud.get_material_by_id(db, material_id)

@router.post("/")
async def save_material(material: schemas.Material, db: Session = Depends(get_db)):
    db_material = crud.get_material_by_title(db, material.title)
    if db_material:
        raise HTTPException(status_code=400, detail="Material already registered")
    return crud.create_material(db=db, material=material)

@router.put("/{material_id}")
async def update_material(material_id: int, new_material: schemas.Material, db: Session = Depends(get_db)):
    db_material = crud.get_material_by_id(db, material_id)
    if db_material:
        return crud.update_material(db, material_id, new_material)
    raise HTTPException(status_code=400, detail="Material doesn't exists")

@router.delete("/{material_id}")
async def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = crud.get_material_by_id(db, material_id)
    if db_material:
        crud.delete_material(db, material_id)
        return {"detail": "Material deleted successfully!"}
    raise HTTPException(status_code=400, detail="Material doesn't exists")
