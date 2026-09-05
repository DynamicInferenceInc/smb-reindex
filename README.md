# smb-reindex

Resume-профиль `document-indexer` для SMB-шары. Файлы зеркалятся в staging,
затем индексируются в коллекцию `docs-cv`: один проект — одна точка.
Шаблонные резюме разбирает парсер; нешаблонные — LLM (`qwen3.8:27b`):
поиск проектов в неразобранном тексте, дозаполнение пустых полей и
`functional_direction` / `solution_platform` одним вызовом на резюме, а если
проектов нет вообще — чанки `experience` (места работы) и `profile`.
Все значения от LLM проверяются на наличие в тексте резюме. `prose`-окна с
`needs_review=true` остаются только если LLM выключена или упала.
Стратегия задаётся `CHUNKING__STRATEGY=resume_project`.

Разница с `local-reindex` только в источнике: SMB вместо локальной папки.

VPN индексатор не поднимает: TCP/445 до шары должен быть уже доступен.

## Зависимости

```bash
cp smb-reindex/.env.example smb-reindex/.env
# Заполните SOURCE__SERVER, SOURCE__SHARE, SOURCE__USERNAME,
# SOURCE__PASSWORD, SOURCE__SUBPATH.
ollama pull nomic-embed-text
ollama pull qwen3.8:27b-q8_0   # или qwen3.8:27b
docker compose --profile smb up -d --build smb-reindex
docker compose logs -f smb-reindex
```

На NVIDIA DGX Spark (ARM64) образы собираются на самой машине; параметры модели
в `.env.example` уже под неё (`num_ctx=65536`, `num_predict=8192`, таймаут 1800 с).
Для Ollama: `OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KEEP_ALIVE=-1`, `OLLAMA_NUM_PARALLEL=1`.

`SOURCE__STAGING_PATH` должен совпадать с `SMB_STAGING_CONTAINER` в корневом
`.env`. Зеркало на хосте — `SMB_STAGING_HOST`.

VPN индексатор не поднимает: TCP/445 до шары должен быть доступен из
контейнера.

Коллекция `docs-cv`, версия `resume-v20` (переиндексирует все резюме). Смена
схемы — bump `QDRANT__INDEX_VERSION` или новая коллекция.

`MODELS__EXTRACTION_MODEL` — text LLM (`qwen3.8:27b-q8_0`), не VLM. Пустая
строка = только парсер: резюме без проектов уйдут в `prose` с `needs_review`.
Шаги LLM включаются `RESUME__LLM_PROJECTS` / `RESUME__LLM_REFINE` /
`RESUME__LLM_EXPERIENCE`; порог остатка — `RESUME__RESIDUAL_MIN_CHARS`.

Аудит без embed/Qdrant: `RESUME_PARSE_ONLY=1` (парсер) или `RESUME_LLM_AUDIT=1`
(парсер + LLM, плюс `resume_chunks.jsonl` со всеми чанками). После аудита и после
каждого reindex печатается и сохраняется `resume_report.txt/.csv`:
`ФИО | Должность | Проектов | из них LLM | Мест работы | Проверить | Файл` по всем
резюме, итоги и списки файлов без ФИО/должности.

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
