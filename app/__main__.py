import uvicorn

if __name__ == "__main__":
    # "app:app" means: inside package 'app', look for variable 'app'
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)