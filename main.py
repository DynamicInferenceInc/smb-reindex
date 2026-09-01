import os

from document_indexer import DocumentIndexer, ProfileSmb
from document_indexer.examples.resume import (
    FunctionalDirectionEnricher,
    ResumePayloadBuilder,
    ResumeProjectChunker,
    load_resume_prompt,
    load_resume_schema,
    parse_only_enabled,
    run_resume_parse_audit,
)

if __name__ == "__main__":
    print(
        "Startup INDEXER_PROFILE=resume "
        f"RESUME_PARSE_ONLY={os.environ.get('RESUME_PARSE_ONLY')!r} "
        f"parse_only={parse_only_enabled()}",
        flush=True,
    )
    settings = ProfileSmb()
    if parse_only_enabled():
        run_resume_parse_audit(settings)
        raise SystemExit(0)
    extraction_model = settings.models.extraction_model.strip()
    enricher = (
        FunctionalDirectionEnricher(
            load_resume_schema(),
            load_resume_prompt(),
            base_url=settings.models.ollama_base_url,
            model=extraction_model,
            timeout_sec=settings.models.extraction_timeout_sec,
        )
        if extraction_model
        else None
    )
    chunking = settings.chunking
    DocumentIndexer(
        settings,
        payload_builder=ResumePayloadBuilder(),
        enricher=enricher,
        document_chunker=ResumeProjectChunker(
            window_chars=chunking.window_chars,
            window_overlap=chunking.window_overlap,
        ),
    ).run()
