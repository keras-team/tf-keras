#!/bin/bash
isort --sl tf_keras
black --line-length 80 tf_keras
flake8 tf_keras
