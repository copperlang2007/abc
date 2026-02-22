"""Utilities to normalize spreadsheet column schemas.

The main goal is to convert arbitrary spreadsheet headers into stable,
machine-friendly field names while preserving enough metadata to map
normalized fields back to their original columns.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata
from typing import Iterable, List


@dataclass(frozen=True)
class ColumnMapping:
    """Represents one original spreadsheet column and its normalized name."""

    original_name: str
    normalized_name: str
    index: int


_NON_ALNUM_PATTERN = re.compile(r"[^a-z0-9]+")
_MULTI_UNDERSCORE_PATTERN = re.compile(r"_+")


def _slugify(value: str) -> str:
    """Normalize a raw column name into an ASCII snake_case slug."""

    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower().strip()
    value = _NON_ALNUM_PATTERN.sub("_", value)
    value = _MULTI_UNDERSCORE_PATTERN.sub("_", value)
    return value.strip("_")


def normalize_spreadsheet_schema(
    headers: Iterable[str],
    *,
    default_prefix: str = "column",
) -> List[ColumnMapping]:
    """Normalize spreadsheet header names into deterministic field names.

    Rules:
    1. Headers are transformed to ASCII snake_case.
    2. Empty/invalid headers become ``{default_prefix}_{index}``.
    3. Duplicate normalized names are de-duplicated with a numeric suffix,
       e.g. ``name``, ``name_2``, ``name_3``.

    Args:
        headers: Iterable of raw header values (strings).
        default_prefix: Prefix used when a header has no valid characters.

    Returns:
        A list of :class:`ColumnMapping` entries preserving input order.
    """

    seen: dict[str, int] = {}
    mappings: List[ColumnMapping] = []

    for index, raw_name in enumerate(headers, start=1):
        normalized = _slugify(raw_name)

        if not normalized:
            normalized = f"{default_prefix}_{index}"

        if normalized in seen:
            seen[normalized] += 1
            normalized = f"{normalized}_{seen[normalized]}"
        else:
            seen[normalized] = 1

        mappings.append(
            ColumnMapping(
                original_name=raw_name,
                normalized_name=normalized,
                index=index,
            )
        )

    return mappings
