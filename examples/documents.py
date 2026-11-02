"""
A campaign's documents
"""
from modeltestsdk import Client

with Client() as client:
    campaign = client.campaign.get_by_name("Bream FPSO").scalar()
    for doc in campaign.documents():
        print(doc.document_class, doc.name, f"{doc.size_bytes / 1e6:.1f} MB")
    report = next(d for d in campaign.documents() if d.document_class == "Main report")
    path = campaign.download_document(report.path, ".")  # saved under its own name
