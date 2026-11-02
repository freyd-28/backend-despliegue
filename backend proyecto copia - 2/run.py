import os
from src import create_app

# Render configurara FLASK_CONFIG=production.
# En local, si no defines la variable, se usa development.
app = create_app(os.getenv("FLASK_CONFIG", "development"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("DEBUG", "True").lower() in ("true", "1", "t", "yes", "on")

    print()
    print("=" * 50)
    print(" BilleterAPP API")
    print("=" * 50)
    print(f" Servidor: http://localhost:{port}")
    print(f" API:      http://localhost:{port}/api/v1")
    print(f" Debug:    {debug_mode}")
    print("=" * 50)
    print()

    app.run(host="0.0.0.0", port=port, debug=debug_mode)
