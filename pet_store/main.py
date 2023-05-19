from fastapi import FastAPI, status
from pet_store.api.router import api_router

app = FastAPI(title='Pet Store')


@app.get('/healthcheck', status_code=status.HTTP_204_NO_CONTENT)
def healthcheck():
    return


app.include_router(api_router)
