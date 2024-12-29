from fastapi import APIRouter, Depends, HTTPException
from app.schemas.geocode import GeocodeResponse
from app.services.token_manager import TokenManager, get_token_manager
import httpx
import os
import re

router = APIRouter(
    tags=["geocode"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/geocode/get_address", response_model=GeocodeResponse)
async def get_address(postalCode: int, unitNumber: str = None, token_manager: TokenManager = Depends(get_token_manager)):
    url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={postalCode}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
    
    try:
        if not token_manager.is_token_valid():
            await get_token(token_manager)
    
        headers = {
            "Authorization": f"Bearer {token_manager.token}"
        }

        pattern = r'^\d{6}$'
        if not re.match(pattern, str(postalCode)):
            raise HTTPException(status_code=400, detail="Invalid postal code format. Please provide exactly 6 digits.")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Request failed with the external API.")

        # Parse the response
        data = response.json()
        results = data.get("results", [])
        if not results:
            raise HTTPException(status_code=404, detail="Address not found for the provided postal code.")

        # Construct the geocode data
        result = results[0]  # Use the first result
        geocode_data = {
            "fullAddress": f"{result.get('BLK_NO', '')} {result.get('ROAD_NAME', '')}"
                           f"{', ' + str(unitNumber) if unitNumber else ''}, SINGAPORE {postalCode}",
            "streetAddress": result.get("ROAD_NAME", ""),
            "postalCode": postalCode,
            "unitNumber": unitNumber if unitNumber else "",
        }

        return geocode_data

    except HTTPException as e:
        raise e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")



async def get_token(token_manager: TokenManager):
    url = "https://www.onemap.gov.sg/api/auth/post/getToken"
                
    payload = {
                "email": os.environ['ONEMAP_EMAIL'],
                "password": os.environ['ONEMAP_PASSWORD']
                }
                
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                access_token = data.get("access_token")
                expiry_timestamp = data.get("expiry_timestamp")

                token_manager.update_token(access_token, expiry_timestamp)
                print("get_token is successful")
                return 
            else:
                raise HTTPException(status_code=401, detail="Failed to fetch token")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")



