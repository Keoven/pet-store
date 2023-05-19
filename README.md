## Discussion Points

- Since there isn't much information on how species would get added or removed,
  I went ahead and just moved that to its own table for now to be more flexible.
  At the end, it will depend on the additional requirements for this.

## How to Run

```
1. docker compose build
2. docker compose up -d
3. Go inside the docker container to migrate database: 

docker exec -it pet-store-web-1 bash

4. Setup database

alembic upgrade head

5. Use the following to seed data:

export PYTHONPATH="${PYTHONPATH}:/app"
python -i tests/utils.py

6. Run this inside the interactive python shell that opens up from above:

from pet_store.db import SessionLocal
seed_species(SessionLocal())

7. Visit http://localhost:8000/docs
```
