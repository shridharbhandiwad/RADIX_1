# Contributing to RADIX

Thank you for your interest in contributing to RADIX! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature/fix
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/yourusername/radix.git
cd radix

# Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Run tests to verify setup
pytest
```

## Development Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation changes
- `test/description` - Test additions/changes
- `refactor/description` - Code refactoring

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run all tests
   pytest
   
   # Run specific test
   pytest tests/test_simulators.py
   
   # Run with coverage
   pytest --cov=radix
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new radar type support"
   ```

### Commit Message Convention

Use conventional commits format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding/updating tests
- `refactor:` Code refactoring
- `style:` Code style changes (formatting)
- `perf:` Performance improvements
- `chore:` Maintenance tasks

Examples:
```
feat: add ISAR radar simulator
fix: correct doppler calculation in AESA
docs: update API documentation
test: add tests for normalizer
```

## Code Style

### Python

- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use docstrings for classes and functions

Example:
```python
def calculate_range(position: np.ndarray, radar_pos: np.ndarray) -> float:
    """
    Calculate range from radar to target.
    
    Args:
        position: Target position [x, y, z] in meters
        radar_pos: Radar position [x, y, z] in meters
    
    Returns:
        Range in meters
    """
    return np.linalg.norm(position - radar_pos)
```

### JavaScript/React

- Use functional components
- Use hooks for state management
- Use meaningful variable names
- Add PropTypes or TypeScript types

Example:
```javascript
function RadarDisplay({ detections, tracks, radars }) {
  // Component implementation
}
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Test edge cases and error conditions

### Test Structure

```python
class TestRadarSimulator:
    """Test radar simulator functionality"""
    
    def test_detection_generation(self):
        """Test that detections are generated correctly"""
        # Arrange
        simulator = create_simulator()
        target = create_target()
        
        # Act
        detection = simulator.generate_detection(target)
        
        # Assert
        assert detection is not None
        assert detection.range_m > 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_simulators.py

# Run with coverage report
pytest --cov=radix --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Adding New Features

### Adding a New Radar Type

1. **Create simulator class**
   ```python
   # radix/simulators/new_radar_simulator.py
   from .base import RadarSimulator
   
   class NewRadarSimulator(RadarSimulator):
       def generate_detection(self, target, timestamp):
           # Implementation
           pass
   ```

2. **Add to RadarType enum**
   ```python
   # radix/models/schemas.py
   class RadarType(str, Enum):
       # ... existing types
       NEW_RADAR = "NEW_RADAR"
   ```

3. **Add normalization logic**
   ```python
   # radix/core/normalizer.py
   def _normalize_new_radar(self, raw):
       # Implementation
       pass
   ```

4. **Add tests**
   ```python
   # tests/test_simulators.py
   class TestNewRadarSimulator:
       def test_creation(self):
           # Test implementation
           pass
   ```

5. **Update documentation**
   - Add to README.md
   - Update ARCHITECTURE.md
   - Add usage examples

### Adding New API Endpoints

1. **Add endpoint to main.py**
   ```python
   @app.get("/api/new-endpoint")
   async def new_endpoint():
       # Implementation
       return {"status": "ok"}
   ```

2. **Add tests**
   ```python
   # tests/test_api.py
   def test_new_endpoint():
       response = client.get("/api/new-endpoint")
       assert response.status_code == 200
   ```

3. **Update API documentation**
   - Add docstring to endpoint
   - Update README.md

## Documentation

### Code Documentation

- Add docstrings to all public classes and methods
- Use Google style docstrings
- Include examples where helpful

### README Updates

When adding features:
- Update feature list
- Add usage examples
- Update API reference if needed

### Architecture Documentation

For significant changes:
- Update ARCHITECTURE.md
- Explain design decisions
- Document new patterns

## Pull Request Process

1. **Before submitting**
   - Run all tests and ensure they pass
   - Update documentation
   - Add/update tests for your changes
   - Rebase on latest main branch

2. **PR Description**
   - Clearly describe the changes
   - Reference any related issues
   - Include screenshots for UI changes
   - List breaking changes if any

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Testing
   - [ ] All existing tests pass
   - [ ] New tests added
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)
   ```

4. **Review Process**
   - Address review comments
   - Update PR as needed
   - Maintain a positive attitude

## Issue Reporting

### Bug Reports

Include:
- Clear, descriptive title
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or screenshots

### Feature Requests

Include:
- Clear description of the feature
- Use case / motivation
- Proposed implementation (if any)
- Alternatives considered

## Project Structure

```
workspace/
├── radix/              # Core package
│   ├── api/           # FastAPI backend
│   ├── core/          # Processing engine
│   ├── models/        # Data schemas
│   └── simulators/    # Radar simulators
├── frontend/          # React frontend
│   └── src/
│       └── components/
├── tests/             # Test suite
├── docs/              # Documentation
└── scripts/           # Utility scripts
```

## Getting Help

- Check existing issues and documentation
- Ask questions in GitHub Discussions
- Review test files for usage examples
- Refer to ARCHITECTURE.md for design details

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to RADIX!
