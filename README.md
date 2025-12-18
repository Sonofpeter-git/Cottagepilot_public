# SensorHub - IoT Sensor Management Platform

A comprehensive IoT sensor management platform built with Vue.js, Django, and MongoDB. Monitor, analyze, and manage your sensor network with real-time data visualization and advanced analytics.

## Features

### Frontend (Vue.js + TypeScript)
- **Modern UI/UX**: Beautiful, responsive design with Tailwind CSS
- **Real-time Monitoring**: Live sensor data updates and visualization
- **Interactive Dashboards**: Customizable charts and analytics
- **Sensor Management**: Add, edit, delete, and configure sensors
- **Data Visualization**: Advanced charts with Chart.js integration
- **Mobile Responsive**: Works seamlessly on all devices

### Backend (Django + MongoDB)
- **RESTful API**: Comprehensive API for sensor and data management
- **MongoDB Integration**: Scalable NoSQL database for sensor data
- **Real-time Processing**: Background tasks with Celery
- **Advanced Analytics**: AI-powered insights and trend analysis
- **Alert System**: Configurable alerts and notifications
- **User Authentication**: Secure user management and permissions

## Tech Stack

### Frontend
- Vue 3 with Composition API
- TypeScript for type safety
- Tailwind CSS for styling
- Pinia for state management
- Vue Router for navigation
- Chart.js for data visualization
- Axios for API communication

### Backend
- Django 4.2 with Django REST Framework
- MongoDB with Djongo ORM
- Celery for background tasks
- Redis for caching and task queue
- JWT authentication
- Comprehensive API documentation

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- MongoDB 5.0+
- Redis 6.0+

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Database Setup
1. Install and start MongoDB
2. Install and start Redis
3. Update `.env` file with your database credentials

## API Endpoints

### Sensors
- `GET /api/sensors/` - List all sensors
- `POST /api/sensors/` - Create new sensor
- `GET /api/sensors/{id}/` - Get sensor details
- `PUT /api/sensors/{id}/` - Update sensor
- `DELETE /api/sensors/{id}/` - Delete sensor
- `GET /api/sensors/{id}/data/` - Get sensor data
- `POST /api/sensors/{id}/add_data/` - Add sensor data

### Analytics
- `GET /api/analytics/reports/` - List analytics reports
- `GET /api/analytics/insights/` - Get sensor insights
- `POST /api/analytics/insights/generate_insights/` - Generate new insights

## Project Structure

```
sensorhub/
├── src/                    # Frontend source code
│   ├── components/         # Vue components
│   ├── views/             # Page components
│   ├── stores/            # Pinia stores
│   ├── services/          # API services
│   ├── types/             # TypeScript types
│   └── router/            # Vue Router configuration
├── backend/               # Django backend
│   ├── sensorhub/         # Main Django project
│   ├── sensors/           # Sensors app
│   ├── analytics/         # Analytics app
│   └── requirements.txt   # Python dependencies
└── README.md
```

## Key Features

### Sensor Management
- Add sensors with various types (temperature, humidity, pressure, etc.)
- Real-time status monitoring
- Bulk operations and filtering
- Location-based organization

### Data Visualization
- Interactive charts and graphs
- Historical data analysis
- Real-time updates
- Customizable time ranges

### Analytics & Insights
- Trend analysis
- Anomaly detection
- Predictive analytics
- Custom reports

### Alert System
- Threshold-based alerts
- Real-time notifications
- Multiple severity levels
- Alert history and management

## Deployment

### Frontend (Netlify/Vercel)
```bash
npm run build
# Deploy dist/ folder to your hosting provider
```

### Backend (Production)
```bash
# Install production dependencies
pip install gunicorn

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn sensorhub.wsgi:application
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: support@sensorhub.com
- Documentation: [docs.sensorhub.com](https://docs.sensorhub.com)
- Issues: [GitHub Issues](https://github.com/sensorhub/issues)