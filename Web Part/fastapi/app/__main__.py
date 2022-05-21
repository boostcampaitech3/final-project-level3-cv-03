if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8008, reload=True) # reload는 저장될 때 마다 재실행
