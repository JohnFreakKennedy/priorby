import os
import time


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_storage_for_user(user_id: int):
    directory_path = f"storage/{user_id}"
    file_path = os.path.join(directory_path, "redirect.txt")

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")

    if not os.path.exists(file_path):
        open(file_path, 'w').close()
        print(f"Created file: {file_path}")


def read_storage_data(user_id: int):
    directory_path = f"storage/{user_id}"
    file_path = os.path.join(directory_path, "redirect.txt")

    with open(file_path, 'r') as file:
        file_data = file.read()

    return file_data


def write_to_storage_data(user_id: int, text: str):
    directory_path = f"storage/{user_id}"
    file_path = os.path.join(directory_path, "redirect.txt")

    with open(file_path, 'w') as file:
        file_data = file.write(text)
        file.close()

    return file_data


def clear_storage_data(user_id: int):
    try:
        directory_path = f"storage/{user_id}"
        file_path = os.path.join(directory_path, "redirect.txt")

        with open(file_path, 'w') as file:
            file_data = file.write("")
            file.close()
    except Exception as e:
        print(f"file not found")


def generate_user_id():
    return int(time.time())
