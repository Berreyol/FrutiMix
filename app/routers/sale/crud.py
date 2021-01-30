from sqlalchemy.orm import Session
from sqlalchemy import cast, DATE, and_
from ... import models, schemas
from ..product.crud import get_product_by_title, get_product_by_id
from datetime import datetime, date, timezone

def list_sale(db: Session):
    return db.query(models.Sale).all()

def get_sale_by_id(db: Session, sale_id: int):
    return db.query(models.Sale).filter(models.Sale.id == sale_id).first()

def get_sales_by_product(db: Session, product_id: int):
    return db.query(models.Sale).filter(models.Sale.product_id == product_id).all()

def get_sales_by_date(db: Session, created_at: date):
    return db.query(models.Sale) \
        .filter(cast(models.Sale.created_at, DATE) == created_at) \
        .all()

def get_sales_by_date_range(db: Session, start: date, end: date):
    return db.query(models.Sale) \
        .filter(and_(
            cast(models.Sale.created_at, DATE) >= start,
            cast(models.Sale.created_at, DATE) <= end)).all() 

def get_sales_by_datetime_range(db: Session, start: datetime, end: datetime):
    return db.query(models.Sale).filter(models.Sale.created_at.between(start, end)).all()

def create_sale(db: Session, sale: schemas.Sale):
    created_at = datetime.now(timezone.utc)
    db_sale = models.Sale(
        created_at = created_at,
        total = sale.total
    )
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def create_sale_details(db: Session, sale_id: int, sale: schemas.Sale):
    for detail in sale.details:
        db_product = get_product_by_title(db, detail.product.title)
        db_sale_detail = models.SaleDetail(
            sale_id = sale_id,
            product_id = db_product.id,
            quantity = detail.quantity
        )   
        db.add(db_sale_detail)
    db.commit()

def update_sale(db: Session, sale_id: int, sale: schemas.Sale):
    db_product = get_product_by_id(db, sale_id)
    db_sale = get_sale_by_id(db, product_id)
    db_sale.quantity = sale.quantity
    db_sale.total = sale.quantity * db_product.price
    db.commit()
    db.refresh(db_sale)
    return db_sale

def delete_sale(db: Session, sale_id: int):
    db_sale = get_sale_by_id(db, sale_id)
    db.delete(db_sale)
    db.commit()