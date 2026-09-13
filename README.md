# LLM Usage Metering & Billing Service

A scalable backend service built with FastAPI, SQLAlchemy, PostgreSQL, and Stripe for tracking LLM token consumption, calculating tiered model costs, and automating customer invoicing.

## Features
- **User Management**: Customer profile registration and tracking.
- **API Key Provisioning**: Secure key generation for API authentication.
- **Automated Metering**: Live cost tracking for models including `gpt-4o`, `gpt-4o-mini`, and `claude-3-5-sonnet`.
- **Invoicing System**: Aggregated cost calculations and pending invoice generation.

## Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL (via Docker) & SQLAlchemy ORM
- **Validation**: Pydantic
- **Billing**: Stripe SDK

## Quickstart

1. **Clone the repository**
   ```bash
   git clone [https://github.com/RayyanAHR/flyrank-capstone-metering-billing.git](https://github.com/RayyanAHR/flyrank-capstone-metering-billing.git)
   cd flyrank-capstone-metering-billing
