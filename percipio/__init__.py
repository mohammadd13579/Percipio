"""
percipio - Semantic data inference and transformation.

(from Latin: "to grasp, to understand, to perceive")

Usage:
    import percipio
    
    data = ["$5.00", "£20.50", "15.00 €"]
    schema = percipio.infer(data)
    
    print(schema.name)
    # Output: Currency
    
    clean_data = schema.clean(data)
    # Output: [
    #   {'amount': 5.0, ...},
    #   {'amount': 20.5, ...},
    #   {'amount': 15.0, ...}
    # ]
"""

# Public API
from .core import infer
from .types import register_type, BaseSemanticType, SemanticTypeStats
from . import built_in_types # This import triggers registration of built-in types

__version__ = "0.1.0"
__all__ = [
    "infer", 
    "register_type", 
    "BaseSemanticType", 
    "SemanticTypeStats"
]

print("percipio: Registered built-in types.")
