# Superhero API

## Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pipenv install
   ```
3. Activate the virtual environment:
   ```bash
   pipenv shell
   ```
4. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
5. Run the application:
   ```bash
   flask run
   ```

## Endpoints

- `GET /heroes`: List all heroes.
- `GET /heroes/<id>`: Get a specific hero by ID.
- `GET /powers`: List all powers.
- `GET /powers/<id>`: Get a specific power by ID.
- `PATCH /powers/<id>`: Update a power's description.
- `POST /hero_powers`: Create a new hero-power association.

## Testing

Use the provided Postman collection to test the API.
