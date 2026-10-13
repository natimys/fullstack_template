import os


os.environ.update(
    {
        "DB_USER": "test_user",
        "DB_PASSWORD": "test-only-database-password",
        "DB_NAME": "test_database",
        "JWT_SECURITY_KEY": "test-only-key-with-more-than-thirty-two-characters",
        "ACCESS_TOKEN_EXPIRES": "15",
        "REFRESH_TOKEN_EXPIRES": "30",
        "CORS_ORIGINS": "[]",
        "CORS_ALLOW_CREDENTIALS": "true",
        "CORS_ALLOW_METHODS": '["GET","POST","PATCH","DELETE","OPTIONS"]',
        "CORS_ALLOW_HEADERS": '["Content-Type","X-CSRF-TOKEN"]',
    }
)
