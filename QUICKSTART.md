# RADIX Quick Start Guide

Get RADIX up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:

```bash
# Check Python version (3.8+)
python --version

# Check Node.js version (16+)
node --version

# Check npm
npm --version

# Check pip
pip --version
```

If any are missing, install them first.

## Step 1: Install Dependencies

### Backend Dependencies

```bash
# From the workspace directory
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- NumPy, Pandas (data processing)
- Uvicorn (ASGI server)
- SQLAlchemy (database)
- And other dependencies

### Frontend Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Return to workspace root
cd ..
```

## Step 2: Start the Backend

Open a terminal and run:

```bash
python -m uvicorn radix.api.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Keep this terminal open!**

## Step 3: Start the Frontend

Open a **new terminal** and run:

```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Keep this terminal open too!**

## Step 4: Access the Application

Open your web browser and navigate to:

**http://localhost:3000**

You should see the RADIX interface with:
- Real-time 3D radar view
- System status metrics
- Active tracks list
- Detection table
- Performance charts

## Step 5: Explore the Features

### View Real-Time Data

The simulation starts automatically. You should see:
- Targets appearing in the 3D view
- Detections updating in the table
- Tracks being created and confirmed
- Data rate metrics updating

### Interact with the 3D View

- **Rotate**: Click and drag
- **Zoom**: Scroll wheel
- **Pan**: Right-click and drag
- **Hover**: Mouse over points to see details

### Check System Status

The status bar shows:
- Uptime
- Active radars (should show 3)
- Total detections (increasing)
- Active tracks
- Data rate (Hz)

### Monitor Performance

The performance chart shows:
- Blue line: Data rate over time
- Green line: Active track count

## Step 6: Explore the API

### Interactive API Documentation

Visit: **http://localhost:8000/docs**

Here you can:
- View all API endpoints
- Test endpoints directly
- See request/response schemas
- Explore data models

### Try Some API Calls

#### Get System Status
```bash
curl http://localhost:8000/api/status
```

#### Get Active Tracks
```bash
curl http://localhost:8000/api/tracks
```

#### Get Recent Detections
```bash
curl http://localhost:8000/api/detections?limit=10
```

#### Create a Dataset
```bash
curl -X POST "http://localhost:8000/api/datasets/create?name=Test&description=TestDataset&format=tabular"
```

## Step 7: Run Tests

To verify everything is working correctly:

```bash
# From workspace root
pytest
```

You should see all tests passing:
```
======================== test session starts =========================
collected XX items

tests/test_simulators.py ........
tests/test_normalizer.py .......
tests/test_tracker.py .......
tests/test_extractor.py ......
tests/test_api.py ........

======================== XX passed in X.XXs =========================
```

## Troubleshooting

### Backend won't start

**Error: Port 8000 already in use**
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python -m uvicorn radix.api.main:app --port 8001
```

**Error: Module not found**
```bash
# Make sure you're in the workspace directory
pwd

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't start

**Error: Port 3000 already in use**
```bash
# The frontend will automatically suggest another port
# Press 'y' to use it
```

**Error: Module not found**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### No data showing in GUI

**Check WebSocket connection**
- Look at the header - should show "Connected" in green
- Open browser console (F12) and check for errors
- Make sure backend is running on port 8000

**Refresh the page**
- Sometimes a simple refresh fixes connection issues
- Check browser console for WebSocket errors

### Tests failing

**Import errors**
```bash
# Make sure you're in the workspace root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

**Async warnings**
```bash
# Install pytest-asyncio
pip install pytest-asyncio
```

## Next Steps

### Customize Configuration

Edit `config.yaml` to:
- Add more targets
- Adjust radar parameters
- Change update intervals
- Modify radar locations

### Explore the Code

Key files to start with:
- `radix/api/main.py` - Backend entry point
- `frontend/src/App.jsx` - Frontend entry point
- `radix/simulators/` - Radar simulation logic
- `radix/core/` - Data processing engine

### Build Something Cool

Ideas to try:
1. **Add a new radar type**: Extend the simulator
2. **Custom visualization**: Modify the frontend
3. **ML pipeline**: Use the exported datasets
4. **Real radar integration**: Replace simulators with real data sources

## Common Tasks

### Stop the Services

**Backend**: Press `Ctrl+C` in the backend terminal

**Frontend**: Press `Ctrl+C` in the frontend terminal

### Restart with Fresh Data

```bash
# Remove the database
rm radix.db

# Restart the backend
python -m uvicorn radix.api.main:app --reload
```

### View Logs

**Backend logs**: Visible in the backend terminal

**Frontend logs**: Open browser console (F12)

### Export a Dataset

1. Let the system run for a minute to collect data
2. Go to http://localhost:8000/docs
3. Find `/api/datasets/create`
4. Click "Try it out"
5. Fill in parameters and execute
6. Use the returned `dataset_id` to export

### Check Performance

Monitor the performance chart in the GUI or check metrics:
```bash
curl http://localhost:8000/api/status | python -m json.tool
```

## Need Help?

- **API Documentation**: http://localhost:8000/docs
- **Architecture Guide**: See `ARCHITECTURE.md`
- **Full README**: See `README.md`
- **Test Examples**: Check `tests/` directory

---

## Summary

You should now have:
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ Real-time radar simulation active
- ✅ 3D visualization updating
- ✅ All tests passing

**Congratulations! RADIX is up and running!** 🎉

Start exploring the interface, try the API, and begin building your radar-based AI system!
