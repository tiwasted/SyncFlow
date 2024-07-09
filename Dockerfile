# Использует официальный образ Python
FROM python:3.11

ENV PYTHONUNBUFFERED=1

# Устанавливает зависимости системы
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

# Проверяет poetry
RUN poetry --version

# Устанавливает рабочую директорию
WORKDIR /app

# Копирует файлы poetry.lock pyproject.toml
COPY pyproject.toml poetry.lock* /app/
# RUN pip install poetry

RUN poetry install --no-root

# Копирует файлы проекта
COPY src/ /app/

# Открывает порт
EXPOSE 8000

# Команда для запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
