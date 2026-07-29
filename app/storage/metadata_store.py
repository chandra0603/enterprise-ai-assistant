import json
import os
from langchain_core.documents import Document


class MetadataStore:

    def __init__(self):

        self.folder = "metadata"

        self.hash_file = "metadata/file_hashes.json"
        
        os.makedirs(self.folder, exist_ok=True)

        self.parent_file = os.path.join(
            self.folder,
            "parents.json"
        )

        self.child_file = os.path.join(
            self.folder,
            "children.json"
        )

    def save(self,parents,children,file_hashes):

        print("=" * 60)
        print("MetadataStore.save() called")
        print(f"Parents : {len(parents)}")
        print(f"Children: {len(children)}")

        parent_data = []

        for parent_id, doc in parents.items():

            parent_data.append({
                "parent_id": parent_id,
                "page_content": doc.page_content,
                "metadata": doc.metadata
            })

        child_data = []

        for doc in children:

            child_data.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata
            })

        print(f"Writing parent file : {os.path.abspath(self.parent_file)}")
        print(f"Writing child file  : {os.path.abspath(self.child_file)}")

        with open(
            self.parent_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                parent_data,
                f,
                indent=4,
                ensure_ascii=False
            )

        with open(
            self.child_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                child_data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("Metadata saved successfully.")
        print("=" * 60)
        with open(self.hash_file, "w") as file:
            json.dump(file_hashes, file, indent=4)

    def load(self):

        print("=" * 60)
        print("Loading metadata...")

        if not os.path.exists(self.parent_file):

            print("No metadata found.")
            print("=" * 60)
            return {}, []

        with open(
            self.parent_file,
            "r",
            encoding="utf-8"
        ) as f:

            parent_data = json.load(f)

        with open(
            self.child_file,
            "r",
            encoding="utf-8"
        ) as f:

            child_data = json.load(f)

        parents = {}

        for item in parent_data:

            parents[item["parent_id"]] = Document(
                page_content=item["page_content"],
                metadata=item["metadata"]
            )

        children = []

        for item in child_data:

            children.append(
                Document(
                    page_content=item["page_content"],
                    metadata=item["metadata"]
                )
            )

        print(f"Loaded Parents : {len(parents)}")
        print(f"Loaded Children: {len(children)}")
        print("=" * 60)

        file_hashes = {}

        if os.path.exists(self.hash_file):

            with open(self.hash_file, "r") as file:
                file_hashes = json.load(file)

        return parents, children, file_hashes