import textwrap

def chunk_text(text: str, max_tokens: int = 1500) -> list:
    """Splits text into chunks based on length (approx tokens)."""
    return textwrap.wrap(text, width=max_tokens)

def summarize_chunk(chunk: str, model_fn) -> str:
    """Summarize one chunk using the provided model function."""
    summary_prompt = f"Summarize this chat section for tone, maturity, emotional clarity:\n\n{chunk}"
    return model_fn(summary_prompt)

def summarize_large_text(text: str, model_fn, max_tokens=1500) -> str:
    """Splits large input and returns combined summaries."""
    chunks = chunk_text(text, max_tokens=max_tokens)
    summaries = [summarize_chunk(c, model_fn) for c in chunks]
    return "\n".join(summaries)
