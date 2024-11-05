import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class GitHandler(FileSystemEventHandler):
    def __init__(self, repo_path, file_path):
        self.repo_path = repo_path
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            print(f"{self.file_path} изменён, добавление в git...")
            self.commit_changes()

    def commit_changes(self):
        try:
            # Добавление файла в индекс
            subprocess.run(["git", "-C", self.repo_path, "add", self.file_path], check=True)
            # Коммит изменений
            subprocess.run(["git", "-C", self.repo_path, "commit", "-m", f"Автоматический коммит изменений в {self.file_path}"], check=True)
            print(f"Изменения в {self.file_path} закоммичены.")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при коммите: {e}")

    def clear_commit_history(self):
        try:
            # Удаление всей истории коммитов, оставляя только текущий коммит
            subprocess.run(["git", "-C", self.repo_path, "checkout", "--orphan", "latest_branch"], check=True)
            subprocess.run(["git", "-C", self.repo_path, "add", "-A"], check=True)
            subprocess.run(["git", "-C", self.repo_path, "commit", "-m", "Очистка истории коммитов"], check=True)
            subprocess.run(["git", "-C", self.repo_path, "branch", "-D", "master"], check=True)  # Удаление старой ветки
            subprocess.run(["git", "-C", self.repo_path, "branch", "-m", "master"], check=True)  # Переименование ветки
            print("История коммитов очищена.")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при очистке истории: {e}")

def monitor_changes(repo_path, file_path, stop_event):
    event_handler = GitHandler(repo_path, file_path)
    observer = Observer()
    observer.schedule(event_handler, repo_path, recursive=False)
    observer.start()

    print(f"Наблюдение за изменениями в {file_path}...")
    try:
        while not stop_event.is_set():  # Проверяем флаг остановки
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.stop()
    observer.join()

def command_interface(handler, stop_event):
    while True:
        command = input("Введите 'clear' для очистки истории коммитов, 'exit' для выхода: ")
        if command.lower() == 'clear':
            handler.clear_commit_history()
        elif command.lower() == 'exit':
            print("Выход из программы...")
            stop_event.set()  # Устанавливаем флаг остановки
            break

def main():
    repo_path = r"C:\Users\User\Desktop\konf2\my_repo"
    file_path = os.path.join(repo_path, "example.txt")

    # Создаем обработчик GitHandler
    handler = GitHandler(repo_path, file_path)

    # Создаем событие для остановки
    stop_event = threading.Event()

    # Запускаем наблюдение в отдельном потоке
    monitor_thread = threading.Thread(target=monitor_changes, args=(repo_path, file_path, stop_event), daemon=True)
    monitor_thread.start()

    # Запускаем интерфейс командной строки в основном потоке
    command_interface(handler, stop_event)

    # Завершение потока наблюдения
    print("Завершение наблюдения...")
    monitor_thread.join()

if __name__ == "__main__":
    main()
