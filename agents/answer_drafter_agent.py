from transformers import pipeline, AutoTokenizer

# Load pipeline and tokenizer
model_name = "google/flan-t5-base"
generator = pipeline("text2text-generation", model=model_name, temperature=0.7)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_answer(context):
    if not isinstance(context, str):
        context = str(context)

    # Prompt for summarization
    prompt_intro = (
        "You are a helpful assistant. Carefully read the research content and write a coherent, non-repetitive summary paragraph. Do not list points; write naturally like a human-written summary.\n\n"
    )

    # Token budget
    max_input_tokens = 512
    reserved_prompt_tokens = tokenizer.encode(prompt_intro, truncation=False)
    available_tokens = max_input_tokens - len(reserved_prompt_tokens)

    # Tokenize and chunk context
    context_tokens = tokenizer.encode(context, truncation=False)
    chunked_summaries = []

    for i in range(0, len(context_tokens), available_tokens):
        chunk = context_tokens[i:i + available_tokens]
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)

        full_prompt = f"{prompt_intro}{chunk_text}"
        result = generator(full_prompt, max_length=200, truncation=True, do_sample=False)

        if result and 'generated_text' in result[0]:
            chunked_summaries.append(result[0]['generated_text'].strip())
        else:
            chunked_summaries.append("[Summary not available for this chunk]")

    return " ".join(chunked_summaries).strip()