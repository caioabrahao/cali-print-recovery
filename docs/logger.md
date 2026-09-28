# Logger Util

Semantic utility for printing information in the terminal.

Logging levels can be enabled and disabled in the `config.toml`. Verbose option can be toggled.

```python
import cali_pra.console.logger as logger

logger.info("Establishing Connection"...)
logger.warn("Client Disconnected")
logger.error(f"Error {e}")

```

## Functions

### logger.title()

Use for cosmetic titles (probably only the initial app startup)

```python
    logger.title("Cali Print Recovery Bookkeeper Started")
```

### logger.info()

Displays information in blue relevant to the end user.

```python
    logger.info("Connection Established")
```

### logger.warn()

Show warnings in yellow relevant to the end user

```python
    logger.warn("Failed writing a registry! Retrying")
```

### logger.error()

Use for showing errors in red, relevant to the end user

```python
    logger.error("Fatal Crash! Sorry about that.")
```