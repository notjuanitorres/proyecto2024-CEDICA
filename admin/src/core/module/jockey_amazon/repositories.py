from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from src.core.module.jockey_amazon.data import DAYS_MAPPING
from src.core.module.jockey_amazon.models import JockeyAmazon, JockeyAmazonFile
from src.core.database import db
from src.core.module.common.repositories import apply_filters


class AbstractJockeyAmazonRepository(ABC):
    def __init__(self):
        self.storage_path = "jockeys_amazons/"

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
    def archive(self, jockey_id: int) -> bool:
        pass

    @abstractmethod
    def recover(self, jockey_id: int) -> bool:
        pass

    @abstractmethod
    def delete(self, jockey_id: int) -> bool:
        pass

    @abstractmethod
    def add_document(self, jockey_id: int, document: JockeyAmazonFile):
        pass

    @abstractmethod
    def get_document(self, horse_id: int, document_id: int) -> Dict:
        pass

    @abstractmethod
    def delete_document(self, jockey_id: int, document_id: int):
        pass

    @abstractmethod
    def get_file_page(
            self,
            jockey_id: int,
            page: int,
            per_page: int,
            max_per_page: int = 10,
            search_query: Dict = None,
            order_by: List = None,
    ):

        pass

    @abstractmethod
    def update_document(self, jockey_id: int, document_id: int, data: Dict) -> bool:
        pass

    @abstractmethod
    def is_dni_used(self, dni: str) -> bool:
        raise NotImplementedError

class JockeyAmazonRepository(AbstractJockeyAmazonRepository):
    def __init__(self):
        super().__init__()
        self.db = db
    
    def __get_by_dni(self, dni: str) -> JockeyAmazon | None:
        return self.db.session.query(JockeyAmazon).filter(JockeyAmazon.dni == dni).first()

    def add(self, jockey: JockeyAmazon) -> JockeyAmazon:
        self.db.session.add(jockey)
        self.db.session.flush()
        self.save()
        return jockey

    def get_page(
            self,
            page: int,
            per_page: int,
            max_per_page: int = 20,
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
    
    def archive(self, jockey_id: int) -> bool:
        jockey = self.get_by_id(jockey_id)
        if not jockey or jockey.is_deleted:
            return False
        jockey.is_deleted = True
        self.save()
        return True
    
    def recover(self, jockey_id: int) -> bool:
        jockey = self.get_by_id(jockey_id)
        if not jockey or not jockey.is_deleted:
            return False
        jockey.is_deleted = False
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

    def add_document(self, jockey_id: int, document: JockeyAmazonFile):
        jockey: JockeyAmazon = self.get_by_id(jockey_id)
        jockey.files.append(document)
        self.save()

    def get_all(self):
        return self.db.session.query(JockeyAmazonFile).all()

    def __get_query_document(self, jockey_id: int, document_id: int):
        query = (
            self.db.session.query(JockeyAmazonFile)
            .filter_by(jockey_amazon_id=jockey_id, id=document_id)
        )
        return query

    def get_document(self, horse_id: int, document_id: int) -> Dict:
        doc = self.__get_query_document(horse_id, document_id).first()
        return doc.to_dict() if doc else doc

    def delete_document(self, jockey_id: int, document_id: int):
        jockey: JockeyAmazon = self.get_by_id(jockey_id)
        document = self.__get_query_document(jockey.id, document_id)
        document.delete()
        self.save()

    def get_file_page(
            self,
            jockey_id: int,
            page: int,
            per_page: int,
            max_per_page: int = 10,
            search_query: Dict = None,
            order_by: List = None,
    ):

        query = JockeyAmazonFile.query

        if search_query.get("filters"):
            search_query["filters"]["jockey_amazon_id"] = jockey_id
        else:
            search_query["filters"] = {"jockey_amazon_id": jockey_id}

        query = apply_filters(JockeyAmazonFile, query, search_query, order_by)

        return query.paginate(
            page=page, per_page=per_page, error_out=False, max_per_page=max_per_page
        )

    def update_document(self, jockey_id: int, document_id: int, data: Dict) -> bool:
        doc_query = self.db.session.query(JockeyAmazonFile).filter_by(jockey_amazon_id=jockey_id, id=document_id)
        if not doc_query:
            return False
        doc_query.update(data)
        self.save()
        return True
    
    def update_school_information(self, jockey_id: int, data: Dict) -> bool:
        jockey = JockeyAmazon.query.get(jockey_id)
        if not jockey:
            return False
        
        school_data = data.get("school_institution", {})
        for key, value in school_data.items():
            if hasattr(jockey.school_institution, key):
                setattr(jockey.school_institution, key, value)
 
        jockey.current_grade_year = data.get('current_grade_year', jockey.current_grade_year)
        jockey.school_observations = data.get('school_observations', jockey.school_observations)

        self.save()


        return True

    def update_assignments(self, jockey_id: int, data: Dict) -> bool:
        jockey = JockeyAmazon.query.get(jockey_id)
        if not jockey:
            return False
        assignment = jockey.work_assignment

        if assignment and data:
            assignment_data = data.get("work_assignments", {})
            for key, value in assignment_data.items():
                setattr(assignment, key, value)

        jockey.has_scholarship = data.get("has_scholarship")
        jockey.scholarship_observations = data.get("scholarship_observations")
        jockey.scholarship_percentage = data.get("scholarship_percentage")
        self.db.session.add(assignment)
        self.db.session.add(jockey)
        days_abbreviations = assignment_data.get("days", [])
        assignment.days = [DAYS_MAPPING[abbr] for abbr in days_abbreviations if abbr in DAYS_MAPPING]
        self.save()
        return True


    def is_dni_used(self, dni: str) -> bool:
        return self.__get_by_dni(dni) is not None

