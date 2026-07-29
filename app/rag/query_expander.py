from app.llm.gemini import GeminiLLM


class QueryExpander:

    def __init__(self):

        self.llm = GeminiLLM()

    def expand(self, question: str):

        prompt = f"""
Generate 4 different search queries for the question below.

Only return the queries.

Question:
{question}
"""

        response = self.llm.generate(prompt)

        queries = []

        for line in response.split("\n"):

            line = line.strip()

            if line:

                if line[0].isdigit():

                    line = line.split(".", 1)[1].strip()

                queries.append(line)

        queries.append(question)

        return list(set(queries))