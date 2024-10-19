from src.web import create_app

app = create_app()
app.testing = True

client = app.test_client()


def test_404_error_handler():
    """Test error handler for page not found error (404)"""
    response = client.get("/noexiste")

    assert 404 == response.status_code
    assert b'<div class="error-code">404</div>' in response.data
    assert b'<div class="error-message">No encontrado</div>' in response.data
    assert b'<div class="error-details">La URL solicitada no se encuentra en el servidor.</div>' in response.data
