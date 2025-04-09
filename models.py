from dataclasses import dataclass
from datetime import datetime

from constants import ClassicQuality, WardQuality


@dataclass
class ActivityState:
    true: bool
    pred: bool


@dataclass
class AnnotatedSegment:
    start: datetime
    end: datetime
    annotation: ActivityState


@dataclass
class ClassicQualifiedUnit:
    quality: ClassicQuality
    start: int
    end: int


@dataclass
class WardQualifiedUnit:
    quality: WardQuality
    start: int
    end: int
