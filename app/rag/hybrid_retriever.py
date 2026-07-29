class HybridRetriever:

    def merge(
        self,
        semantic_results,
        keyword_results,
        top_k=3
    ):

        merged = {}

        # Semantic Search Weight
        for doc, score in semantic_results:

            key = doc.page_content

            merged[key] = {
                "doc": doc,
                "score": score * 0.7
            }

        # Keyword Search Weight
        for doc, score in keyword_results:

            key = doc.page_content

            keyword_score = score * 0.3

            if key in merged:
                merged[key]["score"] += keyword_score
            else:
                merged[key] = {
                    "doc": doc,
                    "score": keyword_score
                }

        ranked = sorted(
            merged.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        return [
            (item["doc"], item["score"])
            for item in ranked[:top_k]
        ]