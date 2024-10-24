"""
This module initializes the jockey_amazon package. It imports the necessary classes,
forms, and mappers for managing jockey operations within the Amazon region.

Classes:
    JockeyAmazonRepository: Repository for jockey operations in the Amazon region.
    AbstractJockeyAmazonRepository: Abstract repository defining jockey operations interface.

Forms:
    JockeyAmazonCreateForm: Form for creating a new jockey profile.
    JockeyAmazonEditForm: Form for editing an existing jockey profile.
    JockeyAmazonSearchForm: Form for searching jockey records.
    JockeyAmazonAddDocumentsForm: Form for adding documentation to jockey profiles.
    JockeyAmazonDocumentSearchForm: Form for searching jockey documents.
    
Information Forms:
    GeneralInformationForm: Form for managing basic jockey information.
    HealthInformationForm: Form for managing jockey health records.
    SchoolInformationForm: Form for managing jockey educational background.
    FamilyInformationForm: Form for managing jockey family information.
    WorkAssignmentForm: Form for managing jockey work assignments.

Mappers:
    JockeyAmazonMapper: Data mapper for jockey Amazon entities.
"""

from .repositories import JockeyAmazonRepository, AbstractJockeyAmazonRepository
from .forms import (
    JockeyAmazonCreateForm,
    JockeyAmazonEditForm,
    JockeyAmazonSearchForm,
    JockeyAmazonAddDocumentsForm,
    JockeyAmazonDocumentSearchForm,
    GeneralInformationForm,
    HealthInformationForm,
    SchoolInformationForm,
    FamilyInformationForm,
    WorkAssignmentForm,
)
from .mappers import JockeyAmazonMapper
from .data import *

__all__ = [
    "AbstractJockeyAmazonRepository",
    "JockeyAmazonRepository",
    "JockeyAmazonCreateForm",
    "JockeyAmazonEditForm",
    "JockeyAmazonAddDocumentsForm",
    "JockeyAmazonDocumentSearchForm",
    "JockeyAmazonSearchForm",
    "JockeyAmazonMapper",
    "GeneralInformationForm",
    "HealthInformationForm",
    "SchoolInformationForm",
    "FamilyInformationForm",
    "WorkAssignmentForm",
]
