# smb-reindex

Resume-профиль `document-indexer` для SMB-шары. Файлы зеркалятся в staging,
затем индексируются в коллекцию `docs-cv` с `project_experiences`.

Разница с `local-reindex` только в источнике: `ProfileSmb` вместо
`ProfileLocal`. Схема, builder и LLM те же.

## Docker

Из корня `core-reindex`:

```bash
cp smb-reindex/.env.example smb-reindex/.env
# Заполните SOURCE__SERVER, SOURCE__SHARE, SOURCE__USERNAME,
# SOURCE__PASSWORD, SOURCE__SUBPATH.
ollama pull nomic-embed-text
ollama pull qwen3:8b
docker compose --profile smb up -d --build smb-reindex
docker compose logs -f smb-reindex
```

`SOURCE__STAGING_PATH` должен совпадать с `SMB_STAGING_CONTAINER` в корневом
`.env`. Зеркало на хосте — `SMB_STAGING_HOST`.

VPN индексатор не поднимает: TCP/445 до шары должен быть доступен из
контейнера.

Коллекция `docs-cv`, версия `resume-v6`. Смена схемы — bump
`QDRANT__INDEX_VERSION` или новая коллекция.

`MODELS__EXTRACTION_MODEL` — text LLM (`qwen3:8b`), не VLM. Пустая строка =
индекс без извлечения полей.

## Нативный запуск

В `.env` для хоста:

```dotenv
SOURCE__STAGING_PATH=staging
QDRANT__URL=http://127.0.0.1:6333
MODELS__OLLAMA_BASE_URL=http://127.0.0.1:11434
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
