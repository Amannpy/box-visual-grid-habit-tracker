# Box-Based Visual Grid Habit Tracker

A revolutionary habit tracking system that transforms daily activities into an intuitive, visually engaging experience using customizable colored grid squares.

## 🎯 Product Overview

The Box-Based Visual Grid System represents a revolutionary approach to habit tracking that transforms daily activities into an intuitive, visually engaging experience. By representing each day as a customizable grid of colored squares, users can quickly tap boxes to log activities, creating a beautiful mosaic of their life patterns over time.

## ✨ Key Features

### Core Features (MVP)
- **Visual Grid Calendar**: Customizable daily grids with color-coded activity boxes
- **Multiple Grid Layouts**: 4x4, 6x6, 8x8 configurations
- **GitHub-style Heat Map**: Beautiful pattern visualization
- **Touch-responsive Interface**: Optimized for mobile and web
- **Activity Management**: Quick creation with color and icon selection
- **Basic Analytics**: Streak counters and completion tracking
- **User Authentication**: Simple email/password with guest mode

### Enhanced Features
- **Smart Reminders**: Customizable notification system
- **Data Insights**: Pattern recognition and correlation analysis
- **Customization Options**: Multiple themes and color palettes

## 🏗️ Technical Architecture

### Backend
- **Framework**: Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **Containerization**: Docker

### Frontend
- **Framework**: React with TypeScript
- **PWA**: Service Workers for offline functionality
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker & Docker Compose
- PostgreSQL

### Backend Setup
```bash
# Clone the repository
git clone <repository-url>
cd box-visual-grid-habit-tracker

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Docker Setup
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d
```

## 📊 Market Opportunity

- **US Market**: Projected to grow from $5.80B (2025) to $20.76B (2034) - CAGR 15.20%
- **Global Market**: Expected to reach $30.34B by 2032 - CAGR 13.21%

## 🎯 Unique Selling Proposition

1. **Instant Visual Feedback**: Pixel-grid approach provides immediate visual gratification
2. **Intuitive One-Tap Logging**: Record habits from home-screen widgets
3. **Beautiful Pattern Recognition**: Daily activities create artistic mosaics
4. **Zero Learning Curve**: No training or complex setup required
5. **Privacy-First Architecture**: All data remains on-device

## 📁 Project Structure

```
box-visual-grid-habit-tracker/
├── backend/                 # Django REST API
│   ├── core/               # Core Django settings
│   ├── users/              # User management
│   ├── activities/         # Activity and grid models
│   ├── analytics/          # Analytics and insights
│   └── api/                # API endpoints
├── frontend/               # React PWA
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── store/          # Redux store
│   │   └── utils/          # Utility functions
│   └── public/             # Static assets
├── docker-compose.yml      # Docker configuration
└── requirements.txt        # Python dependencies
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Activities
- `GET /api/activities/` - List user activities
- `POST /api/activities/` - Create new activity
- `PUT /api/activities/{id}/` - Update activity
- `DELETE /api/activities/{id}/` - Delete activity

### Grid Operations
- `GET /api/grids/{date}/` - Get daily grid
- `POST /api/grids/{date}/log/` - Log activity in grid
- `GET /api/grids/range/{start_date}/{end_date}/` - Get grid range

### Analytics
- `GET /api/analytics/streaks/` - Get activity streaks
- `GET /api/analytics/completion-rates/` - Get completion rates
- `GET /api/analytics/patterns/` - Get pattern insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@boxgridtracker.com or create an issue in this repository.