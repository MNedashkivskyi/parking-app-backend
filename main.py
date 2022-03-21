from os import environ
import uvicorn


if __name__ == "__main__":
    environ['MODE'] = 'PROD'
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8080, log_level="debug", reload=True)