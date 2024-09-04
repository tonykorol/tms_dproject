#!/bin/sh

celery -A worker.worker worker -l INFO
