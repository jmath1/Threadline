import logging

logger = logging.getLogger("django")

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the incoming request
        logger.info(f"Request: {request.method} {request.path} {request.body}")

        # Process the response
        response = self.get_response(request)

        # Log the outgoing response
        content_lines = response.content.splitlines()
        if len(content_lines) > 100:
            logger.info(f"Response: {response.status_code} {content_lines[:100]} [Content truncated]")
        else:
            logger.info(f"Response: {response.status_code} {response.content}")

        return response
