from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from app.config import AZURE_SEARCH_CONFIG, AZURE_OPENAI_CONFIG
from openai import AzureOpenAI
import PyPDF2
import io

search_client = SearchClient(
    endpoint=AZURE_SEARCH_CONFIG["endpoint"],
    index_name=AZURE_SEARCH_CONFIG["index_name"],
    credential=AzureKeyCredential(AZURE_SEARCH_CONFIG["api_key"])
)

openai_client = AzureOpenAI(
    api_key=AZURE_OPENAI_CONFIG["api_key"],
    api_version=AZURE_OPENAI_CONFIG["api_version"],
    azure_endpoint=AZURE_OPENAI_CONFIG["endpoint"]
)


class RAGPipeline:
    async def index_document(self, content: bytes, filename: str):
        """Index a document into Azure Cognitive Search"""
        # VULNERABILITY: No file type validation
        text = ""
        if filename.endswith('.pdf'):
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            for page in reader.pages:
                text += page.extract_text()
        else:
            # VULNERABILITY: Assuming UTF-8, no error handling
            text = content.decode('utf-8')

        # Generate embeddings
        embedding_response = openai_client.embeddings.create(
            input=text[:8000],  # Truncate for token limit
            model="text-embedding-ada-002"
        )

        document = {
            "id": filename.replace('.', '_'),
            "content": text,
            "embedding": embedding_response.data[0].embedding,
            "filename": filename
        }

        # VULNERABILITY: No sanitization of document content
        result = search_client.upload_documents(documents=[document])
        return {"id": document["id"], "status": "indexed"}

    async def search(self, query: str, top_k: int = 5):
        """Search for relevant documents"""
        # Generate query embedding
        embedding_response = openai_client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )

        results = search_client.search(
            search_text=query,
            top=top_k,
            select=["content", "filename"]
        )

        return [{"content": r["content"], "filename": r["filename"]} for r in results]
