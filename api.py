from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()



#creating apis
@app.get("/")
def first_api():
    return "this is my first api"


@app.get("/users")
def get_users():
    users = {
        "users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}  
        ]
    }
    return users


#creting class for request
class Student(BaseModel):
    name: str
    age: int
    course: str
    
 
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None
    

#data for students
students = {
    1: {
        "name": "John Doe",
        "age": 21,
        "course": "Computer Science"
    },
    2: {
        "name": "Jane Smith",
        "age": 22,
        "course": "Mathematics" 
    },
    3: {
        "name": "Mike Johnson",
        "age": 20,
        "course": "Physics"
    },
    4: {
        "name": "Emily Davis",
        "age": 23,
        "course": "Chemistry"
    }
    
}

#path parameters

@app.get("/students/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student to retrieve", gt=0, lt=1000)):
    student = students.get(student_id)
    if student:
        return student
    return {"error": "Student not found"}
    
#Query Parameters
#note: python dosent allow Optional arguments before required arguments if you use *
@app.get("/search-by-name/")
def get_student(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"error": "Student not found"}


    
    
#request body and post method
@app.post("/students/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"error": "Student ID already exists"}
    students[student_id] = student
    return students[student_id]

#update student info using put method
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"error": "Student not found"}

    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.course != None:
        students[student_id].course = student.course
    
    return students[student_id]

#api to delete student
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"error": "Student not found"}
    del students[student_id]
    return {"message": "Student deleted successfully"}

