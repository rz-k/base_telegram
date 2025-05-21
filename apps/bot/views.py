import json
import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from apps.bot.dispatcher import Dispatcher
from apps.bot.telegram_models import Update


class TelegramWebhookView(APIView):

    def post(self, request):
        try:
            update_dict = request.data
            print(json.dumps(update_dict, indent=4, ensure_ascii=False))

            update = Update(**update_dict)
            Dispatcher(update).dispatch()

        except Exception as e:
            msg = traceback.format_exc().strip()
            formate_msg = (f"\n{'-'*30}\n{' '*7}Your Exception:{' '*7}| \n{'-'*100}\n{msg}\n{'-'*100}")
            print(formate_msg)
        
        return Response({"ok": True})
