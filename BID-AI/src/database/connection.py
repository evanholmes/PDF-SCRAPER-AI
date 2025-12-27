"""
Database connection and session management for BID-AI
"""

import os
from contextlib import contextmanager

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from .models import Base

# Load environment variables
load_dotenv()


class DatabaseManager:
    """Manages database connections and sessions"""

    def __init__(self, database_url: str = None):
        """
        Initialize database manager

        Args:
            database_url: PostgreSQL connection string.
                         If None, reads from DATABASE_URL env variable
        """
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", "postgresql://localhost/bidai"
        )

        # Create engine
        self.engine = create_engine(
            self.database_url,
            echo=os.getenv("SQL_ECHO", "False").lower() == "true",
            pool_pre_ping=True,  # Verify connections before using
            pool_size=10,
            max_overflow=20,
        )

        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        logger.info(f"Database manager initialized")

    def create_all_tables(self):
        """Create all tables defined in models"""
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=self.engine)
        logger.success("All tables created successfully")

    def drop_all_tables(self):
        """Drop all tables (USE WITH CAUTION!)"""
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=self.engine)
        logger.warning("All tables dropped")

    def reset_database(self):
        """Drop and recreate all tables (USE WITH CAUTION!)"""
        logger.warning("Resetting database...")
        self.drop_all_tables()
        self.create_all_tables()
        logger.success("Database reset complete")

    @contextmanager
    def get_session(self) -> Session:
        """
        Context manager for database sessions

        Usage:
            with db.get_session() as session:
                # do database operations
                session.add(obj)
                session.commit()
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def execute_sql_file(self, filepath: str):
        """
        Execute SQL commands from a file

        Args:
            filepath: Path to SQL file
        """
        logger.info(f"Executing SQL file: {filepath}")

        with open(filepath, "r") as f:
            sql_commands = f.read()

        with self.engine.begin() as conn:
            # Split by semicolon and execute each statement
            for statement in sql_commands.split(";"):
                statement = statement.strip()
                if statement:
                    try:
                        conn.execute(statement)
                    except Exception as e:
                        logger.error(f"Error executing statement: {e}")
                        logger.debug(f"Statement: {statement[:100]}...")
                        raise

        logger.success(f"SQL file executed successfully: {filepath}")


# Global database manager instance
db_manager = None


def init_db(database_url: str = None) -> DatabaseManager:
    """
    Initialize the global database manager

    Args:
        database_url: PostgreSQL connection string

    Returns:
        DatabaseManager instance
    """
    global db_manager

    if db_manager is None:
        db_manager = DatabaseManager(database_url)

    return db_manager


def get_db() -> DatabaseManager:
    """
    Get the global database manager instance

    Returns:
        DatabaseManager instance

    Raises:
        RuntimeError: If database not initialized
    """
    if db_manager is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    return db_manager


# Convenience function for getting sessions
@contextmanager
def get_session() -> Session:
    """
    Convenience function to get a database session

    Usage:
        from database.connection import get_session

        with get_session() as session:
            opportunities = session.query(Opportunity).all()
    """
    db = get_db()
    with db.get_session() as session:
        yield session


if __name__ == "__main__":
    # Example usage / testing
    from loguru import logger

    logger.info("Testing database connection...")

    # Initialize database
    db = init_db()

    # Create tables
    db.create_all_tables()

    # Test session
    with get_session() as session:
        from .models import Municipality

        # Try to query municipalities
        municipalities = session.query(Municipality).all()
        logger.info(f"Found {len(municipalities)} municipalities")

    logger.success("Database connection test successful!")
