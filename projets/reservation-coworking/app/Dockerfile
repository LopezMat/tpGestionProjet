# Image de production de l'app de réservation (DEC-003, architecture.md § 8).
# Construction : docker build --build-arg GIT_COMMIT=<sha40> -t esn-reservation-coworking:<sha40> .
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dépendances de production seulement (jamais requirements-dev.txt).
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Utilisateur non root.
RUN useradd --system --create-home --uid 10001 app

COPY reservation ./reservation

# SHA figé dans l'image, renvoyé par /health ; placé en fin de fichier pour ne pas
# invalider le cache des couches précédentes à chaque commit.
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

ENV PORT=8000
EXPOSE 8000
USER app

CMD ["python", "-m", "reservation.demarrer"]
