# smb-reindex

Consumer-профиль `document-indexer` для SMB-шары. Файлы зеркалятся в
staging, затем индексируются оттуда.

Настройки берутся из `.env` в этой папке. Compose подключает его как
`env_file`; `IndexerSettings()` в `main.py` читает переменные процесса.

## Docker

Из корня `core-reindex`:

```bash
cp smb-reindex/.env.example smb-reindex/.env
# Заполните SMB_SERVER, SMB_SHARE, SMB_USERNAME, SMB_PASSWORD, SMB_SUBPATH.
docker compose up -d --build smb-reindex
docker compose logs -f smb-reindex
```

`SMB_STAGING_PATH` в `.env` должен совпадать с `SMB_STAGING_CONTAINER` в
корневом `.env`. Зеркало на хосте — `SMB_STAGING_HOST`.

VPN индексатор не поднимает: TCP/445 до шары должен быть доступен из
контейнера.

## Нативный запуск

Для `python main.py` на хосте поменяйте в `.env`:

```dotenv
SMB_STAGING_PATH=staging
QDRANT_URL=http://127.0.0.1:6333
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision
pip install -e .
cp .env.example .env
python main.py
```
