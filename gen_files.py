import sys
import random
import os
import glob

def count_files_in_directory(directory):
    try:
        file_count = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
        return file_count
    except OSError:
        return 0

def is_executable_by_umask(file_path):
    try:
        st = os.stat(file_path)
        return st.st_mode & 0o111
    except OSError:
        return False

def list_executable_files(directory):
    file_count = {}
    executable_files = []

    for file_path in glob.glob(os.path.join(directory, '**'), recursive=True):
        if os.path.isfile(file_path) and is_executable_by_umask(file_path):
            executable_files.append(file_path)
            permission = format(os.stat(file_path).st_mode & 0o777, '03o')
            file_count[permission] = file_count.get(permission, 0) + 1
    return executable_files, file_count


def get_max_min_permissions(file_count):
    max_files_permission = max(file_count, key=file_count.get, default='None')
    min_files_permission = min(file_count, key=file_count.get, default='None')
    return max_files_permission, min_files_permission


def generate_permission_files(directory, num_files=None):
    if not os.path.exists(directory):
        os.makedirs(directory)

    permission_mapping = {
        '0': '---',
        '1': '--x',
        '2': '-w-',
        '3': '-wx',
        '4': 'r--',
        '5': 'r-x',
        '6': 'rw-',
        '7': 'rwx'
    }

    if num_files is None:
        for i in range(512):
            permission_octal = format(i, '03o')
            file_name = ''.join(permission_mapping[char] for char in permission_octal) + '.txt'
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'w') as file:
                file.write(f"Permission: {permission_octal}")
            os.chmod(file_path, i)
    else:
        for i in range(num_files):
            permission_octal = format(random.randint(0, 511), '03o')
            file_name = f'{i:04d}' + ''.join(permission_mapping[char] for char in permission_octal) + '.txt'
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'w') as file:
                file.write(f"Permission: {permission_octal}")
            os.chmod(file_path, int(permission_octal, 8))

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        directory = sys.argv[1]
        num_files = None
        if len(sys.argv) == 4 and sys.argv[2] == '-r':
            try:
                num_files = int(sys.argv[3])
            except ValueError:
                print("Please provide a valid number for the '-r' option.")
                sys.exit(1)
        generate_permission_files(directory, num_files)
        file_count_in_directory = count_files_in_directory(directory)
        print(f"Files generated in {directory}")
        print(f"Number of files in {directory}: {file_count_in_directory}")

    else:
        print("Usage: python gen_files.py <directory> [-r <number_of_files>]")

directory = 'test2'
executable_files, file_count = list_executable_files(directory)
max_files_permission, min_files_permission = get_max_min_permissions(file_count)

print("Executable files:")
for file in executable_files:
   print(file)

print(f"\nMaximum files permission: {max_files_permission} with {file_count.get(max_files_permission, 0)} files")
print(f"Minimum files permission: {min_files_permission} with {file_count.get(min_files_permission, 0)} files")