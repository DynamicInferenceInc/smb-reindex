from document_indexer import DocumentIndexer, ProfileSmb
from document_indexer.examples.resume import (
    FunctionalDirectionEnricher,
    ResumePayloadBuilder,
    ResumeProjectChunker,
    load_resume_prompt,
    load_resume_schema,
)

if __name__ == "__main__":
    settings = ProfileSmb()
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
