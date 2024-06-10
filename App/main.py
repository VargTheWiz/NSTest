from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    #обаботка ошибки недоступности базы данных
    try:
        yield db
    finally:
        db.close()

#добавить рулон на склад
@app.post("/rolls/", response_model=schemas.Roll)
def create_roll(roll: schemas.RollCreate, db: Session = Depends(get_db)):
    return crud.create_roll(db=db, roll=roll)
    
#получить список рулонов со склада, лимит до 100, сортировка по ид с 1 до х
@app.get("/rolls/", response_model=list[schemas.Roll])
def read_rolls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rolls = crud.get_rolls(db, skip=skip, limit=limit)
    return rolls
    
#получить список рулонов которые сейчас на складе
@app.get("/rollsonsite/", response_model=list[schemas.Roll])
def read_onsite_rolls(db: Session = Depends(get_db)):
    rolls = crud.get_onsite_rolls(db)
    return rolls

#фильтрации по одному из диапазонов единовременно (id/веса/длины/даты добавления/даты удаления со склада)
#посомтреть все рулоны с фильтром по ид
@app.get("/rollsfilteredbyid/", response_model=list[schemas.Roll])
def read_filtered_rolls_by_id(start: int, end: int, db: Session = Depends(get_db)):
    if (start > end):
        temp = end
        end = start
        start = temp
        print("Start should be less than end")
    rolls = crud.get_filtered_rolls_by_id(db, start=start, end=end)
    return rolls

#посомтреть все рулоны с фильтром по весу
@app.get("/rollsfilteredbyweight/", response_model=list[schemas.Roll])
def read_filtered_rolls_by_weight(start: float, end: float, db: Session = Depends(get_db)):
    if (start > end):
        temp = end
        end = start
        start = temp
        print("Start should be less than end")
    rolls = crud.get_filtered_rolls_by_weight(db, start=start, end=end)
    return rolls

#посомтреть все рулоны с фильтром по длине
@app.get("/rollsfilteredbylength/", response_model=list[schemas.Roll])
def read_filtered_rolls_by_length(start: int, end: int, db: Session = Depends(get_db)):
    if (start > end):
        temp = end
        end = start
        start = temp
        print("Start should be less than end")
    rolls = crud.get_filtered_rolls_by_length(db, start=start, end=end)
    return rolls
    
#посомтреть все рулоны с фильтром по дате добавления
@app.get("/rollsfilteredbydateadd/", response_model=list[schemas.Roll])
def read_filtered_rolls_by_dateadd(start: datetime, end: datetime, db: Session = Depends(get_db)):
    if (start > end):
        temp = end
        end = start
        start = temp
        print("Start should be less than end")
    rolls = crud.get_filtered_rolls_by_dateadd(db, start=start, end=end)
    return rolls
    
#посомтреть все рулоны с фильтром по дате удаления
@app.get("/rollsfilteredbydateremove/", response_model=list[schemas.Roll])
def read_filtered_rolls_by_dateremove(start: datetime, end: datetime, db: Session = Depends(get_db)):
    if (start > end):
        temp = end
        end = start
        start = temp
        print("Start should be less than end")
    rolls = crud.get_filtered_rolls_by_dateremove(db, start=start, end=end)
    return rolls


@app.get("/statistics/")
def get_all_statistics(start: datetime, end: datetime, db: Session = Depends(get_db)):
    return crud.get_statistics(db, start, end)

#посмотреть один рулон
@app.get("/rolls/{roll_id}", response_model=schemas.Roll)
def read_roll(roll_id: int, db: Session = Depends(get_db)):
    db_roll = crud.get_roll(db, roll_id=roll_id)
    if db_roll is None:
        raise HTTPException(status_code=404, detail="Roll not found")
    return db_roll
    
#рулон остается в базе данных, но получает дату вывоза
@app.patch("/rolls/{roll_id}", response_model=schemas.Roll)
def remove_roll(roll_id: int, roll: schemas.RollRemove, db: Session = Depends(get_db)):
    db_roll = crud.get_roll(db, roll_id=roll_id)
    if db_roll is None:
        raise HTTPException(status_code=404, detail="Roll not found")
    roll_removed = crud.remove_roll(db=db, roll=roll, roll_id=roll_id)#передаем именно RollRemove, в краде разберемся
    return roll_removed


