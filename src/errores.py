# src/errores.py
"""Módulo de excepciones y errores específicos de la aplicación"""

class AppError(Exception):
    """Clase base para errores de la aplicación."""
    pass

# Errores de autenticación
class AuthError(AppError):
    """Errores relacionados con autenticación de usuarios."""
    pass

class MaxLoginAttemptsError(AuthError):
    """Excepción lanzada cuando se excede el número máximo de intentos de login."""
    pass

# Errores de clima
class ClimaError(AppError):
    """Errores relacionados con la consulta de clima."""
    pass

class CiudadNoEncontradaError(ClimaError):
    """Excepción lanzada cuando la ciudad consultada no existe en la API de clima."""
    pass

class ConexionClimaError(ClimaError):
    """Excepción lanzada ante un fallo de conexión o timeout en la API de clima."""
    pass

# Errores de IA
class IAError(AppError):
    """Errores relacionados con el servicio de IA (Gemini)."""
    pass

class ConexionIAError(IAError):
    """Excepción lanzada ante un fallo de conexión o respuesta inválida de la IA."""
    pass

# Errores de configuración/API keys
class APIKeyMissingError(AppError):
    """Excepción lanzada cuando falta la clave de API en el entorno."""
    pass