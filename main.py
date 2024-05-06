import time
import queue 
import threading
from weather_api import fetch_weather
from database import save_to_database,export_data

LATITUDE = 55.7035  # Широта Сколтеха
LONGITUDE = 37.5849  # Долгота Сколтеха
DB_URL = "sqlite:///weather.db"  # URL для SQLite базы данных
EXCEL_FILE_PATH = "weather_data.xlsx"  # Путь для файла .xlsx


def fetch_weather_data(queue):
    while True:
        #Запрос по api к серверу openmeteo
        weather_data = fetch_weather(LATITUDE, LONGITUDE)
        if weather_data:
            #Записываем в очередь данные полученные по api и команду 
            queue.put(["INPUT",weather_data])
            time.sleep(900)  # Пауза на 15 минут
            
#Просто процесс который висит в консоли для подачи в очередь команды об экспорте
def writer(queue):
    while True:
        export = input("Хотите экспортировать данные в файл .xlsx? (да/нет): ")
        if export.lower() == "да":
            #Записываем в очередь название файла и команду для дальнейшего ветвления
            queue.put(["Export",EXCEL_FILE_PATH])
        elif export.lower() == "нет":
            print("Экспорт данных отменен.")
        else:
            print("Некорректный ввод. Пожалуйста, введите 'да' или 'нет'.")
         

#Функция необходима для дальнейшего ветвления распределения по задачам
def tree_of_proces(queue):
    while True:
        #Получаем объект из очереди если он там есть
        if queue.empty():
            continue
        else:
            test = queue.get()
            #Если это объект класса Экспорт, переводим в функцию для экспорта в Excel
        if test[0]=='Export':
            export_data(test[1],DB_URL)
            #Если это объект класса INPUT, переводим в фнкцию для дополнения базы
        elif test[0]=='INPUT':
            save_to_database(test[1],DB_URL)
        else: 
            #Иначе сообщаем об ошибке
            print("Error")
            

def main():
    # Создаём очереди для заполнения командами взаимодействия с базой.
    Queue = queue.Queue()
    # Объявление потоков с необходимыми нам функциями и аргументами для них
    fetch_thread = threading.Thread(target=fetch_weather_data, args=(Queue,))
    db_thread = threading.Thread(target=tree_of_proces, args=(Queue,))
    writer_thread = threading.Thread(target=writer, args=(Queue,))
    # Запуск на 3 потоках 3 процесссов
    fetch_thread.start()
    db_thread.start()
    writer_thread.start()
    # Слежение за этими потоками 
    fetch_thread.join()
    db_thread.join()
    writer_thread.join()

if __name__ == "__main__":
    main()