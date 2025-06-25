import json
import traceback

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.telegram.dispatcher import Dispatcher
from apps.telegram.telegram_models import Update
from utils.logger import logger


class TelegramWebhookView(APIView):
    """
    A Django REST Framework API view that handles incoming POST requests from the Telegram Bot API.

    This view:
    - Parses the incoming JSON payload from Telegram.
    - Constructs an `Update` object from the payload.
    - Passes the update to the `Dispatcher` to determine how it should be handled.
    - Logs any exceptions that occur during processing.

    Returns:
        JSON response indicating success ({"ok": True}).
    """

    def post(self, request: Request) -> Response:
        """
        Handles incoming Telegram webhook POST request.

        Args:
            request (Request): The incoming HTTP request from Telegram containing the update payload.

        Returns:
            Response: A JSON response with a success message.
        """
        try:
            update_dict = request.data
            logger.info("Received Telegram update:\n%s", json.dumps(update_dict, indent=4, ensure_ascii=False))

            update = Update(**update_dict)
            Dispatcher(update).dispatch()

        except Exception:
            error_msg = traceback.format_exc().strip()
            logger.error("Exception while processing Telegram update:\n%s", error_msg)

        return Response({"ok": True}, status=status.HTTP_200_OK)
