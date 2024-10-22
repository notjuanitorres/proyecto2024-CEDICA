from minio import Minio


class Storage:
    """
    A class to handle storage operations using Minio.

    Attributes:
        __client (Minio): The Minio client instance.

    Methods:
        init_app(app):
            Initialize the storage with the given Flask app configuration.
        client:
            Get the Minio client instance.
        client(value):
            Set the Minio client instance.
    """
    def __init__(self, app=None):
        """
        Initialize the Storage class.

        Args:
            app (Flask, optional): The Flask application instance.
            If provided, the storage will be initialized with the given app configuration.
        """
        self.__client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialize the storage with the given Flask app configuration.

        Args:
            app (Flask): The Flask application instance.

        Returns:
            Flask: The Flask application instance with storage initialized.
        """
        minio_server = app.config.get("MINIO_SERVER")
        access_key = app.config.get("MINIO_ACCESS_KEY")
        secret_key = app.config.get("MINIO_SECRET_KEY")
        secure = app.config.get("MINIO_SECURE", False)

        self.__client = Minio(
            endpoint=minio_server, access_key=access_key, secret_key=secret_key, secure=secure
        )

        app.storage = self

        return app

    @property
    def client(self):
        """
        Get the Minio client instance.

        Returns:
            Minio: The Minio client instance.
        """
        return self.__client

    @client.setter
    def client(self, value):
        """
        Set the Minio client instance.

        Args:
            value (Minio): The Minio client instance.
        """
        self.__client = value


storage = Storage()
