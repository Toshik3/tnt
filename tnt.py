import os
import sys
import shutil
import pathlib
import zipfile


def normalize(filename):
    translit = str.maketrans(
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюя', 'abvgdeejzijklmnoprstufhzcss_y_eua')
    filename = filename.translate(translit)
    allowed_chars = set(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    filename = ''.join(c if c in allowed_chars else '_' for c in filename)
    return filename


def process_folder(source_folder, destination_folder):
    allowed_image_extensions = ('.JPEG', '.PNG', '.JPG', '.SVG')
    allowed_video_extensions = ('.AVI', '.MP4', '.MOV', '.MKV')
    allowed_doc_extensions = ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX')
    allowed_audio_extensions = ('.MP3', '.OGG', '.WAV', '.AMR')
    allowed_archive_extensions = ('.ZIP', '.GZ', '.TAR')
    ignored_folders = ["archives", "video", "audio", "documents", "images"]

    for root, dirs, files in os.walk(source_folder):
        for ignored_folder in ignored_folders:
            if ignored_folder in dirs:
                dirs.remove(ignored_folder)

        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1]

            if file_extension != "":
                if file_extension.upper() in allowed_image_extensions:
                    subdir = 'images'
                elif file_extension.upper() in allowed_video_extensions:
                    subdir = 'video'
                elif file_extension.upper() in allowed_doc_extensions:
                    subdir = 'documents'
                elif file_extension.upper() in allowed_audio_extensions:
                    subdir = 'audio'
                elif file_extension.upper() in allowed_archive_extensions:
                    subdir = 'archives'
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(os.path.join(
                            destination_folder, subdir, normalize(file)))
                    continue
                else:
                    subdir = 'others'

                shutil.move(file_path, os.path.join(
                    destination_folder, subdir))


if len(sys.argv) != 2:
    print('Usage: python sort.py <directory_path>')
    sys.exit(1)

folder_path = sys.argv[1]

if not os.path.isdir(folder_path):
    print('Invalid directory path.')
    sys.exit(1)

destination_folder = os.path.join(folder_path, 'sorted')
os.makedirs(destination_folder, exist_ok=True)
process_folder(folder_path, destination_folder)

