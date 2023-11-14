import os
import shutil
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Słownik z formatami plików i odpowiadającymi im folderami
picture = "PICTURES"
docs = "DOCUMENTS"

FORMATS_TO_FOLDERS = {
    '.jpg': picture,
    '.jpeg': picture,
    '.png': picture,
    '.gif': picture,
    '.bmp': picture,
    '.pdf': docs,
    '.doc': docs,
    '.docx': docs,
    '.txt': docs,
    '.xls': docs,
    '.xlsx': docs,
    '.ppt': docs,
    '.pptx': docs,
    # Dodaj nowe formaty i foldery tutaj
}


def sort_existing_files(directory):
    # Sprawdź, czy folder istnieje
    if not os.path.exists(directory):
        print(f"Directory  {directory} does not exist.")
        return

    # Sortuj istniejące pliki w folderze
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            sort_and_move_file(file_path)


def sort_and_move_file(file_path):
    # Sprawdź, czy katalogi istnieją, jeśli nie, utwórz je
    for folder in set(FORMATS_TO_FOLDERS.values()):
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Sortuj i przenieś plik
    _, file_extension = os.path.splitext(file_path)
    destination_folder = FORMATS_TO_FOLDERS.get(file_extension.lower(), 'OTHERS')

    destination_path = os.path.join(destination_folder, os.path.basename(file_path))

    try:
        # Sprawdź, czy katalog docelowy istnieje, jeśli nie, utwórz go
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Sprawdź, czy plik o takiej samej nazwie już istnieje w katalogu docelowym
        count = 1
        while os.path.exists(destination_path):
            base_name, extension = os.path.splitext(os.path.basename(file_path))
            new_name = f"{base_name}_{count}{extension}"
            destination_path = os.path.join(destination_folder, new_name)
            count += 1

        shutil.move(file_path, destination_path)

    except FileNotFoundError as e:
        print(f"Ignoring error: {e}")


def setup_observer(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    return observer


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Jeśli modyfikacja dotyczy pliku, a nie folderu
        if event.is_directory:
            return

        # Sortuj i przenieś plik
        sort_and_move_file(event.src_path)


if __name__ == "__main__":
    path = "E:\\TEST_CZY_DZIALA_DO_file_organizer"

    # Sortuj istniejące pliki na początku
    sort_existing_files(path)

    observer = setup_observer(path)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
