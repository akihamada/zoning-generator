"""
荷重組合せモジュール — 令82条に基づく荷重ケースと組合せ

出典:
  - 建築基準法施行令 第82条（許容応力度計算）
  - 建築基準法施行令 第83条（固定荷重）
  - 建築基準法施行令 第85条（積載荷重）
  - 建築基準法施行令 第86条（積雪荷重）
  - 建築基準法施行令 第87条（風圧力）
  - 建築基準法施行令 第88条（地震力）

単位: 荷重値自体は本モジュールでは扱わない。
       組合せ係数のみ定義し、実荷重は外部から与える。
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class LoadCase:
    """単一荷重ケース

    Attributes:
        name: 荷重ケース名 ("G", "P", "S", "W", "K" 等)
        description: 説明
        duration: "long" (長期) または "short" (短期)
    """

    name: str
    description: str
    duration: str  # "long" or "short"


@dataclass(frozen=True)
class LoadCombination:
    """荷重組合せ

    出典: 令82条 第一号〜第三号

    Attributes:
        name: 組合せ名
        factors: 各荷重ケースの係数 {"G": 1.0, "P": 1.0, ...}
        duration: "long" or "short"
        description: 令の条文参照
    """

    name: str
    factors: dict  # {荷重ケース名: 係数}
    duration: str
    description: str


# --- 標準荷重ケース ---
LC_G = LoadCase("G", "固定荷重（令83条）", "long")
LC_P = LoadCase("P", "積載荷重（令85条）", "long")
LC_S = LoadCase("S", "積雪荷重（令86条）", "short")
LC_W = LoadCase("W", "風圧力（令87条）", "short")
LC_K = LoadCase("K", "地震力（令88条）", "short")


# --- 令82条に基づく標準荷重組合せ ---
STANDARD_COMBINATIONS = [
    # ---- 長期 (令82条第一号) ----
    LoadCombination(
        name="長期(常時)",
        factors={"G": 1.0, "P": 1.0},
        duration="long",
        description="令82条第一号: G + P",
    ),
    # 多雪区域の長期積雪
    LoadCombination(
        name="長期(積雪・多雪区域)",
        factors={"G": 1.0, "P": 1.0, "S": 0.7},
        duration="long",
        description="令82条第一号: G + P + 0.7S（多雪区域）",
    ),
    # ---- 短期 (令82条第二号) ----
    LoadCombination(
        name="短期(積雪)",
        factors={"G": 1.0, "P": 1.0, "S": 1.0},
        duration="short",
        description="令82条第二号: G + P + S",
    ),
    LoadCombination(
        name="短期(風)",
        factors={"G": 1.0, "P": 1.0, "W": 1.0},
        duration="short",
        description="令82条第二号: G + P + W",
    ),
    LoadCombination(
        name="短期(地震)",
        factors={"G": 1.0, "P": 1.0, "K": 1.0},
        duration="short",
        description="令82条第二号: G + P + K",
    ),
    # 多雪区域の短期
    LoadCombination(
        name="短期(積雪+風・多雪区域)",
        factors={"G": 1.0, "P": 1.0, "S": 0.35, "W": 1.0},
        duration="short",
        description="令82条第二号: G + P + 0.35S + W（多雪区域）",
    ),
    LoadCombination(
        name="短期(積雪+地震・多雪区域)",
        factors={"G": 1.0, "P": 1.0, "S": 0.35, "K": 1.0},
        duration="short",
        description="令82条第二号: G + P + 0.35S + K（多雪区域）",
    ),
]
