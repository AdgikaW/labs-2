import socket
import time
import os

PORT = 9999

# Создаем сетевой потоковый сокет (IPv4, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Строка управления повторным использованием закомментирована по условию эксперимента
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(f"[СЕРВЕР] Инициализация. Мой PID: {os.getpid()}")
server_socket.bind(('127.0.0.1', PORT))
server_socket.listen(1)
print(f"[СЕРВЕР] Сокет переведен в режим listen. Порт {PORT} зарезервирован в ядре.")

print("[СЕРВЕР] Вызов accept(). Поток сейчас уйдет в глубокий сон...")
client_socket, client_address = server_socket.accept()
print(f"[СЕРВЕР] Поток разбужен! Зафиксировано подключение от {client_address}")

print("[СЕРВЕР] Ожидание данных от клиента (вызов recv)...")
data = client_socket.recv(1024)
print(f"[СЕРВЕР] Данные получены из RX-буфера ядра: {data.decode('utf-8')}")

print("[СЕРВЕР] Закрываем соединение и освобождаем дескрипторы.")
client_socket.close()
server_socket.close()
