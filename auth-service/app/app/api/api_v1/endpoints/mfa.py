from fastapi import APIRouter
from starlette.responses import FileResponse
from app import schemas
router = APIRouter()


@router.post("/qr.png")
def qr_endpoint():
    """
    Returns a image array from the QR
    """
    return FileResponse('qr.png', media_type="image/png")


@router.post("/txt.png")
def txt_endpoint():
    """
    Returns a txt array from the QR
    """
    return FileResponse('txt.png', media_type="image/png")


@router.post("/activate/")
def txt_endpoint(payload: schemas.ActivateMfaRequest):
    """
    Returns a txt array from the QR
    """
    return FileResponse('txt.png', media_type="image/png")
