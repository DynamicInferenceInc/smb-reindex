FROM document-indexer

WORKDIR /app

COPY main.py ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
