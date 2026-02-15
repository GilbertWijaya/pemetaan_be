"""Test the Flask application"""


def test_app_creation(app):
    """Test that the app is created properly"""
    assert app is not None
    assert app.config['TESTING'] is True


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'message' in data
