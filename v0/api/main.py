# fastapi
import ssl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# create app
app = FastAPI()

# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPLICATE_API_TOKEN = "r8_089y8ZSDYbmyeSLS683N98FfNqZWZPb0Ca76A"


import json
import aiohttp
import asyncio
import certifi

sslcontext = ssl.create_default_context(cafile=certifi.where())


async def generate(prompt: str) -> str:
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
    }
    data = {
        "version": "5957069d5c509126a73c7cb68abcddbb985aeefa4d318e7c63ec1352ce6da68c",
        "input": {
            "prompt": prompt,
            "save_mesh": True,
            "batch_size": 1,
            "render_mode": "nerf",
            "render_size": 128,
            "guidance_scale": 15,
        },
    }
    async with aiohttp.ClientSession() as session:
        print("sending request")
        async with session.post(
            url, headers=headers, data=json.dumps(data), ssl=sslcontext
        ) as response:
            response.raise_for_status()
            out = await response.json()
            get = out["urls"]["get"]
            while True:
                print("sending request", get)
                async with session.get(
                    get,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Token {REPLICATE_API_TOKEN}",
                    },
                    ssl=sslcontext,
                ) as status_response:
                    status = await status_response.json()
                    if status["status"] == "canceled" or status["status"] == "failed":
                        return status["status"]
                    if status["status"] == "finished":
                        return status["output"][1]
                await asyncio.sleep(4)


# prompt id
@app.get("/prompt/{prompt}")
async def prompt(prompt: str):
    return await generate(prompt)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# uvicorn main:app --reload
