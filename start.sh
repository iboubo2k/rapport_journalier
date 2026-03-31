#!/usr/bin/env bash
streamlit run main.py \
  --server.headless true \
  --server.address 0.0.0.0 \
  --server.port ${PORT:-10000} \
  --server.enableCORS false \
  --server.enableXsrfProtection false
