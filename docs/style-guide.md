# Style Guide

## SQLAlchemy

* For string types always use `sqlalchemy.Text` instead of `sqlalchemy.String`.
* Follow the PostgreSQL [naming conventions](https://til.cybertec-postgresql.com/post/2019-09-02-Postgres-Constraint-Naming-Convention/) for keys and other indexes.
* If you need some specific types like URL, don't invent them by yourself.
Check out [sqlalchemy-utils.types](https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.url).
* When you define types based on `sqlalchemy.dialects.postgresql.ENUM` don't forget to specify.
the column's [name](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.Enum.params.name).
