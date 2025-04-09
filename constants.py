from enum import StrEnum


class ClassicMetric(StrEnum):
    ACC = "ACCURACY"
    F1 = "F1"
    MCC = "MCC"
    PRC = "PRC"
    SNS = "SNS"
    SPC = "SPC"
    NPV = "NPV"


class WardMetric(StrEnum):
    IN = "INSERTION"
    DE = "DELETION"
    SO = "START-OVERFILL"
    SU = "START-UNDERFILL"
    EO = "END-OVERFILL"
    EU = "END-UNDERFILL"
    ME = "MERGE"
    FR = "FRAGMENTATION"
    TP = "TP"
    TN = "TN"


class NcibiMetric(StrEnum):
    DURPLUS = "DURATION-PLUS"
    DURMINUS = "DURATION-MINUS"
    FREQPLUS = "FREQUENCY-PLUS"
    FREQMINUS = "FREQUENCY-MINUS"
    TP = "TP"
    TN = "TN"


type Metric = ClassicMetric | WardMetric | NcibiMetric


class ClassicQuality(StrEnum):
    TP = "TP"
    TN = "TN"
    FP = "FP"
    FN = "FN"


class WardQuality(StrEnum):
    IN = "IN"
    DE = "DE"
    SO = "SO"
    SU = "SU"
    EO = "EO"
    EU = "EU"
    ME = "ME"
    FR = "FR"
    TP = "TP"
    TN = "TN"


class NcibiQuality(StrEnum):
    DURPLUS = "DURPLUS"
    DURMINUS = "DURMINUS"
    FREQPLUS = "FREQPLUS"
    FREQMINUS = "FREQMINUS"
    TP = "TP"
    TN = "TN"


