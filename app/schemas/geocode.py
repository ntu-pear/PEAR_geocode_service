from pydantic import BaseModel

class GeocodeResponse(BaseModel):
    fullAddress: str
    streetAddress: str
    postalCode: int
    unitNumber: str = None
