# smb-reindex

Resume-профиль `document-indexer` для SMB-шары. Файлы зеркалятся в staging,
затем индексируются в коллекцию `docs-cv` с `project_experiences`.

Разница с `local-reindex` только в источнике: `ProfileSmb` вместо
`ProfileLocal`. Схема, builder и LLM те же.

VPN индексатор не поднимает: TCP/445 до шары должен быть уже доступен.

## Зависимости

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

Коллекция `docs-cv`, версия `resume-v11`. Смена схемы — bump
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
python main.py
```

Первый цикл синхронизирует шару в staging и делает полный `index`. Дальше —
polling и инкрементальные `index(..., changes)`.

Логи: `tail -f indexer.log`, если процесс запущен с `tee`, либо stdout `python main.py`.

## Docker

Образ собирается поверх `document-indexer`. Из контейнера Qdrant/Ollama обычно
доступны как `http://host.docker.internal:6333` и `:11434`.

`SOURCE__STAGING_PATH` в `.env` должен совпадать с томом staging в compose.

```bash
cp .env.example .env
# заполните учётные данные SMB
docker compose up -d --build smb-reindex
docker compose logs -f smb-reindex
```
