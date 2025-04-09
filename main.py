from datetime import datetime
from itertools import groupby
from operator import itemgetter
from re import findall, sub
from typing import Callable, Iterator, Mapping, Optional, Sequence, TypeAlias

from constants import (
    METRIC_TO_FORMULA,
    QUALIFICATION_RULE_CLASSIC,
    QUALIFICATION_RULE_WARD,
    QUALITY_TO_CLUSTER,
    ClassicMetric,
    ClassicQuality,
    Cluster,
    Formula,
    Metric,
    NcibiMetric,
    WardMetric,
    WardQuality,
)
from models import (
    ActivityState,
    AnnotatedSegment,
    ClassicQualifiedUnit,
    WardQualifiedUnit,
)

type Quality = ClassicQuality | WardQuality
type SystemOutput = Sequence[AnnotatedSegment]
type State = tuple[bool, bool]
type ClassicMap = Mapping[State, ClassicQuality]
type PastCurrentNextQuality = tuple[ClassicQuality, ...]
type WardMap = Mapping[PastCurrentNextQuality, WardQuality]
type IndClassicQuality = tuple[int, ClassicQuality]
type IterIndClassicQuality = Iterator[IndClassicQuality]
type QualityStrings = set[str]
type QualitySet = set[Quality]
type ClassicQualUnitIter = Iterator[ClassicQualifiedUnit]
type WardQualUnitIter = Iterator[WardQualifiedUnit]
type QualUnitIter = Iterator[WardQualifiedUnit | ClassicQualifiedUnit]
type IndClassicQualities = tuple[IndClassicQuality, ...]
type QualityIndClassicQualities = tuple[ClassicQuality, IndClassicQualities]
type GrpIterIndClassicQuality = Iterator[QualityIndClassicQualities]
type MetricFormula = Mapping[Metric, Formula]
type GrpdQualUnitIter = Iterator[tuple[Quality, QualUnitIter]]
type RedGrpdQualUnitIter = Iterator[tuple[Quality, tuple[tuple[int, int], ...]]]
type QualityCount = Mapping[Quality, int]
type QualityDuration = Mapping[Quality, float]
type QualityCluster = Mapping[Quality, Cluster]
type QualityFixedQuanity = Mapping[Quality, float]
type QualityQuantity = QualityCount | QualityDuration
type Formatter = Callable[[str], str]


def get_formula(data: Metric, map: MetricFormula) -> Formula:
    return map[data]


def parse(data: Formula) -> QualityStrings:
    return set(findall(r"lambda_\w+", data))


def formatter(data: str) -> str:
    return data.split("_")[1].upper()


def format(data: QualityStrings, formatter: Formatter) -> QualitySet:
    return {
        (
            ClassicQuality[formatter(q)]
            if formatter(q) in ClassicQuality.__members__
            else WardQuality[formatter(q)]
        )
        for q in data
    }


def tag_classic(data: SystemOutput, map: ClassicMap) -> IterIndClassicQuality:
    for i, seg in enumerate(data):
        yield i, map[(seg.annotation.true, seg.annotation.pred)]


def group_segments(data: IterIndClassicQuality) -> GrpIterIndClassicQuality:
    for quality, group in groupby(data, key=itemgetter(1)):
        yield (quality, tuple(group))


def unify(data: GrpIterIndClassicQuality) -> ClassicQualUnitIter:
    for quality, group in data:
        yield ClassicQualifiedUnit(
            quality=quality,
            start=min(seg_index for seg_index, _ in group),
            end=max(seg_index for seg_index, _ in group) + 1,
        )


def tag_ward(data: ClassicQualUnitIter, map: WardMap) -> WardQualUnitIter:
    q_units_ = tuple(enumerate(data))
    for u in q_units_:
        yield WardQualifiedUnit(
            quality=map[
                (
                    q_units_[max(u[0] - 1, 0)][1].quality,
                    q_units_[u[0]][1].quality,
                    q_units_[min(u[0] + 1, len(q_units_) - 1)][1].quality,
                )
            ],
            start=u[1].start,
            end=u[1].end,
        )


def filter(data: QualUnitIter, required: QualitySet) -> QualUnitIter:
    for unit in data:
        if unit.quality in required:
            yield unit


def sort(data: QualUnitIter) -> QualUnitIter:
    for unit in sorted(data, key=lambda u: u.quality):
        yield unit


def group_units(data: QualUnitIter) -> GrpdQualUnitIter:
    for quality, group in groupby(data, key=lambda u: u.quality):
        yield (quality, group)


def reduce(data: GrpdQualUnitIter) -> RedGrpdQualUnitIter:
    for group_quality, group_units in data:
        yield (
            group_quality,
            tuple((unit.start, unit.end) for unit in tuple(group_units)),
        )


def count(data: RedGrpdQualUnitIter) -> QualityCount:
    return {quality: len(groups) for quality, groups in data}


def durify(data: RedGrpdQualUnitIter, output: SystemOutput) -> QualityDuration:
    return {
        quality: sum(
            (output[end - 1].end - output[start].start).total_seconds()
            for start, end in reduced_group
        )
        for quality, reduced_group in data
    }


