from fastapi import FastAPI

from .database import engine
from . import models

from .routers.material import materials
from .routers.product import products
from .routers.category import categories
from .routers.inventory.materials import material_inventory
from .routers.inventory.products import product_inventory
from .routers.sale import sales

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.router.redirect_slashes = False
app.include_router(materials.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(material_inventory.router)
app.include_router(product_inventory.router)
app.include_router(sales.router)

@app.get("/")
async def home():
    return {"message": "Hello from frutimix"}
