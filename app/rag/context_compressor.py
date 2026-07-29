from app.llm.gemini import GeminiLLM


class ContextCompressor:

    def __init__(self):

        self.llm = GeminiLLM()

    def compress(self, question, documents):

        compressed_documents = []

        for doc, score in documents:

            prompt = f"""
You are a context compressor.

Question:
{question}

Document:
{doc.page_content}

Return ONLY the sentences relevant to answering the question.

If nothing is relevant return:

NONE
"""

            result = self.llm.generate(prompt).strip()

            if result.upper() != "NONE":

                doc.page_content = result

                compressed_documents.append((doc, score))

        return compressed_documents