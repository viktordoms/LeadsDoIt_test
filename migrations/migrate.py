
import sys
sys.path.append('.')

import re
import typing as t
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column as Column_
from sqlalchemy.orm.attributes import InstrumentedAttribute

from libs.db import engine, Base

class MigrationException(Exception):
    """
    Exception class for migrations
    """

    pass

Table = Base
TableType = t.Type[Table]
Column = t.Union[Column_, InstrumentedAttribute]

class Migrator:

    def __init__(
            self,
            migration_engine: t.Optional[Engine] = None
    ) -> None:
        """
        Initialize migration object
        """

        self.engine = migration_engine or engine

        self.migration_codes = [
            str(attribute).replace("migration_", "")  # Get only code
            for attribute in self.__dir__()
            if re.fullmatch(r"^migration_[0-9a-f]+$", attribute)
        ]

    def run(self, code: str) -> bool:
        """
        Run specified migration

        Args:
            code (str): Migration code number

        Returns:
            bool: Whether migration was executed successfully or not
        """

        from libs.db import (
            db_session
        )

        if not re.fullmatch(f"^[0-9a-f]+$", code):
            # Invalid code
            raise MigrationException(f"Invalid migration code '{code}'")

        elif code not in self.migration_codes:
            # Not exists
            raise MigrationException(f"Migration with number '{code}' not found")

        print(f"Running migration with number '{code}'")

        migration: t.Callable = getattr(self, f"migration_{code}")

        try:
            # Run this migration
            migration()

        except (SQLAlchemyError, MigrationException, Exception) as error:
            # Failed
            print(f"Migration failed: {error}")
            return False

        else:
            # Success
            print("Migration finished.")
            db_session.commit()
            return True

    def create_tables(
            self,
            tables: t.Union[TableType, t.List[TableType]],
            *_tables: TableType,
            commit: bool = False,
    ) -> None:
        """
        Creates given tables
        If any of tables already exist, then it will be skipped.
        Tables you want to create may be specified as list, or as function parameters
        """

        from libs.db import db_session

        if not isinstance(tables, list):
            # Get from *_tables
            tables = [tables, *_tables]

        try:
            for table in tables:
                if not self.engine.dialect.has_table(self.engine, table.__table__.name):
                    # Not exists => create
                    table.__table__.create(self.engine, checkfirst=True)
                    print(f"Table '{table.__table__.name}' created.")
                else:
                    # Already exists
                    print(f"Table '{table.__table__.name}' already exists.")

            if commit:
                # Save changes
                db_session.commit()

        except (SQLAlchemyError, Exception) as error:
            # Failed
            db_session.rollback()
            table_names = "', '".join((table.__name__ for table in tables))
            raise MigrationException(
                f"Failed to create tables '{table_names}': {error}"
            )

    def migration_7156722f(self) -> None:
        """
        [19.05.2025] Create tables:
         - TblWeatherHistory
        """
        from libs.db import (
            TblWeatherHistory
        )

        self.create_tables(
            TblWeatherHistory,
            commit=True,
        )


def main() -> None:
    migrator = Migrator(engine)

    if len(sys.argv) > 1:
        for code in sys.argv[1:]:
            try:
                # Run with specified number
                migrator.run(code=code)

            except MigrationException as migration_error:
                # Failed
                print(migration_error)
                exit(-1)

    else:
        # Not specified
        print("Migration number is not specified.")
        return None


if __name__ == "__main__":
    main()
