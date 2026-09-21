import os
import sys

sys.path.insert(0, r'C:\Users\ontha\Downloads\backend-starter (2)\backend-starter (2)\backend')
os.chdir(r'C:\Users\ontha\Downloads\backend-starter (2)\backend-starter (2)\backend')

from app.database import init_db
from app.main import app

init_db()
print('DB_INIT_OK')
print(app.title)
