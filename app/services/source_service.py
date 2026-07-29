class SourceService:

    @staticmethod
    def build(documents):

        sources = []

        seen = set()

        for doc in documents:

            source = doc.metadata.get("source", "Unknown")

            page = doc.metadata.get("page", 0)

            file_name = source.split("\\")[-1]
            file_name = file_name.split("/")[-1]

            key = (file_name, page)

            if key not in seen:

                seen.add(key)

                sources.append({
                    "file_name": file_name,
                    "page": page + 1
                })

        return sources