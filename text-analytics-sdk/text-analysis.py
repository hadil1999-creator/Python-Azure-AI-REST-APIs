from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    try:
        # Load Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Create Text Analytics client
        credential = AzureKeyCredential(cog_key)
        cog_client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)

        # Read all text files from the reviews folder
        reviews_folder = 'reviews'
        documents = []

        for file_name in os.listdir(reviews_folder):
            file_path = os.path.join(reviews_folder, file_name)
            with open(file_path, encoding='utf8') as f:
                text = f.read()
                documents.append({"id": file_name, "text": text})  # Each file is a document

        if not documents:
            print("No documents found in the reviews folder.")
            exit()

        # Batch API Calls
        print("\nProcessing batch request...\n")

        # Language Detection
        language_results = cog_client.detect_language(documents=documents)
        for doc, result in zip(documents, language_results):
            print(f"\nFile: {doc['id']}\nLanguage: {result.primary_language.name}")

        # Sentiment Analysis
        sentiment_results = cog_client.analyze_sentiment(documents=documents)
        for doc, result in zip(documents, sentiment_results):
            print(f"\nFile: {doc['id']}\nSentiment: {result.sentiment}")

        # Key Phrase Extraction
        key_phrase_results = cog_client.extract_key_phrases(documents=documents)
        for doc, result in zip(documents, key_phrase_results):
            if result.key_phrases:
                print(f"\nFile: {doc['id']}\nKey Phrases: {', '.join(result.key_phrases)}")

        # Named Entity Recognition
        entity_results = cog_client.recognize_entities(documents=documents)
        for doc, result in zip(documents, entity_results):
            if result.entities:
                print(f"\nFile: {doc['id']}\nEntities:")
                for entity in result.entities:
                    print(f"\t{entity.text} ({entity.category})")

        # Linked Entity Recognition
        linked_entity_results = cog_client.recognize_linked_entities(documents=documents)
        for doc, result in zip(documents, linked_entity_results):
            if result.entities:
                print(f"\nFile: {doc['id']}\nLinked Entities:")
                for entity in result.entities:
                    print(f"\t{entity.name} ({entity.url})")

    except Exception as ex:
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
