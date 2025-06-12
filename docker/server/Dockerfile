FROM python:3.10-slim

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости заранее для кэширования
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем curl и другие нужные пакеты
RUN apt-get update && apt-get install -y curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
ENV POETRY_VERSION=1.8.1
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Настройка Poetry (устанавливаем зависимости в системную среду)
ENV PYTHONDONTWRITEBYTECODE=1
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Копируем остальной код (после установки зависимостей для кэширования)
COPY . /app

# Указываем порт и команду запуска
EXPOSE 8000
CMD ["uvicorn", "web.server:app", "--host", "0.0.0.0", "--port", "8000"]