class Cluster(StrEnum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


class Formula(StrEnum):
    F1 = "(2 * lambda_TP)/(2 + lambda_TP - lambda_TN)"
    ACC = "(lambda_TP + lambda_TN)/2"
    IN = "lambda_IN"
    DE = "lambda_DE"
    SO = "lambda_SO"
    SU = "lambda_SU"
    EO = "lambda_EO"
    EU = "lambda_EU"
    ME = "lambda_ME"
    FR = "lambda_FR"
    TP = "lambda_TP"
    TN = "lambda_TN"
    MCC = "0.5 * (((lambda_TP+lambda_TN-1)/(((lambda_TP+1-lambda_TN)*(lambda_TN+1-lambda_TP))**0.5)) + 1)"
    PRC = "lambda_TP/(lambda_TP + (1-lambda_TN))"
    SNS = "lambda_TP"
    SPC = "lambda_TN"
    NPV = "lambda_TN/(lambda_TN + (1-lambda_TP))"
    DURPLUS = "lambda_DURPLUS"
    DURMINUS = "lambda_DURMINUS"
    FREQPLUS = "lambda_FREQPLUS"
    FREQMINUS = "lambda_FREQMINUS"


METRIC_TO_FORMULA = {
    ClassicMetric.F1: Formula.F1,
    ClassicMetric.ACC: Formula.ACC,
    ClassicMetric.MCC: Formula.MCC,
    ClassicMetric.PRC: Formula.PRC,
    ClassicMetric.SNS: Formula.SNS,
    ClassicMetric.SPC: Formula.SPC,
    ClassicMetric.NPV: Formula.NPV,
    WardMetric.IN: Formula.IN,
    WardMetric.DE: Formula.DE,
    WardMetric.SO: Formula.SO,
    WardMetric.SU: Formula.SU,
    WardMetric.EO: Formula.EO,
    WardMetric.EU: Formula.EU,
    WardMetric.ME: Formula.ME,
    WardMetric.FR: Formula.FR,
    WardMetric.TP: Formula.TP,
    WardMetric.TN: Formula.TN,
    NcibiMetric.DURPLUS: Formula.DURPLUS,
    NcibiMetric.DURMINUS: Formula.DURMINUS,
    NcibiMetric.FREQPLUS: Formula.FREQPLUS,
    NcibiMetric.FREQMINUS: Formula.FREQMINUS,
    NcibiMetric.TP: Formula.TP,
    NcibiMetric.TN: Formula.TN,
}

QUALIFICATION_RULE_CLASSIC = {
    (True, True): ClassicQuality.TP,
    (True, False): ClassicQuality.FN,
    (False, True): ClassicQuality.FP,
    (False, False): ClassicQuality.TN,
}

QUALIFICATION_RULE_WARD = {
    (ClassicQuality.FP, ClassicQuality.FP, ClassicQuality.TN): WardQuality.IN,
    (ClassicQuality.FP, ClassicQuality.FP, ClassicQuality.FN): WardQuality.IN,
    (ClassicQuality.TN, ClassicQuality.FP, ClassicQuality.FP): WardQuality.IN,
    (ClassicQuality.FN, ClassicQuality.FP, ClassicQuality.FP): WardQuality.IN,
    (ClassicQuality.TN, ClassicQuality.FP, ClassicQuality.TN): WardQuality.IN,
    (ClassicQuality.TN, ClassicQuality.FP, ClassicQuality.FN): WardQuality.IN,
    (ClassicQuality.FN, ClassicQuality.FP, ClassicQuality.FN): WardQuality.IN,
    (ClassicQuality.TN, ClassicQuality.FP, ClassicQuality.FN): WardQuality.IN,
    (ClassicQuality.FP, ClassicQuality.FP, ClassicQuality.TP): WardQuality.SO,
    (ClassicQuality.TN, ClassicQuality.FP, ClassicQuality.TP): WardQuality.SO,
    (ClassicQuality.FN, ClassicQuality.FP, ClassicQuality.TP): WardQuality.SO,
    (ClassicQuality.TP, ClassicQuality.FP, ClassicQuality.FP): WardQuality.EO,
    (ClassicQuality.TP, ClassicQuality.FP, ClassicQuality.TN): WardQuality.EO,
    (ClassicQuality.TP, ClassicQuality.FP, ClassicQuality.FN): WardQuality.EO,
    (ClassicQuality.TP, ClassicQuality.FP, ClassicQuality.TP): WardQuality.ME,
    ##
    (ClassicQuality.FN, ClassicQuality.FN, ClassicQuality.TN): WardQuality.DE,
    (ClassicQuality.FN, ClassicQuality.FN, ClassicQuality.FP): WardQuality.DE,
    (ClassicQuality.TN, ClassicQuality.FN, ClassicQuality.FN): WardQuality.DE,
    (ClassicQuality.FP, ClassicQuality.FN, ClassicQuality.FN): WardQuality.DE,
    (ClassicQuality.TN, ClassicQuality.FN, ClassicQuality.TN): WardQuality.DE,
    (ClassicQuality.TN, ClassicQuality.FN, ClassicQuality.FP): WardQuality.DE,
    (ClassicQuality.FP, ClassicQuality.FN, ClassicQuality.FP): WardQuality.DE,
    (ClassicQuality.TN, ClassicQuality.FN, ClassicQuality.FP): WardQuality.DE,
    (ClassicQuality.FN, ClassicQuality.FN, ClassicQuality.TP): WardQuality.SU,
    (ClassicQuality.TN, ClassicQuality.FN, ClassicQuality.TP): WardQuality.SU,
    (ClassicQuality.FP, ClassicQuality.FN, ClassicQuality.TP): WardQuality.SU,
    (ClassicQuality.TP, ClassicQuality.FN, ClassicQuality.FN): WardQuality.EU,
    (ClassicQuality.TP, ClassicQuality.FN, ClassicQuality.TN): WardQuality.EU,
    (ClassicQuality.TP, ClassicQuality.FN, ClassicQuality.FP): WardQuality.EU,
    (ClassicQuality.TP, ClassicQuality.FN, ClassicQuality.TP): WardQuality.FR,
    ##
    (ClassicQuality.TP, ClassicQuality.TP, ClassicQuality.TP): WardQuality.TP,
    (ClassicQuality.TP, ClassicQuality.TP, ClassicQuality.TN): WardQuality.TP,
    (ClassicQuality.TP, ClassicQuality.TP, ClassicQuality.FP): WardQuality.TP,
    (ClassicQuality.TP, ClassicQuality.TP, ClassicQuality.FN): WardQuality.TP,
    (ClassicQuality.TN, ClassicQuality.TP, ClassicQuality.TP): WardQuality.TP,
    (ClassicQuality.TN, ClassicQuality.TP, ClassicQuality.TN): WardQuality.TP,
    (ClassicQuality.TN, ClassicQuality.TP, ClassicQuality.FP): WardQuality.TP,
    (ClassicQuality.TN, ClassicQuality.TP, ClassicQuality.FN): WardQuality.TP,
    (ClassicQuality.FP, ClassicQuality.TP, ClassicQuality.TP): WardQuality.TP,
    (ClassicQuality.FP, ClassicQuality.TP, ClassicQuality.TN): WardQuality.TP,
    (ClassicQuality.FP, ClassicQuality.TP, ClassicQuality.FP): WardQuality.TP,
    (ClassicQuality.FP, ClassicQuality.TP, ClassicQuality.FN): WardQuality.TP,
    (ClassicQuality.FN, ClassicQuality.TP, ClassicQuality.TP): WardQuality.TP,
    (ClassicQuality.FN, ClassicQuality.TP, ClassicQuality.TN): WardQuality.TP,
    (ClassicQuality.FN, ClassicQuality.TP, ClassicQuality.FP): WardQuality.TP,
    (ClassicQuality.FN, ClassicQuality.TP, ClassicQuality.FN): WardQuality.TP,
    ##
    (ClassicQuality.TP, ClassicQuality.TN, ClassicQuality.TP): WardQuality.TN,
    (ClassicQuality.TP, ClassicQuality.TN, ClassicQuality.TN): WardQuality.TN,
    (ClassicQuality.TP, ClassicQuality.TN, ClassicQuality.FP): WardQuality.TN,
    (ClassicQuality.TP, ClassicQuality.TN, ClassicQuality.FN): WardQuality.TN,
    (ClassicQuality.TN, ClassicQuality.TN, ClassicQuality.TP): WardQuality.TN,
    (ClassicQuality.TN, ClassicQuality.TN, ClassicQuality.TN): WardQuality.TN,
    (ClassicQuality.TN, ClassicQuality.TN, ClassicQuality.FP): WardQuality.TN,
    (ClassicQuality.TN, ClassicQuality.TN, ClassicQuality.FN): WardQuality.TN,
    (ClassicQuality.FP, ClassicQuality.TN, ClassicQuality.TP): WardQuality.TN,
    (ClassicQuality.FP, ClassicQuality.TN, ClassicQuality.TN): WardQuality.TN,
    (ClassicQuality.FP, ClassicQuality.TN, ClassicQuality.FP): WardQuality.TN,
    (ClassicQuality.FP, ClassicQuality.TN, ClassicQuality.FN): WardQuality.TN,
    (ClassicQuality.FN, ClassicQuality.TN, ClassicQuality.TP): WardQuality.TN,
    (ClassicQuality.FN, ClassicQuality.TN, ClassicQuality.TN): WardQuality.TN,
    (ClassicQuality.FN, ClassicQuality.TN, ClassicQuality.FP): WardQuality.TN,
    (ClassicQuality.FN, ClassicQuality.TN, ClassicQuality.FN): WardQuality.TN,
}
QUALIFICATION_RULE_NCIBI = {
    WardQuality.IN: NcibiQuality.FREQPLUS,
    WardQuality.FR: NcibiQuality.FREQPLUS,
    WardQuality.DE: NcibiQuality.FREQMINUS,
    WardQuality.ME: NcibiQuality.FREQMINUS,
    WardQuality.SO: NcibiQuality.DURPLUS,
    WardQuality.EO: NcibiQuality.DURPLUS,
    WardQuality.SU: NcibiQuality.DURMINUS,
    WardQuality.EU: NcibiQuality.DURMINUS,
    WardQuality.TP: NcibiQuality.TP,
    WardQuality.TN: NcibiQuality.TN,
}

QUALITY_TO_CLUSTER = {
    ClassicQuality.TP: Cluster.POSITIVE,
    ClassicQuality.FN: Cluster.POSITIVE,
    ClassicQuality.TN: Cluster.NEGATIVE,
    ClassicQuality.FP: Cluster.NEGATIVE,
    WardQuality.DE: Cluster.POSITIVE,
    WardQuality.SU: Cluster.POSITIVE,
    WardQuality.EU: Cluster.POSITIVE,
    WardQuality.FR: Cluster.POSITIVE,
    WardQuality.IN: Cluster.NEGATIVE,
    WardQuality.SO: Cluster.NEGATIVE,
    WardQuality.EO: Cluster.NEGATIVE,
    WardQuality.ME: Cluster.NEGATIVE,
}
