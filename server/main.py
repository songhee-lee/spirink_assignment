from fastapi import FastAPI
import uvicorn

from router import chat

app = FastAPI(
    title="Chatbot",
    debug=True
)

app.include_router(chat.router, prefix="/api")

if __name__ == "__main__":
    # uvicorn을 통해 FastAPI 애플리케이션 실행
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)