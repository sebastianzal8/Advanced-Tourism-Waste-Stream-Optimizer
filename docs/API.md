# API Documentation

## Overview
The Advanced Tourism Waste Stream Optimizer API provides endpoints for managing and analyzing waste data in tourism destinations.

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.waste-optimizer.com`

## Authentication
The API uses JWT tokens for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Health Check
- **GET** `/health`
- Returns the health status of the API

### Waste Data
- **GET** `/api/waste-data`
- Retrieve waste data for analysis
- **POST** `/api/waste-data`
- Upload new waste data
- **PUT** `/api/waste-data/{id}`
- Update existing waste data
- **DELETE** `/api/waste-data/{id}`
- Delete waste data

### Analytics
- **GET** `/api/analytics/summary`
- Get waste analytics summary
- **GET** `/api/analytics/predictions`
- Get waste generation predictions
- **POST** `/api/analytics/optimize`
- Generate optimization recommendations

### Reports
- **GET** `/api/reports/sustainability`
- Generate sustainability report
- **GET** `/api/reports/cost-analysis`
- Generate cost analysis report

## Data Models

### Waste Data
```json
{
  "id": "string",
  "destination": "string",
  "waste_type": "string",
  "quantity": "number",
  "unit": "string",
  "date": "string",
  "source": "string"
}
```

### Optimization Recommendation
```json
{
  "id": "string",
  "destination": "string",
  "recommendation_type": "string",
  "description": "string",
  "estimated_savings": "number",
  "implementation_cost": "number",
  "roi": "number"
}
```

## Error Responses
All error responses follow this format:
```json
{
  "error": "string",
  "message": "string",
  "status_code": "number"
}
```

## Rate Limiting
- 100 requests per minute per API key
- 1000 requests per hour per API key 