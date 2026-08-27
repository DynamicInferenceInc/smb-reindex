from document_indexer import DocumentIndexer, JsonSchemaEnricher, ProfileSmb
from document_indexer.examples.resume import (
    ResumePayloadBuilder,
    load_resume_prompt,
    load_resume_schema,
)

if __name__ == "__main__":
    settings = ProfileSmb()
    extraction_model = settings.models.extraction_model.strip()
    enricher = (
        JsonSchemaEnricher(
            load_resume_schema(),
            load_resume_prompt(),
            base_url=settings.models.ollama_base_url,
            model=extraction_model,
            timeout_sec=settings.models.extraction_timeout_sec,
        )
        if extraction_model
        else None
    )
    DocumentIndexer(
        settings,
        payload_builder=ResumePayloadBuilder(),
        enricher=enricher,
    ).run()
