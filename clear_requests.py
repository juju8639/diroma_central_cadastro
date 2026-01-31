import sqlite3
import shutil
import os
from datetime import datetime

DB = 'app.db'
if not os.path.exists(DB):
    print('Nenhum arquivo app.db encontrado em cwd:', os.getcwd())
    raise SystemExit(1)

# Backup
bak = f"app.db.bak.{datetime.now().strftime('%Y%m%dT%H%M%S')}"
shutil.copy2(DB, bak)
print('Backup criado:', bak)

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM requests')
before = cur.fetchone()[0]
print('Solicitações antes:', before)
cur.execute('DELETE FROM requests')
conn.commit()
cur.execute('SELECT COUNT(*) FROM requests')
after = cur.fetchone()[0]
print('Solicitações depois:', after)
conn.close()
print('Limpeza concluída.')
