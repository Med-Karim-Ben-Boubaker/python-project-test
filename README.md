# FastAPI CI/CD Demo

A simple FastAPI application with testing and Jenkins CI/CD pipeline integration.

## Features

- RESTful API with FastAPI
- Unit tests with pytest
- Code coverage reporting
- Jenkins pipeline configuration
- Linting with flake8

## Prerequisites

- Python 3.7+
- pip
- Jenkins (for CI/CD pipeline)

## Setup

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd python-project-test
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

## API Documentation

- Interactive API docs: http://127.0.0.1:8000/docs
- Alternative API docs: http://127.0.0.1:8000/redoc

## Running Tests

Run all tests with coverage:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=app --cov-report=term-missing
```

## Linting

Run flake8 for code style checking:
```bash
flake8 app --count --max-complexity=10 --max-line-length=127 --statistics
```

## Jenkins Pipeline

The project includes a `Jenkinsfile` that defines the CI/CD pipeline with the following stages:

1. **Setup**: Creates a virtual environment and installs dependencies
2. **Lint**: Runs flake8 for code style checking
3. **Test**: Runs unit tests with coverage
4. **Build**: Placeholder for build steps
5. **Deploy**: Placeholder for deployment (runs only on main branch)

To set up the Jenkins pipeline:

1. Install required Jenkins plugins:
   - Pipeline
   - JUnit
   - Cobertura
   - HTML Publisher

2. Create a new Pipeline job in Jenkins and point it to your repository's `Jenkinsfile`.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   └── tests/            # Test files
│       ├── __init__.py
│       ├── conftest.py   # Test fixtures
│       └── test_main.py  # Test cases
├── requirements.txt      # Project dependencies
├── pytest.ini           # Pytest configuration
└── Jenkinsfile          # Jenkins pipeline definition
```

## License

This project is open source and available under the [MIT License](LICENSE).
