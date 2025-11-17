import percipio
import re

# --- Problem: 'percipio' doesn't know our company's Employee ID format ---
print("--- Running inference with standard types ---")
data = ["EMP-12345", "EMP-54321", "Not an ID", "USER-999"]
try:
    schema = percipio.infer(data)
    # This will probably be inferred as 'String'
    print(f"Standard inference: {schema.name}\n")
except Exception as e:
    print(f"Could not infer type: {e}\n")


# --- Solution: Define and register our own SemanticType ---

# Use the @register_type decorator
@percipio.register_type
class EmployeeIDType(percipio.BaseSemanticType):
    """Matches our custom Employee ID format: EMP-XXXXX"""
    
    # 1. Set the name and specificity
    name: str = "EmployeeID"
    specificity: float = 0.9 # Very specific!
    
    # 2. Add a regex for fast validation
    regex: re.Pattern = re.compile(r"^EMP-\d{5}$")
    
    # 3. Implement the class-level validation
    @classmethod
    def validate_item(cls, item: any) -> bool:
        return isinstance(item, str) and bool(cls.regex.match(item))
        
    # 4. Implement the instance-level cleaning
    def _clean_item(self, item: any) -> dict | None:
        if not self.validate_item(item):
            return None
        
        # Transform the string into a structured dict
        id_num = int(item.split('-')[1])
        return {
            "prefix": "EMP",
            "id_number": id_num,
            "raw": item
        }

print("--- Rerunning inference with *custom* type registered ---")
# Now, percipio.infer() will automatically find and use our new type
custom_schema = percipio.infer(data)

print(f"New Inferred Type: {custom_schema.name}") # Success!
print(f"Confidence: {custom_schema.stats.confidence * 100:.2f}%")
print(f"Valid: {custom_schema.stats.valid_count} / {custom_schema.stats.total_count}\n")

# And we can use its .clean() method just like a built-in type
print("--- Cleaning with custom type ---")
clean_ids = custom_schema.clean(data)
for item in clean_ids:
    print(item)