def fix(data: QualityQuantity, map: QualityCluster) -> QualityFixedQuanity:
    return {
        target_quality: data[target_quality]
        / sum(
            data[quality]
            for quality in data
            if map[quality] == map[target_quality]
        )
        for target_quality in data
    }


def fill(data: Mapping[Quality, float], formula: str) -> str:
    filled_formula = formula
    for quality in data:
        filled_formula = filled_formula.replace(
            f"lambda_{quality}",
            str(data[quality]),
        )
    return filled_formula


def refill(data: str, default_value: float) -> str:
    return sub(r"lambda_\w+", str(default_value), data)


def evalaute(data: str, default_value: float) -> float:
    try:
        return eval(data)
    except ZeroDivisionError:
        return default_value


def compute_classic(
    segments: SystemOutput,
    classic_map: ClassicMap,
    quality_to_cluster: QualityCluster,
    formula_qualities: QualitySet,
    formula: Formula,
    default_value: float,
) -> float:
    result = tag_classic(segments, map=classic_map)
    result = group_segments(result)
    result = unify(result)
    result = filter(result, required=formula_qualities)
    result = sort(result)
    result = group_units(result)
    result = reduce(result)
    result = count(result)
    result = fix(result, map=quality_to_cluster)
    result = fill(result, formula=formula)
    result = refill(result, default_value=default_value)
    result = evalaute(result, default_value=default_value)
    return result


def compute_ward(
    segments: SystemOutput,
    classic_map: ClassicMap,
    ward_map: WardMap,
    quality_to_cluster: QualityCluster,
    formula_qualities: QualitySet,
    formula: Formula,
    default_value: float,
) -> float:
    result = tag_classic(segments, map=classic_map)
    result = group_segments(result)
    result = unify(result)
    result = tag_ward(result, map=ward_map)
    result = filter(result, required=formula_qualities)
    result = sort(result)
    result = group_units(result)
    result = reduce(result)
    result = count(result)
    result = fix(result, map=quality_to_cluster)
    result = fill(result, formula=formula)
    result = refill(result, default_value=default_value)
    result = evalaute(result, default_value=default_value)
    return result


def compute_ncibi(
    segments: SystemOutput,
    classic_map: ClassicMap,
    ward_map: WardMap,
    quality_to_cluster: QualityCluster,
    formula_qualities: QualitySet,
    formula: Formula,
    default_value: float,
) -> float:
    result = tag_classic(segments, map=classic_map)
    result = group_segments(result)
    result = unify(result)
    result = tag_ward(result, map=ward_map)
    result = filter(result, required=formula_qualities)
    result = sort(result)
    result = group_units(result)
    result = reduce(result)
    result = durify(result, output=segments)
    result = fix(result, map=quality_to_cluster)
    result = fill(result, formula=formula)
    result = refill(result, default_value=default_value)
    result = evalaute(result, default_value=default_value)
    return result


def score_annotated_segments(
    segments: SystemOutput,
    metric: Metric,
    metric_to_formula: MetricFormula,
    classic_map: ClassicMap,
    ward_map: WardMap,
    quality_to_cluster: Mapping[Quality, Cluster],
    default_value: float = 0.0,
) -> Optional[float]:
    formula = get_formula(metric, metric_to_formula)
    qualities_str = parse(formula)
    qualities = format(qualities_str, formatter=formatter)
    if isinstance(metric, ClassicMetric):
        return compute_classic(
            segments,
            classic_map,
            quality_to_cluster,
            qualities,
            formula,
            default_value,
        )
    if isinstance(metric, WardMetric):
        return compute_ward(
            segments,
            classic_map,
            ward_map,
            quality_to_cluster,
            qualities,
            formula,
            default_value,
        )
    if isinstance(metric, NcibiMetric):
        return compute_ncibi(
            segments,
            classic_map,
            ward_map,
            quality_to_cluster,
            qualities,
            formula,
            default_value,
        )
    return None


if __name__ == "__main__":

    segments = (
        AnnotatedSegment(
            start=datetime(2023, 10, 1, 12, 0),
            end=datetime(2023, 10, 1, 12, 5),
            annotation=ActivityState(
                true=True,
                pred=True,
            ),
        ),
        AnnotatedSegment(
            start=datetime(2023, 10, 1, 12, 5),
            end=datetime(2023, 10, 1, 12, 15),
            annotation=ActivityState(
                true=True,
                pred=True,
            ),
        ),
        AnnotatedSegment(
            start=datetime(2023, 10, 1, 12, 15),
            end=datetime(2023, 10, 1, 12, 45),
            annotation=ActivityState(
                true=True,
                pred=False,
            ),
        ),
        AnnotatedSegment(
            start=datetime(2023, 10, 1, 12, 45),
            end=datetime(2023, 10, 1, 12, 55),
            annotation=ActivityState(
                true=True,
                pred=True,
            ),
        ),
    )

    metric = ClassicMetric.ACC

    out = score_annotated_segments(
        segments,
        metric,
        METRIC_TO_FORMULA,
        QUALIFICATION_RULE_CLASSIC,
        QUALIFICATION_RULE_WARD,
        QUALITY_TO_CLUSTER,
        default_value=0.0,
    )

    print(f"Score {metric} {out:.4f}")
