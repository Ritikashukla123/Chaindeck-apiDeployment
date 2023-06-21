from supertokens_python.recipe.jwt import asyncio,syncio
from supertokens_python.recipe.jwt.syncio import create_jwt
from supertokens_python.recipe.jwt.interfaces import CreateJwtOkResult

# async def create_jwt():
#     jwtResponse = await asyncio.create_jwt({
#             "source": "prometheus-fast-api",
#             # ... extra payload
#      })
async def create_jwt():
    jwtResponse = await asyncio.create_jwt({    
    "source": "prometheus-fast-api"

    })  
    if isinstance(jwtResponse, CreateJwtOkResult):
        _ = jwtResponse.jwt
        print(jwtResponse.jwt) 
        # Send JWT as Authorization header to M2
    else:
        raise Exception("Unable to create JWT. Should never come here.")

    return _  