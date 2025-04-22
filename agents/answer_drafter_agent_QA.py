from transformers import pipeline

# Load QA pipeline
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

def generate_answer(context, user_question=""):
    if not isinstance(context, str):
        context = str(context)
    if not isinstance(user_question, str):
        user_question = str(user_question)

    result = qa_model(question=user_question, context=context)
    return result["answer"]