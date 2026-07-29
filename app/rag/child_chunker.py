from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChildChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

    def split(self, documents):

        return self.splitter.split_documents(documents)