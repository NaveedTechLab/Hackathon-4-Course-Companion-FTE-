# Course Companion FTE

A full-stack educational learning management system (LMS) that operates as a digital tutor 168 hours/week. Built with FastAPI backend and Next.js frontend, featuring AI-powered premium features.

![Course Companion](https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=800&h=400&fit=crop)

## Project Structure

```
Course-Companion-FTE/
├── phase-1/          # Core FastAPI Backend (Port 8000)
├── phase-2/          # Premium API with AI Features (Port 8001)
├── phase-3/          # Next.js Frontend (Port 3000)
└── README.md         # This file
```

## Features

### Core Features (Free)
- User Authentication (Email/Password, Google, Facebook)
- Course Browsing & Enrollment
- Progress Tracking
- Basic Quizzes
- Learning Paths
- User Profiles & Settings

### Premium Features (AI-Powered)
- Adaptive Learning Paths
- LLM-Graded Assessments
- Cross-Chapter Synthesis
- Advanced Analytics
- Priority Support

## Tech Stack

### Backend (Phase 1 & 2)
- **Framework:** FastAPI (Python 3.9+)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Storage:** Cloudflare R2 for media assets
- **AI:** Claude API for premium features

### Frontend (Phase 3)
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Charts:** Chart.js with react-chartjs-2
- **Icons:** Heroicons
- **State:** React Context API

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL (optional for full backend)

### Running the Frontend (Phase 3)

```bash
cd phase-3
npm install
npm run dev
```

Visit `http://localhost:3000`

### Running the Backend (Phase 1)

```bash
cd phase-1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs at `http://localhost:8000/docs`

### Running Premium API (Phase 2)

```bash
cd phase-2
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## Demo Credentials

The frontend includes a demo mode:
- **Email/Password:** Any valid email with 6+ character password
- **Social Login:** Click Google or Facebook for instant demo access

## Screenshots

### Dashboard
- Personalized greeting
- Course progress tracking
- Weekly activity charts
- Score trends

### Courses
- Browse all available courses
- Filter by category
- Search functionality
- Enrollment system

### Learning Path
- Structured learning journey
- Progress indicators
- Lesson, Quiz, and Project types

## Environment Variables

### Phase 1 & 2 (Backend)
```env
DATABASE_URL=postgresql://user:pass@localhost/coursedb
R2_ACCESS_KEY_ID=your_r2_key
R2_SECRET_ACCESS_KEY=your_r2_secret
R2_BUCKET_NAME=course-companion
ANTHROPIC_API_KEY=your_claude_key
```

### Phase 3 (Frontend)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_PREMIUM_API_URL=http://localhost:8001
```

## API Endpoints

### Phase 1 - Core API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses` | List all courses |
| GET | `/api/courses/{id}` | Get course details |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/register` | User registration |
| GET | `/api/progress` | User progress |

### Phase 2 - Premium API
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/adaptive-path` | Generate learning path |
| POST | `/api/grade-response` | AI grading |
| POST | `/api/synthesize` | Cross-chapter synthesis |

## Responsive Design

The frontend is fully responsive:
- **Mobile:** Hamburger menu, touch-friendly UI
- **Tablet:** Adaptive grid layouts
- **Desktop:** Full sidebar navigation

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Next.js](https://nextjs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Heroicons](https://heroicons.com/)
- [Unsplash](https://unsplash.com/) for images
