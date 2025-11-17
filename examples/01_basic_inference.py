import percipio

# --- Example 1: A list of emails and junk ---
print("--- Example 1: Emails ---")
data = ["test@example.com", "user.name@google.com", "not-an-email", "gemini@ai.dev"]
schema = percipio.infer(data)

print(f"Inferred Type: {schema.name}")
print(f"Confidence: {schema.stats.confidence * 100:.2f}%")
print(f"Valid: {schema.stats.valid_count} / {schema.stats.total_count}")
print("-" * 20)


# --- Example 2: A list of integers ---
print("\n--- Example 2: Integers ---")
data = ["123", 456, "789", "invalid", 10]
schema = percipio.infer(data)

print(f"Inferred Type: {schema.name}")
print(f"Confidence: {schema.stats.confidence * 100:.2f}%")
print(f"Valid: {schema.stats.valid_count} / {schema.stats.total_count}")
print("-" * 20)
