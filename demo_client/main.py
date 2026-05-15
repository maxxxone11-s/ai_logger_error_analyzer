from fastapi import FastAPI
import traceback
import httpx

app = FastAPI()

async def send_error_to_logger(e: Exception, source: str):
    error_payload = {
        "api_key": "LUVtbCzBau-lyDJvgKpgW9clfnHy18xvH-pbzYINE90",
        "message": f"{type(e).__name__}: {str(e)}",
        "level": "error",
        "stack_trace": traceback.format_exc(),
        "source": source
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/errors/",
            json=error_payload
        )
    
    return response

async def handler_exception(e: Exception):
    response = await send_error_to_logger(
        e=e,
        source="demo_client/main.py"
    )

    return {
        "status": "error_sent",
        "logger_status_code": response.status_code,
        "logger_response": response.json()
    }

@app.get("/broken-parser")
async def broken_parser():
    numbers = None
    try:
        for item in numbers:
            print(item)

    except Exception as e:
        response = await handler_exception(e)
        return response
    
@app.get("/broken-value")
async def broken_value():
    value = "abc"
    try:
        number = int(value)
        return {"number": number}
    
    except Exception as e:
        response = await handler_exception(e)
        return response
    
@app.get("/broken-network")
async def broken_network():
    async with httpx.AsyncClient() as client:
        try:
            await client.get("http://127.0.0.1:9999")
        except Exception as e:
            response = await handler_exception(e)
            return response