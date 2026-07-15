from pydantic import BaseModel, Field
from typing import List, Dict


class CourseRecommendation(BaseModel):
    recommended_courses: List[str] = Field(
        description="List of recommended courses"
    )

    reason: str = Field(
        description="Reason for recommending these courses"
    )

    prerequisites: List[str] = Field(
        description="Prerequisites required before taking the courses"
    )

    learning_sequence: List[str] = Field(
        description="Suggested order of learning"
    )

    confidence: float = Field(
        description="Confidence score between 0 and 1"
    )

    source_metadata: List[Dict] = Field(
        description="Metadata of retrieved source documents"
    )