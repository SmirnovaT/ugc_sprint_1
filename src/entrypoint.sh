#!/usr/bin/env bash

gunicorn main:app --bind 0.0.0.0:$APP_PORT --workers 4