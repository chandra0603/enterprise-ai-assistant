from langchain_text_splitters import RecursiveCharacterTextSplitter


class ParentChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )

    def split(self, documents):

        return self.splitter.split_documents(documents)