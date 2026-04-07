import shutil
import os

path = r'd:\JOVEMPANO\frontend\node_modules\.vite'
if os.path.exists(path):
    print(f'Deleting {path}...')
    shutil.rmtree(path)
    print('Deleted successfully.')
else:
    print(f'{path} does not exist.')
