from fastapi import FastAPI 
from fastapi.responses import JSONResponse
import logging
from app.manager import Manager



manager = Manager()

async def lifespan(app: FastAPI):
    logging.info("Starting lifespan")
    try:
        manager.run()
        logging.info("Data processed successfully")
    except Exception as e:
        logging.error(f"Error during lifespan: {e}")
    
    yield
    logging.info("Ending lifespan")

app = FastAPI(lifespan=lifespan)


@app.get("/antisemitic-1-weapons")
def get_antisemitic_with_weapons():
    """
    Endpoint to retrieve antisemitic with at least 1 weapons from the elastic.
    Returns the data or an error message if the retrieval fails.
    """
    try:
        if manager.status:
            data = manager.search_by_weapons(1)
            logging.info("Data received successfully")
            return JSONResponse(content=data)
        else:
            logging.warning("Data processing not completed")
            return JSONResponse(content={"Errore": "Data processing not completed"})
    except Exception as e:
        logging.error(f"Error while retrieving antisemitic data: {e}")
        return JSONResponse(content={"Error": str(e)})
    
@app.get("/antisemitic-2-weapons")
def get_antisemitic_with_2():
    """
    Endpoint to retrieve antisemitic with at least 2 weapons from the elastic.
    Returns the data or an error message if the retrieval fails.
    """
    try:
        if manager.status:
            data = manager.search_by_weapons(2)
            logging.info("Data received successfully")
            return JSONResponse(content=data)
        else:
            logging.warning("Data processing not completed")
            return JSONResponse(content={"Errore": "Data processing not completed"})
    except Exception as e:
        logging.error(f"Error while retrieving non-antisemitic data: {e}")
        return JSONResponse(content={"Error": str(e)})
