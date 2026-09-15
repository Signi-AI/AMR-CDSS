from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.core import seed
from app.auth import loginroute


from app.api.v1.routers import patient,clinical_visit,pathogen,antimicrobial,result_analyis,cell_cont,clinical_rule
from backend.app.api.v1.routers import user

app=FastAPI(title="Clinical Decision Support System Backend")

app.include_router(loginroute.router)
app.include_router(user.router)
app.include_router(patient.router)
app.include_router(clinical_visit.router)
app.include_router(result_analyis.router)
app.include_router(pathogen.router)
app.include_router(antimicrobial.router)
app.include_router(cell_cont.router)
app.include_router(clinical_rule.router)
app.include_router(seed.router)



os.makedirs("uploads", exist_ok=True)
app.mount("/uplaods", StaticFiles(directory="uploads"), name="uploads")

@app.get("/test")
def test():
    return{
        "message":"welcome to our clinical support system backend"
    }