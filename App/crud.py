from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from datetime import datetime, date
from sqlalchemy import func, text

from . import models, schemas


def get_roll(db: Session, roll_id: int):
    return db.query(models.Roll).filter(models.Roll.id == roll_id).first()
    
def get_rolls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Roll).offset(skip).limit(limit).all()
    
def get_onsite_rolls(db: Session):
    return db.query(models.Roll).filter(models.Roll.dateremove == None)
    
def get_filtered_rolls_by_id(db: Session, start: int, end: int):
    return db.query(models.Roll).filter(models.Roll.id >= start, models.Roll.id <= end).all()
    
def get_filtered_rolls_by_weight(db: Session, start: float, end: float):
    return db.query(models.Roll).filter(models.Roll.weight >= start, models.Roll.weight <= end).all()

def get_filtered_rolls_by_length(db: Session, start: int, end: int):
    return db.query(models.Roll).filter(models.Roll.length >= start, models.Roll.length <= end).all()

def get_filtered_rolls_by_dateadd(db: Session, start: datetime, end: datetime):
    #технически оно работает, надо только помнить что дата начинается с 00:00
    return db.query(models.Roll).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).all()

def get_filtered_rolls_by_dateremove(db: Session, start: datetime, end: datetime):
    #технически оно работает, надо только помнить что дата начинается с 00:00
    return db.query(models.Roll).filter(models.Roll.dateremove >= start, models.Roll.dateremove <= end).all()
    
def get_statistics(db: Session, start: datetime, end: datetime):
    #всего записей в таблице, всего удалено со склада, всего на складе за период
    rolls_count = db.query(models.Roll).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).count()
    rolls_removed_count = db.query(models.Roll).filter(models.Roll.dateremove != None, models.Roll.dateadd >= start, models.Roll.dateadd <= end).count()
    rolls_cur_count = db.query(models.Roll).filter(models.Roll.dateremove == None, models.Roll.dateadd >= start, models.Roll.dateadd <= end).count()
    
    #средняя, макс, мин длина за период
    rolls_mean_length = db.query(func.avg(models.Roll.length)).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    rolls_max_length = db.query(func.max(models.Roll.length)).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    rolls_min_length = db.query(func.min(models.Roll.length)).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    
    #средний, макс, мин вес за период
    rolls_mean_weight = db.query(func.avg(models.Roll.weight)).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    rolls_max_weight = db.query(func.max(models.Roll.weight)).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    rolls_min_weight = db.query(func.min(models.Roll.weight)).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    
    #сумма веса рулонов за период
    rolls_sum_weight = db.query(func.sum(models.Roll.weight)).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    
    #максимальный промежуток между добавлением и удалением рулона
    
    #rolls_max_datemargin = db.query(func.max(func.timediff(models.Roll.dateremove, models.Roll.dateadd)  )).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    #no timediff | datadiff function?
    
    #rolls_max_datemargin = db.query(func.max(func.timestampdiff(models.Roll.dateremove, models.Roll.dateadd))).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    #no timediff | datadiff function?
    
    #rolls_max_datemargin = db.query(func.max(models.Roll.dateremove.timestamp() - models.Roll.dateadd.timestamp())).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    #no attribute "timestamp()"
    
    #rolls_max_datemargin = db.query(func.max(models.Roll.dateremove - models.Roll.dateadd)).filter(models.Roll.dateadd >= start, models.Roll.dateadd <= end).scalar()
    
    #сдаюсь print(rolls_max_datemargin)

    #минимальный промежуток между добавлением и удалением рулона
    
    return {'Всего рулонов в ДБ ':rolls_count, 
            'Рулонов выдно: ':rolls_removed_count, 
            'Рулонов сейчас на складе: ':rolls_cur_count,
            'Средняя длина рулона ':rolls_mean_length,
            'Максимальная длина рулона ':rolls_max_length,
            'Минимальная длина рулона ':rolls_min_length,
            'Средний вес рулона ':rolls_mean_weight,
            'Максимальный вес рулона ':rolls_max_weight,
            'Минимальный вес рулона ':rolls_min_weight,
            'Сумма веса рулонов ':rolls_sum_weight
            }

def create_roll(db: Session, roll: schemas.RollCreate):
    db_roll = models.Roll(length=roll.length, weight=roll.weight)
    db.add(db_roll)
    db.commit()
    db.refresh(db_roll)
    return db_roll

def remove_roll(db: Session, roll: schemas.RollRemove, roll_id: int):
    #проверим что рулон существует
    roll_data = roll.model_dump(exclude_unset=True)#получили данные которые будем обновлять
    db.query(models.Roll).filter(models.Roll.id == roll_id).update(roll_data)#обновляем бдa
    db.commit()
    return db.query(models.Roll).filter(models.Roll.id == roll_id).first()

    
#отредоаактировать запись в дб - добавить дату удаления    
#def remove_roll(db: Session, roll_id: int)
