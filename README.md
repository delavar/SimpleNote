 # How to Run the Simple Note Application

## Prerequisites
- Docker and Docker Compose installed on your system

## Setup Instructions

1. **Configure Environment Variables**
   - Copy `local.env.sample` to `local.env`
   - Fill in the required PostgreSQL credentials:
     ```
     POSTGRES_DB=simplenote_db
     POSTGRES_USER=your_username
     POSTGRES_PASSWORD=your_password
     ```

2. **Optional: Set Debug Level & Allowed Hosts**
   - Add `DEBUG=True` to your `local.env` file to enable Django debug mode
   - Set `DEBUG=False` for production environments
   - Set other acceptable hosts other than `localhost` for example for android emulators you might want to use `10.0.2.2` to connect to host network. You can set this using `ALLOWED_HOSTS=0.0.2.2,localhost,0.0.0.0` environment variable in `local.env`
  

3. **Run the Application**
   ```bash
   docker-compose up --build
   ```

4. **Access the Application**
   - Open your browser and navigate to `http://localhost:8000`
   - The application will automatically run migrations on startup

## Stopping the Application
bash
docker-compose down
