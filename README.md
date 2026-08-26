# smb-reindex

Consumer-профиль `document-indexer` для SMB-шары. Файлы зеркалятся в `staging/`, затем индексируются оттуда.

Нативно (VPN до шары должен быть уже поднят):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision
pip install -e .
cp .env.example .env
# заполните SMB_SERVER, SMB_SHARE, SMB_USERNAME, SMB_PASSWORD, SMB_SUBPATH
python main.py
```

Деплой обоих профилей — из `../document_indexer`:

```bash
docker compose up -d --build
docker logs -f smb-reindex
```
