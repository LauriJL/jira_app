import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .services import NdaValidationError, build_nda, suggested_filename, validate


@csrf_exempt
@require_POST
def generate_nda(request):
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)

    try:
        data = validate(payload)
    except NdaValidationError as exc:
        return JsonResponse({"errors": exc.errors}, status=400)

    markdown = build_nda(data)
    return JsonResponse({"markdown": markdown, "filename": suggested_filename(data)})
