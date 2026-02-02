# etl-data-warehouse-pipeline
Built an end-to-end idempotent ETL pipeline that consumes OpenWeatherMap API, transforms JSON data, and loads it into a PostgreSQL data warehouse.

Designed dimensional schema with facts and dimensions, enforcing referential integrity and uniqueness constraints.

Implemented idempotent load logic using PostgreSQL ON CONFLICT and unique constraints to prevent duplicate data.

Handled real-world ETL errors including schema mismatch, SSL/API issues, and missing constraints.

Automated workflow using Python scripts and environment variables for secure and reproducible pipelines.