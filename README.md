# URL Shortener Service

## Overview

The **URL Shortener Service** is a simple and efficient web application built with **FastAPI**. It allows users to shorten long URLs into concise, shareable links.

Key features include:
- FastAPI framework for high-performance endpoints
- Auto-generated Swagger documentation for API exploration
- Fully dockerized for ease of deployment
- Environment-based configurations for flexible development and production setups

---

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.10+
- Docker and Docker Compose
- Poetry for dependency management (for development)

---

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AliHezarpisheh/url-shortener-fastapi.git
   cd url-shortener-fastapi
   ```

2. Create a `.env.development` file based on the provided example:
   ```bash
   cp .env.development.example .env.development
   ```
   Configure the values as needed.

3. Install dependencies using Poetry:
   ```bash
   poetry env use 3.13 && poetry install
   ```

4. Run the application in development mode:
   ```bash
   fastapi dev
   ```

5. Access the Swagger documentation at:
   ```
   http://localhost:8000/docs
   ```

---

## Deployment with Docker

1. Create a `.env.production` file based on the provided example:
   ```bash
   cp .env.production.example .env.production
   ```
   Configure the values as needed.

2. Build and start the Docker container:
   ```bash
   docker-compose up -d --build
   ```

3. The application will be available at:
   ```
   http://localhost:8000
   ```

4. Swagger documentation can also be accessed at:
   ```
   http://localhost:8000/docs
   ```

---

## Configuration

- Ensure that `.env.development` and `.env.production` files are created based on the respective example files provided.
- These files contain critical environment variables like database connections and secret keys.
- Update the configurations as necessary to match your environment.

---

For any issues or questions, please contact me!
