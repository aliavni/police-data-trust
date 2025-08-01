from typing import Optional, List
from datetime import datetime

from backend.auth.jwt import min_role_required
from backend.database.models.user import UserRole
from backend.database.models.officer import Officer
from backend.database.models.agency import Agency, Unit
from flask import Blueprint, abort, request
from flask_jwt_extended.view_decorators import jwt_required
from flask import jsonify
from pydantic import BaseModel
from neomodel import db


bp = Blueprint("search_routes", __name__, url_prefix="/api/v1/search")


class Searchresult(BaseModel):
    uid: str
    title: str
    subtitle: Optional[str] = None
    details: Optional[List[str]] = None
    content_type: str
    source: str
    last_updated: datetime
    href: str


def create_officer_result(node) -> Searchresult:
    o = Officer.inflate(node)

    uid = o.uid

    # Subtitle Example: "Asian Man, Sergeant at Agency X"
    u = o.current_unit
    a = u.agency.single() if u else None
    u_rel = u.officers.relationship(o) if u else None

    s = o.primary_source()
    s_rel = o.citations.relationship(s) if s else None

    sub_title = "{ethnicity} {gender}, {rank} at the {agency}".format(
        ethnicity=(
            o.ethnicity_enum.describe()
            if o.ethnicity_enum else "Unknown Ethnicity"
        ),
        gender=(
            o.gender_enum.describe()
            if o.gender_enum else "Unknown Gender"
        ),
        rank=(
            u_rel.highest_rank
            if u_rel else "Officer"
        ),
        agency=(
            a.name
            if a else "Unknown Agency"
        )
    )

    return Searchresult(
        uid=uid,
        title=o.full_name,
        subtitle=sub_title,
        content_type="Officer",
        source=s.name if s else "Unknown Source",
        last_updated=s_rel.date if s_rel else None,
        href=f"/api/v1/officers/{uid}"
    )


def create_agency_result(node) -> Searchresult:
    a = Agency.inflate(node)

    uid = a.uid

    s = a.primary_source
    s_rel = a.citations.relationship(s) if s else None

    return Searchresult(
        uid=uid,
        title=a.name,
        subtitle="{} Agency in {}, {}".format(
            a.jurisdiction_enum.describe() if a.jurisdiction_enum else "",
            a.hq_city if a.hq_city else "Unknown City",
            a.hq_state if a.hq_state else "Unknown State"
        ),
        details=[
            "{} Unit(s) and {} Officers".format(
                len(a.units) if a.units else 0,
                a.total_officers()
            )
        ],
        content_type="Agency",
        source=s.name if s else "Unknown Source",
        last_updated=s_rel.date if s_rel else datetime.now(),
        href=f"/api/v1/agencies/{uid}"
    )


def create_unit_result(node) -> Searchresult:
    u = Unit.inflate(node)

    uid = u.uid

    s = u.primary_source
    s_rel = u.citations.relationship(s)

    return Searchresult(
        uid=uid,
        title=u.name,
        subtitle="Established by the {}".format(
            u.agency.single().name if u.agency else "Unknown Agency"
        ),
        details=[
            "{} Officer(s)".format(
                len(u.officers) if u.officers else 0
            ),
            "Commander: {}".format(
                u.current_commander.full_name
                if u.current_commander else "Unknown"
            )
        ],
        content_type="Unit",
        source=s.name if s else "Unknown Source",
        last_updated=s_rel.date if s_rel else datetime.now(),
        href=f"/api/v1/units/{uid}"
    )


def create_search_result(node) -> Searchresult:
    if "Officer" in node.labels:
        return create_officer_result(node)
    elif "Agency" in node.labels:
        return create_agency_result(node)
    elif "Unit" in node.labels:
        return create_unit_result(node)
    return None


# Text Search Endpoint
@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
def text_search():
    """Text Search
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    query = args.get("query", None, type=str)
    params = {"query": query}

    if not query:
        abort(400, description="Query parameter is required")

    # Query Everything
    cypher = """
    CALL {
        CALL db.index.fulltext.queryNodes('officerNames', $query)
            YIELD node, score
            RETURN node, score
        UNION ALL
        CALL db.index.fulltext.queryNodes('agencyNames', $query)
            YIELD node, score
            RETURN node, score
        UNION ALL
        CALL db.index.fulltext.queryNodes('unitNames', $query)
            YIELD node, score
            RETURN node, score
    }
    RETURN node, score
    ORDER BY score DESC
    """

    results, meta = db.cypher_query(cypher, params)
    if not results:
        return jsonify({"message": "No results found matching the query"}), 204

    res = []
    for result in results[:10]:
        item = create_search_result(result[0])
        res.append(item.model_dump()) if item else None
    return jsonify(res), 200
