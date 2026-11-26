
from flask_openapi3 import APIBlueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


# API Version 1 Blueprint
v1_bp = APIBlueprint(
    "api_v1",
    __name__,
    doc_ui=False
)


# Add deprecation header to every v1 response
@v1_bp.after_request
def add_deprecation_header(response):
    response.headers["Deprecation"] = "true"
    return response


# GET all applications - API v1
@v1_bp.get("/applications")
@jwt_required()
def get_applications_v1():
    from app import db, JobApplication, ApplicationStatus

    current_user_id = int(get_jwt_identity())

    # Read pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status_filter = request.args.get("status")

    # Validate pagination
    if page < 1 or per_page < 1 or per_page > 100:
        return jsonify({
            "error": "Invalid pagination parameters"
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

    applications = [
        application.to_dict()
        for application in pagination.items
    ]

    response = jsonify({
        "version": "v1",
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

    # Pagination headers
    response.headers["X-Total-Count"] = str(pagination.total)
    response.headers["X-Page"] = str(pagination.page)
    response.headers["X-Per-Page"] = str(pagination.per_page)
    response.headers["X-Total-Pages"] = str(pagination.pages)

    return response
