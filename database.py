from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.orm import sessionmaker,declarative_base
import pandas as pd

Base = declarative_base()
#Объявляем класс данных с набором необходимых для задачи полей
class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    temperature = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    pressure = Column(Float)
    rain = Column(Float)
    snowfall = Column(Float)
# Инициализируем базу данных
def init_db(db_url):
    #Содаём движок для базы с указанием url
    engine = create_engine(db_url)
    #Формирование таблички
    Base.metadata.create_all(engine)
    #Открываем сессию для дальнейшей работы с базой
    Session = sessionmaker(bind=engine)
    #Возвращаем движок и сессию(Они понадобятся в других сегментах кода)
    return [Session(),engine]
#Селектим данные из базы в количестве 10 штук с помощью инструмента pandas
def read_weather_data(db_engine, limit=10):
    query = f"SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT {limit}"
    df = pd.read_sql(query, db_engine)
    return df
#Считываем при помощи ранее написаной функции данные из базы
def export_data(name,DB_URL):
    db_engine= init_db(DB_URL)[1]
    #Берём движковую часть базы и с её помощью 
    weather_data = read_weather_data(db_engine)
    export_to_excel(weather_data, name)
    #Отправляем в экспорт название файла и считанные данные 
    print("Данные успешно экспортированы.")

def export_to_excel(weather_data_df, file_path):
    weather_data_df.to_excel(file_path, index=False)

#Записываем в базу объект Погоды
def save_to_database(Weather,db_url):
    db_session = init_db(db_url)[0]
    db_session.add(WeatherData(**Weather))
    db_session.commit()