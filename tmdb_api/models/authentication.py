from pydantic import BaseModel


class GuestSessionResponse(BaseModel):
    success: bool
    guest_session_id: str
    expires_at: str
