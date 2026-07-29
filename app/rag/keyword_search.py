from langchain_core.documents import Document


class KeywordSearch:

    def search(self, query: str, documents: list[Document]):

        query_words = set(query.lower().split())

        results = []

        for doc in documents:

            content_words = set(doc.page_content.lower().split())

            score = len(query_words.intersection(content_words))

            if score > 0:
                results.append((doc, score))

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return results