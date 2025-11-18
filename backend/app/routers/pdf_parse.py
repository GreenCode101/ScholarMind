from servises.docling_pdf import ArixParse

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/parse", tags=["Paper_Parsing"])


@router.get(
    "/pdf",
    status_code=status.HTTP_200_OK,
    tags=["Paper_Parsing"],
    summary="parse pdf",
    description="""
              
                """,
)
async def parse(pdf: str):
    doc = ArixParse(pdf_path=pdf)
    doc.parse()
