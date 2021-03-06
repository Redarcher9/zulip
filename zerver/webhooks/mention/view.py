# Webhooks for external integrations.
from typing import Any, Dict, Iterable, Optional, Text

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.actions import check_send_stream_message
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.lib.validator import check_dict, check_string
from zerver.models import UserProfile

@api_key_only_webhook_view('Mention')
@has_request_variables
def api_mention_webhook(request: HttpRequest, user_profile: UserProfile,
                        payload: Dict[str, Iterable[Dict[str, Any]]] = REQ(argument_type='body'),
                        stream: Text = REQ(default='mention'),
                        topic: Optional[Text] = REQ(default='news')) -> HttpResponse:
    title = payload["title"]
    source_url = payload["url"]
    description = payload["description"]
    # construct the body of the message
    body = '**[%s](%s)**:\n%s' % (title, source_url, description)

    # send the message
    check_send_stream_message(user_profile, request.client, stream, topic, body)

    return json_success()
