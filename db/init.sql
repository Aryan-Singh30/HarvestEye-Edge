-- Enable uuid-ossp extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The FastAPI app will create the table using SQLAlchemy's create_all(),
-- but creating the database and enabling extensions here ensures readiness.
