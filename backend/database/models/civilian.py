"""Define the Classes for Civilians."""
from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    RelationshipTo
)
from backend.schemas import JsonSerializable
from backend.database.models.types.enums import Ethnicity, Gender


class Civilian(StructuredNode, JsonSerializable):
    age = IntegerProperty()
    age_range = StringProperty()
    ethnicity = StringProperty(choices=Ethnicity.choices())
    gender = StringProperty(choices=Gender.choices())

    # Relationships
    complaints = RelationshipTo(
        "backend.database.models.complaint.Complaint", "COMPLAINED_OF")
    witnessed_complaints = RelationshipTo(
        "backend.database.models.complaint.Complaint", "WITNESSED")
