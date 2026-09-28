# Bookkeeper

Package that holds the logic for writing checkpoint registries to disk and removing old ones

## Accessing the Bookkeeper

Ya only need the `saveIndividualRegistry()` function from him, he handles the rest.

```python
from cali_pra.core.bookkeeper import saveIndividualRegistry
    
saveIndividualRegistry(currentPrinterState)
```

### saveIndividualRegistry()

Usage:

```python
registry_data = {
    "thing": "thing's value"
    "array": ['ba', 'ba', 'boei']
}

saveIndividualRegistry(registry_data)
```
