import threading
from icecream import ic
from fastapi import FastAPI, HTTPException, Query
import uvicorn
from pymongo import MongoClient, ReturnDocument
from datetime import datetime
import pytz
import time
from rss import myntra
from ext import ext_myntra
from concurrent.futures import ThreadPoolExecutor, as_completed


app = FastAPI()
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["api_myntra"]
collection_api_keys = db["api_keys"]



def get_ist_timestamp():
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist)
    iso_time = now_ist.isoformat(timespec='milliseconds') + "Z"
    return iso_time


def check_key(key: str) -> bool:
    return collection_api_keys.count_documents({"apikey": key}, limit=1) > 0


def check_credit(key: str, endpoint: str) -> bool:
    user = collection_api_keys.find_one({"apikey": key})
    if not user:
        return True
    data = user.get(endpoint, {})
    total = data.get("total", 0)
    used = data.get("used", 0)
    return used < total

def deduct_credits(apikey: str, endpoint: str, credit: int = 1):
    result = collection_api_keys.find_one_and_update(
        {
            "apikey": apikey,
            "$expr": {
                "$lte": [
                    { "$add": [ f"${endpoint}.used", credit ] },  # field reference
                    f"${endpoint}.total"
                ]
            }
        },
        {
            "$inc": { f"{endpoint}.used": credit }
        },
        return_document=ReturnDocument.AFTER
    )
    if not result:
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests — not enough {endpoint} credits left"
        )


@app.get("/myntra")
def myntra_endpoint(
        keyword: str = Query(''),
        similar: bool = Query(False),
        review: bool = Query(False),
        variants: bool = Query(False),
        apikey: str = Query('')
    ):
    start_time = time.time()
    if not check_key(apikey):
        raise HTTPException(status_code=401, detail="Invalid API key")
    elif not check_credit(apikey, 'flipkart'):
        raise HTTPException(status_code=402, detail="No credits left for Flipkart")
    elif not keyword:
        raise HTTPException(status_code=400, detail="Missing required parameter: keyword")

    response = {}
    result = {}

    def task_pl():
        response = myntra.get_pl_response(keyword)
        return ext_myntra.get_data_pl(response)

    def task_pdp(url):
        response = myntra.get_pdp_response(url)
        return 'pdp', ext_myntra.get_data_pdp(response, url)

    def task_similar(url):
        response = myntra.get_similar_response(url)
        return 'similar', ext_myntra.get_data_similar(response)

    tasks = []
    threads = []
    lock = threading.Lock()  # To safely update shared data from threads

    def process_url(url):
        pdp_data = task_pdp(url)[1]
        # similar_data = task_similar(url)[1]
        # ic(pdp_data)
        data_dict = {}
        data_dict.update(pdp_data)
        # data_dict.update(similar_data)

        # Safely append to shared list
        if 'HTTP Status Code' not in data_dict:
            with lock:
                tasks.append(data_dict)

    # Start threads
    pl_links = task_pl()
    for url in pl_links:
        thread = threading.Thread(target=process_url, args=(url,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    credits_to_deduct = len(pl_links) + 1

    deduct_credits(apikey, "myntra", credits_to_deduct)
    end_time = time.time()
    request_log = {
        'time_stamp' : get_ist_timestamp(),
        'endpoint' : '/myntra',
        'response_time_in_sec' : round(end_time - start_time, 3),
        'input' : keyword,
        'request_cost' : credits_to_deduct,
    }

    response['request_log'] = request_log
    response['results'] = tasks

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="51.91.80.95", port=8989, reload=True)

