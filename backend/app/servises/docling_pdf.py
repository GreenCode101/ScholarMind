from docling.document_converter import DocumentConverter
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption

source = "https://arxiv.org/pdf/2408.09869"  # file path or URL


class ArixParse:
    def __init__(self, pdf_path: str):
        self.path = pdf_path
        self.pipeline_options = PdfPipelineOptions()
        self.pipeline_options.do_ocr = False
        self.pipeline_options.do_table_structure = True
        self.pipeline_options.ocr_options.lang = ["eg"]
        self.pipeline_options.generate_page_images = True
        self.pipeline_options.generate_picture_images = True
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=self.pipeline_options)
            }
        )

    def parse(self):
        return self.converter.convert(self.path).document


if __name__ == "__main__":
    doc = ArixParse(pdf_path=source).parse()
    #    print(doc.)
    # converter = DocumentConverter()
    # doc = converter.convert(source).document

    with open("output.md", "w", encoding="utf-8") as f:
        f.write(doc.export_to_markdown())
