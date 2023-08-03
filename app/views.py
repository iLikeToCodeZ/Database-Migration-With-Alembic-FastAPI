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
    """Checks the status of the FastAPI app.

    Returns:
        status: Success or Error
    """
    try:
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}


@router.post("/import-csv/")
async def import_csv(file: UploadFile = File(...)):
    """FastAPI endpoint that imports CSV files through the FastAPI UI and populates the data.

    Args:
        file (UploadFile, optional): Uploads a file into FastAPI. Defaults to File(...).

    Raises:
        HTTPException: If an invalid file type is uploaded, raise this error.

    Returns:
        message: Validates a successful upload.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV files are allowed.")
    
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
    """FastAPI endpoint that queries the database. Filtering on Business ID and/or Symptom Diagnostic.

    Args:
        business_id (int, optional): A unique identifier that represents a business. Defaults to Query(None, description="Filter by Business ID").
        diagnostic (str, optional): Value that establishes whether a business was diagnosed with a symptom or not. Defaults to Query(None, description="Filter by Symptom Diagnostic").
        db (Session, optional): Database Dependecy. Defaults to Depends(get_db).

    Raises:
        HTTPException: Checks for an empty response.

    Returns:
        results: Queried data response.
    """
    query = db.query(BusinessSymptom)

    if business_id:
        query = query.filter(BusinessSymptom.business_id == business_id)

    if diagnostic:
        query = query.filter(BusinessSymptom.symptom_diagnostic == diagnostic)

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No data found")

    return results
