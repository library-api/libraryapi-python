"""Dataclass models for libraryapi responses. Hand-rolled (no pydantic) to keep deps to httpx only."""
from dataclasses import dataclass, fields
from typing import Any, Optional, Union, get_args, get_origin


def _camel_to_snake(s: str) -> str:
    out: list[str] = []
    for i, ch in enumerate(s):
        if ch.isupper() and i > 0:
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


_FIELD_TYPE_CACHE: dict[type, dict[str, Optional[type]]] = {}


def _resolve_dataclass_types(cls) -> dict[str, Optional[type]]:
    """For each field on cls, return the inner dataclass type (or None for scalars)."""
    cached = _FIELD_TYPE_CACHE.get(cls)
    if cached is not None:
        return cached
    out: dict[str, Optional[type]] = {}
    for f in fields(cls):
        annot = f.type
        # Resolve string forward refs (also accommodates Optional[X])
        if isinstance(annot, str):
            cleaned = annot.replace("Optional[", "").rstrip("]").strip()
            out[f.name] = _DATACLASS_TYPES.get(cleaned)
            continue
        # Optional[X] / Union[X, None] → unwrap
        if get_origin(annot) is Union:
            inner = [a for a in get_args(annot) if a is not type(None)]
            if len(inner) == 1:
                annot = inner[0]
        out[f.name] = annot if isinstance(annot, type) and getattr(annot, "__module__", "") == __name__ else None
    _FIELD_TYPE_CACHE[cls] = out
    return out


def _from_dict(cls, data: Optional[dict]):
    """Build a dataclass instance from a camelCase dict, ignoring unknown keys."""
    if data is None:
        return None
    snake = {_camel_to_snake(k): v for k, v in data.items()}
    sub_types = _resolve_dataclass_types(cls)
    kwargs: dict[str, Any] = {}
    for f in fields(cls):
        v = snake.get(f.name)
        sub = sub_types[f.name]
        if v is None:
            kwargs[f.name] = None
        elif sub is not None:
            kwargs[f.name] = sub._from_dict(v)
        else:
            kwargs[f.name] = v
    return cls(**kwargs)


_DATACLASS_TYPES: dict[str, type] = {}


@dataclass
class Address:
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    zip4: Optional[str] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class GeoPoint:
    lat: Optional[float] = None
    lng: Optional[float] = None
    geocode_quality: Optional[str] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class ParentSystem:
    fscs_id: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class OutletService:
    annual_hours: Optional[int] = None
    weeks_open: Optional[int] = None
    square_footage: Optional[int] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class Outlet:
    outlet_id: Optional[str] = None
    fscs_id: Optional[str] = None
    name: Optional[str] = None
    outlet_type: Optional[str] = None
    parent_system: Optional[ParentSystem] = None
    address: Optional[Address] = None
    phone: Optional[str] = None
    geo: Optional[GeoPoint] = None
    service: Optional[OutletService] = None
    status: Optional[str] = None
    data_year: Optional[str] = None
    distance_miles: Optional[float] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)

    @property
    def weekly_hours(self) -> Optional[int]:
        """Convenience: round(annualHours / weeksOpen)."""
        if self.service and self.service.annual_hours and self.service.weeks_open:
            return round(self.service.annual_hours / self.service.weeks_open)
        return None


@dataclass
class Locale:
    code: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class ServiceArea:
    population: Optional[int] = None
    central_libraries: Optional[int] = None
    branches: Optional[int] = None
    bookmobiles: Optional[int] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class Collections:
    print_volumes: Optional[int] = None
    ebooks: Optional[int] = None
    audio_physical: Optional[int] = None
    audio_downloadable: Optional[int] = None
    video_physical: Optional[int] = None
    video_downloadable: Optional[int] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class Programs:
    total: Optional[int] = None
    kids: Optional[int] = None
    young_adult: Optional[int] = None
    attendance_total: Optional[int] = None
    attendance_kids: Optional[int] = None
    attendance_ya: Optional[int] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class Technology:
    public_computers: Optional[int] = None
    computer_sessions: Optional[int] = None
    wifi_sessions: Optional[int] = None
    website_visits: Optional[int] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class Usage:
    annual_visits: Optional[int] = None
    registered_borrowers: Optional[int] = None
    total_circulation: Optional[int] = None
    kids_circulation: Optional[int] = None
    physical_circulation: Optional[int] = None
    electronic_circulation: Optional[int] = None
    programs: Optional[Programs] = None
    technology: Optional[Technology] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class StaffFTE:
    mls_librarians: Optional[float] = None
    librarians: Optional[float] = None
    other: Optional[float] = None
    total: Optional[float] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class Finance:
    total_revenue: Optional[int] = None
    local_revenue: Optional[int] = None
    state_revenue: Optional[int] = None
    federal_revenue: Optional[int] = None
    other_revenue: Optional[int] = None
    total_expenditures: Optional[int] = None
    per_capita_expenditure: Optional[float] = None
    staff_fte: Optional[StaffFTE] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class LibrarySystem:
    fscs_id: Optional[str] = None
    name: Optional[str] = None
    state: Optional[str] = None
    county: Optional[str] = None
    address: Optional[Address] = None
    phone: Optional[str] = None
    legal_basis: Optional[str] = None
    locale: Optional[Locale] = None
    service_area: Optional[ServiceArea] = None
    collections: Optional[Collections] = None
    usage: Optional[Usage] = None
    finance: Optional[Finance] = None
    outlets_count: Optional[int] = None
    status: Optional[str] = None
    data_year: Optional[str] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class StateTotals:
    library_systems: Optional[int] = None
    outlets: Optional[int] = None
    service_area_population: Optional[int] = None
    annual_visits: Optional[int] = None
    total_circulation: Optional[int] = None
    total_expenditures: Optional[int] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class StateAverages:
    per_capita_expenditure: Optional[float] = None
    outlets_per_system: Optional[float] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class StateSummary:
    state: Optional[str] = None
    data_year: Optional[str] = None
    totals: Optional[StateTotals] = None
    averages: Optional[StateAverages] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class ResponseMeta:
    request_id: Optional[str] = None
    credits_used: Optional[int] = None
    credits_remaining: Optional[int] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


@dataclass
class ResponseSource:
    imls_year: Optional[str] = None
    updated_at: Optional[str] = None
    freshness_days: Optional[int] = None

    @classmethod
    def _from_dict(cls, d):
        return _from_dict(cls, d)


# Register for forward-ref resolution
for _cls in [
    Address, GeoPoint, ParentSystem, OutletService, Outlet,
    Locale, ServiceArea, Collections, Programs, Technology, Usage,
    StaffFTE, Finance, LibrarySystem,
    StateTotals, StateAverages, StateSummary,
    ResponseMeta, ResponseSource,
]:
    _DATACLASS_TYPES[_cls.__name__] = _cls
