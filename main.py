from fastapi import FastAPI

app = FastAPI() # FastAPI instance

@app.get('/')
async def root():
    return {"message":"Welcome to my APIMon ( > - < )"} # auto convert to JSON

@app.get('/posts')
async def getPosts():
    return {"data": "This is your post ⚔️⚔️⚔️ "}
