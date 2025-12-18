#!/bin/bash

# RADIX Startup Script
# This script starts both backend and frontend services

echo "========================================="
echo "  RADIX - Radar Data Integration"
echo "  & eXtraction Framework"
echo "========================================="
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed"
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Check if dependencies are installed
if ! python -c "import fastapi" &> /dev/null; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "🚀 Starting RADIX services..."
echo ""

# Start backend in background
echo "Starting Backend on http://localhost:8000"
python -m uvicorn radix.api.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend in background
echo "Starting Frontend on http://localhost:3000"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================="
echo "✅ RADIX is running!"
echo "========================================="
echo ""
echo "🌐 Web Interface: http://localhost:3000"
echo "📡 API Docs:      http://localhost:8000/docs"
echo "🔌 WebSocket:     ws://localhost:8000/ws"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================="
echo ""

# Trap Ctrl+C and cleanup
cleanup() {
    echo ""
    echo "🛑 Stopping RADIX services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    # Also kill any child processes
    pkill -P $BACKEND_PID 2>/dev/null
    pkill -P $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for services to stop
wait
