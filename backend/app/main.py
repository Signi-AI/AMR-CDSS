from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os


from app.api.v1.routers import auth,patient,clinical_visit,pathogen,antimicrobial,result_analyis,cell_cont,clinical_rule,workflow
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Clinical Decision Support System Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(clinical_visit.router)
app.include_router(result_analyis.router)
app.include_router(pathogen.router)
app.include_router(antimicrobial.router)
app.include_router(cell_cont.router)
app.include_router(clinical_rule.router)
app.include_router(workflow.router)


os.makedirs("uploads", exist_ok=True)
app.mount("/uplaods", StaticFiles(directory="uploads"), name="uploads")

@app.get("/test")
def test():
    return{
        "message":"welcome to our clinical support system backend"
    }