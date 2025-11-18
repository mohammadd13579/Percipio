Percipio
=========

### *Semantic data inference and transformation.*

`percipio` is the "anti-`pydantic`". Instead of validating data against a strict schema you define, `percipio` analyzes messy, real-world data and tells you *what it is* and *how to clean it*.

It moves beyond basic types (like `string`) to infer rich, semantic types (like `Email` or `Address`), and it doesn't just *validate* the data---it provides a one-line method to *transform* an entire messy column into clean, structured, and usable Python objects.

Core Problem
------------

You have a CSV with a column `data`:

```
["$5.00", "£20.50", "15.00 €", "¥1000", "invalid"]
```

What is this? How do you parse it? `percipio` solves this.

Installation
------------

```
pip install percipio.whl
```

Quickstart
----------

```
import percipio

# 1. Your messy data
data = ["$5.00", "£20.50", "15.00 €", "¥1000", "Not a price"]

# 2. Infer the semantic schema
# This analyzes the data and finds the best 'SemanticType'
schema = percipio.infer(data)

# 3. Inspect the results
print(f"Inferred Type: {schema.name}")
print(f"Confidence: {schema.confidence:.2f}%")
print(f"Total entries: {schema.stats.total_count}, Valid: {schema.stats.valid_count}")

# 4. Use the schema to clean & transform the data in one line
# The .clean() method is provided by the inferred SemanticType
clean_data = schema.clean(data)

# 5. Get structured, usable Python objects
for item in clean_data:
    print(item)
```

### Output:

```
Inferred Type: Currency
Confidence: 80.00%
Total entries: 5, Valid: 4
---
{'amount': 5.0, 'currency_symbol': '$', 'currency_code': 'USD', 'raw': '$5.00'}
{'amount': 20.5, 'currency_symbol': '£', 'currency_code': 'GBP', 'raw': '£20.50'}
{'amount': 15.0, 'currency_symbol': '€', 'currency_code': 'EUR', 'raw': '15.00 €'}
{'amount': 1000.0, 'currency_symbol': '¥', 'currency_code': 'JPY', 'raw': '¥1000'}
None
```

Features
--------

-   **Semantic Type Inference:** Goes beyond `int`, `str` to `Email`, `PhoneNumber`, `Currency`, `HttpUrl`, `PersonName`, `UKPostcode`, `GeoCoordinate`, etc.

-   **Hybrid Inference Engine:**

    -   **Level 1 (Regex/Rules):** Blazing-fast matching for common, strict types.

    -   **Level 2 (Statistical):** Analyzes patterns for "softer" types.

    -   **Level 3 (Generative):** (Optional) Uses generative models (like Gemini) to identify ambiguous types (`PersonName`) and *dynamically generate the parsing code*.

-   **One-Line Transformation:** The inferred `schema` object is not just a label; it's a *handler* with a `.clean()` method to parse the entire dataset.

-   **Fully Extensible:** Easily define and register your own custom semantic types.

See the `examples/` directory for more.
