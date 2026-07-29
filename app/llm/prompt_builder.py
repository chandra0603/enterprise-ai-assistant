class PromptBuilder:

    @staticmethod
    def build(question, documents, history):

        history_text = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in history
        )
        
        context = "\n\n".join(
            doc.page_content
            for doc, score in documents
        )

        prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, reply:

"I couldn't find that information in the uploaded documents."

--------------------
Context
--------------------

{context}

--------------------
Question
--------------------

{question}

--------------------
Answer
--------------------
"""

        return prompt