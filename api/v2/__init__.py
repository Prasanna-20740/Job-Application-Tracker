
from flask_openapi3 import APIBlueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


# API Version 2 Blueprint
v2_bp = APIBlueprint(
    "api_v2",
    __name__,
    doc_ui=False
)


# GET all applications - API v2
@v2_bp.get("/applications")
@jwt_required()
def get_applications_v2():
    from app import JobApplication, ApplicationStatus

    current_user_id = int(get_jwt_identity())

    # Read query parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status_filter = request.args.get("status")
    response_format = request.args.get("format", "full").lower()

    # Validate parameters
    if page < 1 or per_page < 1 or per_page > 100:
        return jsonify({
            "error": "Invalid pagination parameters"
        }), 400

    if response_format not in ["full", "summary"]:
        return jsonify({
            "error": "Invalid format. Use full or summary"
        }), 400

    # Get current user's applications
    query = JobApplication.query.filter_by(
        user_id=current_user_id
    )

    # Optional status filter
    if status_filter:
        try:
            status = ApplicationStatus(status_filter.upper())
            query = query.filter_by(status=status)
        except ValueError:
            return jsonify({
                "error": "Invalid application status"
            }), 400

    # Pagination
    pagination = query.order_by(
        JobApplication.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # Full or summary response
    if response_format == "summary":
        applications = [
            {
                "id": application.id,
                "company": application.company,
                "role": application.role,
                "status": application.status.value,
                "applied_date": (
                    application.applied_date.isoformat()
                    if application.applied_date else None
                )
            }
            for application in pagination.items
        ]
    else:
        applications = [
            application.to_dict()
            for application in pagination.items
        ]

    return jsonify({
        "version": "v2",
        "format": response_format,
        "applications": applications,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "total_pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    })
