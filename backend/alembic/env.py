import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app import db
from app.models.user import User
from app.models.otp import Otp

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
# for 'autogenerate' support
target_metadata = db.Model.metadata

# Function to build the database URL from environment variables
def get_database_url():
    db_user = os.getenv('DATABASE_USER')
    db_password = os.getenv('DATABASE_PASSWORD')
    db_host = os.getenv('DATABASE_HOST')
    db_name = os.getenv('DATABASE_NAME')
    db_port = os.getenv('DATABASE_PORT', '3306')  # Default to 3306 if no port is provided

    return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Run migrations in 'offline' mode
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_database_url()  # Use the dynamic URL from environment variables
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Run migrations in 'online' mode
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine whether to run in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
