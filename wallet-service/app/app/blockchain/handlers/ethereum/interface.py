from abc import abstractmethod
from typing import Any, Optional, Dict


class AbstractTransactionFilter:
    @abstractmethod
    def apply(self, block_data: Any, transaction: Any) -> Optional[Dict]:
        pass


class DummyTransactionFilter(AbstractTransactionFilter):
    def apply(self, block_data: Any, transaction: Any) -> Optional[Dict]:
        return None
