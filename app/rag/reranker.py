class ReRanker:

    def rerank(self, question, documents):

        ranked = sorted(
            documents,
            key=lambda item: len(item[0].page_content),
            reverse=True
        )

        return ranked