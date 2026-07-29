class PromptBuilder:

    @staticmethod
    def build(question: str, documents: list):

        context = "\n\n".join(
            doc.page_content
            for doc in documents
        )

        prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, reply:

"I couldn't find that information in the uploaded documents."

-------------------------
Context
-------------------------

{context}

-------------------------
Question
-------------------------

{question}

-------------------------
Answer
-------------------------
"""

        return prompt