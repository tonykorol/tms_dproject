#!/bin/sh

celery -A worker.worker beat -l INFO