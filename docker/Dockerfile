FROM python:3.6.15-slim-buster

LABEL author "Malakai Spann"
LABEL maintainers ["malakaispann@gmail.com",]
LABEL title "Hephaestus Dev"
LABEL description "The official Docker Image for developing, testing, and building the Hephaestus library."

# IMPORTANT: All instructions assume the build context is from the root of the repo.

# Upgrade Package Management OS
RUN apt-get update && \
    apt-get upgrade --assume-yes

# Install Python packages
RUN pip install --upgrade pip && \
    pip install --requirements config/dev.requirements.txt

