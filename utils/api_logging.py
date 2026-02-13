import json
import logging

import allure
import curlify
from allure_commons.types import AttachmentType

logger = logging.getLogger('api')
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    )
    logger.addHandler(handler)


def allure_request_logger(response, *args, **kwargs):
    """Hook for requests.Session — logs request/response to Allure and console."""

    logger.info(
        '%s %s => %s',
        response.request.method,
        response.request.url,
        response.status_code,
    )

    allure.attach(
        body=curlify.to_curl(response.request),
        name='Request curl',
        attachment_type=AttachmentType.TEXT,
        extension='.txt',
    )

    if response.request.body:
        try:
            body = json.dumps(
                json.loads(response.request.body), indent=2, ensure_ascii=False
            )
        except (json.JSONDecodeError, TypeError):
            body = str(response.request.body)
        allure.attach(
            body=body,
            name='Request body',
            attachment_type=AttachmentType.JSON,
            extension='.json',
        )

    try:
        response_body = json.dumps(response.json(), indent=2, ensure_ascii=False)
        content_type = AttachmentType.JSON
        ext = '.json'
    except (json.JSONDecodeError, ValueError):
        response_body = response.text
        content_type = AttachmentType.TEXT
        ext = '.txt'

    allure.attach(
        body=response_body,
        name=f'Response [{response.status_code}]',
        attachment_type=content_type,
        extension=ext,
    )
