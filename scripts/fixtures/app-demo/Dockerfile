# Mini-app de démonstration pour le test réel de la production locale (scripts/test_prod_locale.py).
# Contrat de l'app (ARCHITECTURE § 9, DEC-003) : ARG GIT_COMMIT figé dans l'image, écoute sur $PORT.
FROM python:3.12-alpine
ARG GIT_COMMIT=inconnu
ENV GIT_COMMIT=${GIT_COMMIT} PORT=8000 PYTHONUNBUFFERED=1
WORKDIR /app
COPY app.py .
EXPOSE 8000
CMD ["python", "app.py"]
