from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from src.core.module.jockey_amazon.models import JockeyAmazon
from src.core.database import db
from src.core.module.common.repositories import apply_filters

class AbstractJockeyAmazonRepository(ABC):
    @abstractmethod
    def add(self, jockey: JockeyAmazon) -> JockeyAmazon:
        pass

    @abstractmethod
    def get_page(
            self,
            page: int,
            per_page: int,
            max_per_page: int,
            search_query: Dict = None,
            order_by: List = None,
    ):
        pass

    @abstractmethod
    def get_by_id(self, jockey_id: int) -> Optional[JockeyAmazon]:
        pass

    @abstractmethod
    def update(self, jockey_id: int, data: Dict) -> bool:
        pass

    @abstractmethod
    def delete(self, jockey_id: int) -> bool:
        pass

class JockeyAmazonRepository(AbstractJockeyAmazonRepository):
    def __init__(self):
        self.db = db

    def add(self, jockey: JockeyAmazon) -> JockeyAmazon:
        self.db.session.add(jockey)
        self.db.session.flush()
        self.save()
        return jockey

    def get_page(
            self,
            page: int,
            per_page: int,
            max_per_page: int,
            search_query: Dict = None,
            order_by: List = None,
    ):
        query = JockeyAmazon.query

        query = apply_filters(JockeyAmazon, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def get_by_id(self, jockey_id: int) -> Optional[JockeyAmazon]:
        return self.db.session.query(JockeyAmazon).filter(JockeyAmazon.id == jockey_id).first()

    def update(self, jockey_id: int, data: Dict) -> bool:
        jockey = JockeyAmazon.query.filter_by(id=jockey_id)
        if not jockey:
            return False
        jockey.update(data)
        self.save()
        return True

    def delete(self, jockey_id: int) -> bool:
        jockey = JockeyAmazon.query.filter_by(id=jockey_id)
        if not jockey:
            return False
        jockey.delete()
        self.save()
        return True

    def save(self):
        self.db.session.commit()