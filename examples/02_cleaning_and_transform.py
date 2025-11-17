import percipio
import json # for pretty printing

# --- Example: Messy Currency Data ---
print("--- Example: Currency Cleaning ---")
data = ["$5.00", "£20.50", "15.00 €", "¥1000", "invalid data", " $1,200.00 "]
schema = percipio.infer(data)

print(f"Inferred Type: {schema.name}")
print(f"Valid: {schema.stats.valid_count} / {schema.stats.total_count}\n")

# Now, use the inferred schema to clean the *entire* list
# The .clean() method is provided by the CurrencyType handler
print("--- Cleaning & Transforming Data ---")
clean_data = schema.clean(data)

# The result is a list of structured Python dictionaries
for item in clean_data:
    if item:
        # Pretty print the structured dictionary
        print(json.dumps(item, indent=2))
    else:
        # The 'invalid data' entry becomes None
        print(None)
