# SUBJECT TO CHANGE
# csc3730_YoutubeAnalytics
This is a repository for a Machine Learning Project in which we scrape data from the Youtube API and run analysis on the data for the different video categories of Youtube. 


# YouTube Analytics App

A simple web application that fetches the top YouTube videos from selected categories once per day and displays them in a clean frontend.  
Built with React (frontend), Python (backend), and deployed on Microsoft Azure free tiers.

---

## Tech Stack

### Frontend
- **Language**: JavaScript (ES6+)
- **Framework**: React (create-react-app or Vite)
- **UI Libraries**: 
  - Tailwind CSS (for styling)
  - Axios (for API requests)
- **Hosting/Deployment**: Azure Static Web Apps (Free Tier)

### Backend
- **Language**: Python 3.x
- **Framework**: FastAPI (lightweight and fast) or Flask (simple and minimal)
- **Libraries**:
  - requests (for making HTTP calls if needed)
  - google-api-python-client (for interacting with YouTube Data API v3)
  - python-dotenv (for managing API keys and environment variables)
  - schedule or APScheduler (to run daily scraping tasks)
- **Hosting/Deployment**: Azure App Service (Free Tier)

### Data & APIs
- **API**: YouTube Data API v3 (via free Google API key)
- **Data Storage**: Azure Cosmos DB (Free Tier) or Azure Table Storage (simpler, free option)

### DevOps & Tools
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions (automatic deployment to Azure)
- **Environment Management**: .env files (local), Azure App Service Configuration (production)

---

## How It Works

1. **Frontend (React)**
   - User visits the web app hosted on Azure Static Web Apps.
   - The frontend displays available YouTube categories and top videos (fetched from the backend).
   - All requests to get video data are sent to the backend API.

2. **Backend (Python + FastAPI/Flask)**
   - The backend runs on Azure App Service.
   - A scheduled job (using `schedule` or `APScheduler`) calls the YouTube Data API once per day.
   - Data from the YouTube API is processed and stored in Azure (Cosmos DB or Table Storage).
   - When the frontend makes a request, the backend returns the latest stored results.

3. **YouTube Data API**
   - The backend uses the YouTube Data API v3 to fetch the top videos from selected categories.
   - Only non-sensitive data (video titles, IDs, views, thumbnails, etc.) is stored and returned.
   - API keys are kept secret using environment variables, never exposed in the frontend.

4. **Data Flow**
   - **Daily Scrape** → Backend fetches and stores results.
   - **Frontend Request** → User request hits backend API.
   - **Backend Response** → Returns cached/stored YouTube data to frontend.
   - **Frontend Display** → React renders the video information in a clean UI.

5. **CI/CD**
   - Code is managed with Git + GitHub.
   - GitHub Actions automatically build and deploy the frontend/backend to Azure on each push.

---
