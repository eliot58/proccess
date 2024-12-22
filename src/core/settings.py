import os

DATABASE_URI = f'postgres://{os.environ.get("POSTGRES_USER")}:' \
               f'{os.environ.get("POSTGRES_PASSWORD")}@' \
               f'{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/' \
               f'{os.environ.get("POSTGRES_DB")}'

API_KEY = os.environ.get("API_KEY", "test")

DEPOSIT_ADDRESSES = {
    "ton": "",
    "not": "",
    "usdt": ""
}

APPS_MODELS = [
    "src.user.models",
    "aerich.models",
]