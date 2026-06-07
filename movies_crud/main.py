from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from movies_crud.routes.routes import router
from movies_crud.database import database
from movies_crud.models import movie_model 


database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Movies CRUD API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #  HTML con la API
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE
    allow_headers=["*"],
)
# ---------------------------------------------------------------------------------

# Incluimos las rutas con el prefijo v1
app.include_router(router, prefix="/v1")

@app.get("/")
def root():
    return {"message": "Movies API server is running smoothly!"}