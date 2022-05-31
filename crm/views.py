from django.shortcuts import render
import logging


logger = logging.getLogger(__name__)


def main_page(request):
    logger.info("GET_MAIN_PAGE__200")
    return render(request, "crm/index.html")
