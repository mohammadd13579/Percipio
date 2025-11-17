"""
This is a conceptual example showing how 'percipio'
would be used with pandas.
(This requires pandas to be installed: pip install pandas)
"""

try:
    import pandas as pd
    import percipio
    import json
    import re

    # 1. Create a messy DataFrame
    data = {
        "user": ["test@example.com", "user@google.com", "not-an-email"],
        "id_code": ["EMP-12345", "EMP-54321", "INVALID"],
        "transaction": ["$5.00", "£20.50", "1,200.00 €"]
    }
    df = pd.DataFrame(data)
    print("--- Original Messy DataFrame ---")
    print(df)
    print("\n")

    # 2. Use 'percipio.infer' on each column
    # (Here we manually register the custom type from example 3)
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

    # 3. Infer the schema for the entire DataFrame
    print("--- Inferring DataFrame Schema ---")
    # In a real version, `percipio.infer` might take a DataFrame directly.
    # For now, we do it column by column.
    schema_report = {}
    for col in df.columns:
        schema_report[col] = percipio.infer(df[col].tolist())
    
    for col, schema in schema_report.items():
        print(f"Column '{col}': Inferred Type = {schema.name} (Confidence: {schema.stats.confidence*100:.0f}%)")

    # 4. Create a new, clean DataFrame
    print("\n--- Creating Cleaned DataFrame ---")
    clean_df = pd.DataFrame()
    for col, schema in schema_report.items():
        # Use the inferred schema's .clean() method for each column
        clean_df[f"clean_{col}"] = schema.clean(df[col].tolist())

    print(clean_df)
    print("\n--- Data in 'clean_transaction' column ---")
    
    # The 'clean_transaction' column now contains structured dicts
    for item in clean_df['clean_transaction']:
        print(json.dumps(item, indent=2))

except ImportError:
    print("Pandas not found. Skipping example 04.")
    print("Please run 'pip install pandas' to run this example.")
