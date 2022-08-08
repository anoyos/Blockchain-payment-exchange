import json

from api_contrib.schemas.base import ResponseStatus


def process(func, raw_message):
    data = json.loads(raw_message)
    try:
        func(data)
    except Exception as e:
        return {"status": ResponseStatus.ERROR, "message": str(e)}

    return {"status": ResponseStatus.SUCCESS, "message": "balance changed"}
