# Goals FastAPI

Goals FastAPI is a web application that allows users to track and manage their personal goals. The project consists of a backend API built with FastAPI and a frontend user interface developed with React.js.

## Installation

### Frontend

1. Clone the repository:
   ```
   git clone https://github.com/gbs278/goals-fastapi.git
   ```

2. Navigate to the frontend directory:
   ```
   cd goals-fastapi/frontend/frontend
   ```

3. Install the frontend dependencies:
   ```
   npm install
   ```

4. Start the frontend development server:
   ```
   npm start
   ```

   The frontend application will be running at `http://localhost:3000`.

### Backend

1. Clone the repository:
   ```
   git clone https://github.com/gbs278/goals-fastapi.git
   ```

2. Navigate to the backend directory:
   ```
   cd goals-fastapi/backend
   ```

3. Install the backend dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```
   uvicorn main:app --reload
   ```

   The backend API will be running at `http://localhost:8000`.

## Usage

Once both the frontend and backend servers are running, you can access the Goals FastAPI application by visiting `http://localhost:3000` in your web browser. The frontend interface allows you to interact with the application, create goals, update progress, and view goal statistics. The backend API provides the necessary endpoints for handling goal-related operations.

## Contributing

Contributions to the Goals FastAPI project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the project's GitHub repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
