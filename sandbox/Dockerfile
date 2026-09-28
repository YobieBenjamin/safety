# Sandbox for building/testing untrusted (model-written) algorithm code.
# No secrets, no network at run time (enforced by run.sh), non-root user.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev make coreutils \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir numpy==2.5.3 scipy==1.18.1 scikit-learn==1.9.1
RUN python -c "from sklearn.datasets import load_digits; load_digits()"
RUN useradd -m -u 10001 miner
USER miner
ENV PYTHONDONTWRITEBYTECODE=1 HOME=/tmp
WORKDIR /work
