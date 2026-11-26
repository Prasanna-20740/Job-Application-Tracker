
# API Migration Guide: V1 to V2

## 1. Overview

The Job Application Tracker API supports two versions:

- V1: `/api/v1/`
- V2: `/api/v2/`

V1 is maintained for backward compatibility and includes a deprecation warning header. V2 provides improved response formatting.

## 2. Authentication

Both API versions require JWT Bearer Token authentication.

Add the following header to your requests:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 3. Endpoint Migration

| Feature | V1 Endpoint | V2 Endpoint |
|---|---|---|
| Get applications | `/api/v1/applications` | `/api/v2/applications` |

To migrate, replace `/api/v1/` with `/api/v2/` in your request URL.

## 4. Response Format

### V1 Response

V1 returns the full application details:

- id
- company
- role
- status
- applied_date
- notes
- user_id
- resume_path

V1 also includes the following response header:

```http
Deprecation: true
```

### V2 Full Response

By default, V2 returns full application details:

```http
GET /api/v2/applications
```

Use this format when you need all application fields.

### V2 Summary Response

V2 supports a compact response:

```http
GET /api/v2/applications?format=summary
```

Summary includes only:

- id
- company
- role
- status
- applied_date

Fields such as notes, user_id, and resume_path are omitted.

## 5. Pagination

Both versions support pagination:

```http
GET /api/v2/applications?page=1&per_page=10
```

Supported parameters:

- `page`: Page number (default: 1)
- `per_page`: Records per page (default: 10, maximum: 100)
- `status`: Optional application status filter

## 6. Migration Steps

1. Update the API base path from `/api/v1/` to `/api/v2/`.
2. Keep using JWT Bearer Token authentication.
3. Check whether your application needs full or summary response data.
4. If you need all fields, use the default V2 response.
5. If you need compact data, use `?format=summary`.
6. Test your application with V2 before discontinuing V1 usage.

## 7. Deprecation Notice

V1 endpoints include the response header:

```http
Deprecation: true
```

Clients are encouraged to migrate to V2.

## 8. Backward Compatibility

V1 and V2 currently coexist. V1 remains available for existing clients while they migrate to V2.
