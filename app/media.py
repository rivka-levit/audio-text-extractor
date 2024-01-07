from pathlib import Path

root_dir = Path('/vol/web/media')

for path in root_dir.glob('*'):
    with open(path, 'wb') as file:
        file.write(b'')
    path.unlink()
