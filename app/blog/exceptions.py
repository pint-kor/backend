from fastapi import HTTPException

NOT_WRITER_ERROR = HTTPException(status_code=403, detail="You are not the writer of this post")