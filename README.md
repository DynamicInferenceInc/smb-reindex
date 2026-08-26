# smb-reindex

Профиль `document-indexer` для SMB-шары. Один процесс = одна коллекция Qdrant.
Файлы зеркалятся в staging, затем индексируются оттуда.

Настройки — вложенные ключи `SOURCE__*`, `QDRANT__*`, `MODELS__*` (как в `document-indexer`).
`ProfileSmb` читает `.env` из рабочей директории.

VPN индексатор не поднимает: TCP/445 до шары должен быть уже доступен.

## Зависимости

Нужны запущенные **Ollama** и **Qdrant**. Если они уже подняты `it-consultant-1c`
(контейнеры `it-consultant-ollama` / `it-consultant-qdrant`), достаточно портов
`11434` и `6333`. Модель эмбеддингов: `nomic-embed-text`. VLM по умолчанию
`qwen3-vl:2b` (влезает в 8 ГБ VRAM).

## Нативный запуск

```bash
cp .env.example .env
# заполните SOURCE__SERVER, SOURCE__SHARE, SOURCE__USERNAME, SOURCE__PASSWORD
```

В `.env` для запуска на хосте:

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
