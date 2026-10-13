import socket
import time
import os

PORT = 9995

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', PORT))
server_socket.listen(1)

# КЛЮЧЕВОЙ ВЫЗОВ: Переводим структуру сокета в ядре ОС в неблокирующий режим
server_socket.setblocking(False)

print(f"[НЕНЕБЛОКИРУЮЩИЙ СЕРВЕР] Инициализирован. PID: {os.getpid()}")
print("[СЕРВЕР] Начинаем безумный цикл опроса (Polling) в Ring 3...")

client_socket = None

# Нам приходится крутить цикл, так как accept() больше не усыпляет поток
while True:
    try:
        # В неблокирующем режиме accept() либо мгновенно возвращает клиента,
        # либо мгновенно выбрасывает аппаратное исключение ОС
        client_socket, client_address = server_socket.accept()
        print(f"\n[СЕРВЕР] Ура! Подключение перехвачено: {client_address}")
        break
    except BlockingIOError as e:
        # Это не ошибка поломки программы. Это ядро сообщает: "Очередь пуста, данных нет"
        # Код этой ошибки на низком уровне: EWOULDBLOCK или EAGAIN
        print(".", end="", flush=True)  # Рисуем точки, показывая скорость итераций цикла
       # Микропауза убрана

# Переводим полученный сокет клиента тоже в неблокирующий режим
client_socket.setblocking(False)

print("[СЕРВЕР] Переходим к неблокирующему чтению данных...")
while True:
    try:
        data = client_socket.recv(1024)
        if data:
            print(f"\n[СЕРВЕР] Байты считаны из RX-буфера: {data.decode('utf-8')}")
            break
    except BlockingIOError:
        # Данные от клиента еще летят по кабелю, буфер пуст
        print("*", end="", flush=True)
        time.sleep(0.01)

client_socket.close()
server_socket.close()
print("\n[СЕРВЕР] Работа завершена.")
