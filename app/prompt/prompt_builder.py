class PromptBuilder:

    @staticmethod
    def build(question: str, documents: list, history=None):

        context = "\n\n".join(
            doc.page_content
            for doc, _ in documents
        )

        history_text = ""

        if history:

            history_text = "\n".join(
                f"{role}: {message}"
                for role, message in history
            )

        prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, reply:

"I couldn't find that information in the uploaded documents."

--------------------------------
Conversation History
--------------------------------

{history_text}

--------------------------------
Context
--------------------------------

{context}

--------------------------------
Question
--------------------------------

{question}

--------------------------------
Answer
--------------------------------
"""

        return prompt