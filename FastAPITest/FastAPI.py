from fastapi import FastAPI
from random import randint
from enum import Enum


class StudentName (str, Enum):
    loki = "loki"
    emil = "emil"
    rikki = "rikki"


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/students/{student_name}")
async def get_student_info(student_name: StudentName):
    if student_name == StudentName.loki:
        return {"student_name": student_name, "message": "He's a good boy"}
    elif student_name == StudentName.emil:
        return {"student_name": student_name, "message": "He's a handsome boy"}
    elif student_name == StudentName.rikki:
        return {"student_name": student_name, "message": "He's a smart boy"}



@app.get("/number")
async def number_generator():
    return {"some_number": randint(0, 33)}

@app.get("/my_page/{my_id}")
async def my_page(my_id: int):
    return {"my_id": my_id}
