from typing import List

from pydantic import BaseModel


class Currencies(BaseModel):
    currencies: List[str]
