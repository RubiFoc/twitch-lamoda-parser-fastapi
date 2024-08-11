from fastapi import HTTPException


async def exception_handler(request, exc):
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=400, detail=str(exc))
    elif isinstance(exc, FileNotFoundError):
        raise HTTPException(status_code=404, detail="File not found")

    raise HTTPException(status_code=500, detail="Internal server error")
