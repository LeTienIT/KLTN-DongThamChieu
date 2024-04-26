from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from main import dong_tham_chieu

app = FastAPI()

class InputData(BaseModel):
    cau: str

@app.post("/dong-tham-chieu/")
def process_data(data: InputData):
    result = dong_tham_chieu(data.cau)
    return result