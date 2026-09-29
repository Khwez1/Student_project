from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {'error': 'Something went wrong. Please try again'},
            status=500,
        )
    
    return response