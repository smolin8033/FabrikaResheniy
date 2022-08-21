from celery import shared_task
from celery.utils.log import get_task_logger

from config.celery import app


logger = get_task_logger(__name__)


@app.task
def sample_task():
    logger.info('The sample task has just run.')
