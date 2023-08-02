from fastapi import APIRouter, UploadFile, File, Query, Depends, HTTPException
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import BusinessSymptom
import pandas as pd

router       = APIRouter()
engine       = create_engine("postgresql://postgres:root@localhost/advinow")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get('/status')
async def get_status():
    try:
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}


@router.post("/import-csv/")
async def import_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files are allowed.")
    
    # contents = await file.file.read()
    csv_data = pd.read_csv(file.file)
    
    with SessionLocal() as session:
        for i, row in csv_data.iterrows():
            data = BusinessSymptom(
                id                 = i+1,
                business_id        = row['Business ID'],
                business_name      = row['Business Name'],
                symptom_code       = row['Symptom Code'],
                symptom_name       = row['Symptom Name'],
                symptom_diagnostic = row['Symptom Diagnostic']
            )
            session.add(data)
        session.commit()
    
    return {"message": "CSV file imported successfully"}
    

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI endpoint to get business and symptom data
@router.get("/business-symptoms/")
async def get_business_symptoms(
    business_id : int     = Query(None, description="Filter by Business ID"),
    diagnostic  : str     = Query(None, description="Filter by Symptom Diagnostic"),
    db          : Session = Depends(get_db)
):
    query = db.query(BusinessSymptom)

    if business_id:
        query = query.filter(BusinessSymptom.business_id == business_id)

    if diagnostic:
        query = query.filter(BusinessSymptom.symptom_diagnostic == diagnostic)

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No data found")

    return results
