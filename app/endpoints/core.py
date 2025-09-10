async def root():
    return {"message": "Welcome to Simple AI Question API"}


async def health():
    return {"status": "healthy"}
