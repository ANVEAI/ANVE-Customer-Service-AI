# ANVE Customer Service AI

An enterprise-grade AI-powered customer service solution that combines FastAPI, Streamlit, and LangChain to provide intelligent customer support capabilities.

## Features

- 🤖 AI-powered response generation
- 🎯 Intent classification
- 📊 Sentiment analysis
- 🌐 Multi-language support
- 📝 Conversation context management
- 📈 Performance analytics
- 🔐 Secure authentication
- 📊 Admin dashboard

## Technical Stack

- Backend: FastAPI
- Frontend: Streamlit
- AI/ML: LangChain + OpenAI
- Database: PostgreSQL
- Containerization: Docker
- Authentication: JWT

## Prerequisites

- Docker and Docker Compose
- OpenAI API Key
- Python 3.9+

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/ANVEAI/anve-customer-service-ai.git
cd anve-customer-service-ai
```

2. Create a `.env` file in the root directory:
```bash
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=anve_customer_service
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
```

## Running the Application

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Access the applications:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Project Structure

```
/anve-customer-service-ai
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
├── frontend/
│   ├── pages/
│   └── components/
├── tests/
├── docker/
└── docs/
```

### Running Tests

```bash
docker-compose exec backend pytest
```

### API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Security Features

- JWT Authentication
- Rate Limiting
- Input Validation
- Data Encryption
- Secure Token Management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 