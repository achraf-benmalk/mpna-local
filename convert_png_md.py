from docling.document_converter import DocumentConverter

source = "HPL_report_section.pdf"  # Your file name
converter = DocumentConverter()
result = converter.convert(source)

# Save the markdown content
with open("HPL_report.md", "w", encoding="utf-8") as f:
    f.write(result.document.export_to_markdown())

print("Conversion complete! Check HPL_report.md")