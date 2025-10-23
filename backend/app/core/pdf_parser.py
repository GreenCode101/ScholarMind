import config
chunk_size = config.CHUNK_SIZE
chunk_overlap = config.CHUNK_OVERLAP
start_page = config.START_PAGE
from colorama import init, Fore

def parse_pdf(pdf_path):
    import PyPDF2
    from tqdm import tqdm
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            #get the number of pages in the PDF
            num_pages = len(pdf_reader.pages)
            pages_text = []
            print(f"Total number of pages:" ,num_pages)
            for pages in tqdm(range(start_page ,num_pages),"Extracting Text"):
                
                page = pdf_reader.pages[pages]
                text = page.extract_text()      
                # print(f"Page {pages + 1}:\n{text}\n")
                pages_text.append(text)
            return pages_text
    except Exception as e:
        return Fore.RED +f"Cannot open: {pdf_path} with error: {(e)}"


def clean_text(pages: list[str]) -> list[str]:
    import regex as re
    RE_FIGURES = re.compile(r"Figure\s?\d+(-\d+)?")
    RE_TABLES = re.compile(r"Table\s?\d+(-\d+)?")
    RE_PAGE_NUMBERS = re.compile(r"Page \d+")
    RE_CITATIONS = re.compile(r"\([A-Za-z ,\n\-]+?,\s?\d{4}\)")
    RE_SUPERSCRIPTS = re.compile(r"[¹²³⁴⁵⁶⁷⁸⁹⁰]+")
    RE_NUMERIC = re.compile(r"\[\d{1,3}\]")
    RE_SPACES = re.compile(r'\s+')

    cleaned_pages = []
    for text in pages:
        text = re.sub(RE_FIGURES, " ", text)
        text = re.sub(RE_PAGE_NUMBERS, " ", text)
        text = re.sub(RE_CITATIONS, " ", text)
        text = re.sub(RE_SUPERSCRIPTS, " ", text)
        text = re.sub(RE_NUMERIC, " ", text)
        text = re.sub(RE_TABLES, " ", text)
        # text = re.sub(RE_SPACES, " ", text)
        cleaned_pages.append(text)
    
    return cleaned_pages

def chunk_text(pages: list[str], chunk_size: int = chunk_size, chunk_overlap: int = chunk_overlap) -> list[str]:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=['\n\n\n','\n\n','\n'])
    chunks = []
    for text in pages:
        chunk = splitter.split_text(text)
        chunks.extend(chunk)
    print("Text Chunks Created:" ,len(chunks), "\n")
    import random
    print(Fore.CYAN + f'Sample Chunck:')
    print(f' """{random.choice(chunks)}""" \n')
    return chunks


def process_pdf_to_chunks(pdf_path: str) -> list[str]:
    """Process PDF through the complete pipeline."""
    # Step 1: Parse PDF
    raw_text = parse_pdf(pdf_path)
    # Step 2: Clean with regex
    cleaned_text = clean_text(raw_text)
    # Step 3: Chunk text
    document_chunks = chunk_text(cleaned_text)  
    return document_chunks