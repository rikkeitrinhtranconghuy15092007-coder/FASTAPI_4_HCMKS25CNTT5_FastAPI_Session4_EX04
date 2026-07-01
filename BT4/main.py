from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

# Giả lập Database đã có sẵn một học viên để test bẫy trùng email
students_db = [
    {
        "id": 1,
        "full_name": "Nguyen Van B",
        "email": "existing@gmail.com",
        "age": 25,
        "course": "python",
        "phone": "0123456789"
    }
]

class StudentCreate(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int = Field(..., ge=1)
    course: str = Field(..., min_length=1)
    phone: str = Field(..., pattern=r"^\d{10,11}$")


@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student_in: StudentCreate):
    for student in students_db:
        if student["email"] == student_in.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email đã tồn tại trong hệ thống"
            )
            
    new_id = max(s["id"] for s in students_db) + 1 if students_db else 1
    
    new_student = {
        "id": new_id,
        "full_name": student_in.full_name,
        "email": student_in.email,
        "age": student_in.age,
        "course": student_in.course,
        "phone": student_in.phone
    }
    
    students_db.append(new_student)
    
    return {
        "message": "Đăng ký học viên thành công",
        "data": new_student
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)