import re
from typing import List, Any, Dict, Optional, Type, Callable, Set

# --- Globals ---
# This registry holds all 'discoverable' semantic types
TYPE_REGISTRY: Dict[str, Type["BaseSemanticType"]] = {}


def register_type(cls: Type["BaseSemanticType"]) -> Type["BaseSemanticType"]:
    """
    A class decorator to register a new semantic type
    with the 'percipio' inference engine.
    
    Usage:
        @register_type
        class MyCustomType(BaseSemanticType):
            ...
    """
    name = cls.name
    if not name:
        raise ValueError("SemanticType class must have a 'name' attribute.")
    if name in TYPE_REGISTRY:
        raise ValueError(f"Type '{name}' is already registered.")
    
    TYPE_REGISTRY[name] = cls
    return cls

def get_registered_types() -> List[Type["BaseSemanticType"]]:
    """Returns a list of all registered type classes."""
    return list(TYPE_REGISTRY.values())

# --- Data Structures ---

class SemanticTypeStats:
    """A simple data class to hold inference statistics."""
    def __init__(self, total_count=0, valid_count=0, invalid_count=0, confidence=0.0):
        self.total_count = total_count
        self.valid_count = valid_count
        self.invalid_count = invalid_count
        self.confidence = confidence # The raw % of valid items
    
    def __repr__(self):
        return (f"SemanticTypeStats(total={self.total_count}, "
                f"valid={self.valid_count}, confidence={self.confidence:.2f})")

# --- Base Class ---

class BaseSemanticType:
    """
    The base class for all semantic types.
    
    To create a new type, subclass this and:
    1. Set the 'name' attribute.
    2. Set the 'specificity' (0.0 to 1.0).
    3. Override the 'validate_item' static method.
    4. Override the '_clean_item' instance method.
    """
    
    # --- Class Attributes for Inference ---
    
    # The unique, human-readable name for this type
    name: str = "Base"
    
    # A score from 0.0 (generic) to 1.0 (highly specific).
    # 'String' has 0.1, 'Email' has 0.8. This breaks ties.
    specificity: float = 0.0
    
    # Optional: A pre-compiled regex for fast Level 1 checks.
    regex: Optional[re.Pattern] = None

    # --- Instance Attributes ---
    
    def __init__(self, stats: Optional[SemanticTypeStats] = None):
        """
        An instance of a SemanticType is a "handler" for that type.
        It is initialized with the stats from the inference process.
        """
        self.stats = stats or SemanticTypeStats()

    def __repr__(self):
        return f"<SemanticType: {self.name} (stats={self.stats})>"

    # --- Core API ---
    
    @classmethod
    def validate_item(cls, item: Any) -> bool:
        """
        [Level 1/2 Inference]
        A fast, class-level check to see if a single item
        *could* belong to this type.
        
        This method MUST be overridden by subclasses.
        """
        raise NotImplementedError
    
    def _clean_item(self, item: Any) -> Optional[Any]:
        """
        [Transform]
        The instance-level logic for parsing and cleaning a
        single item *that is assumed to be of this type*.
        
        Returns a structured object (e.g., a dict) or None if
        parsing fails.
        
        This method MUST be overridden by subclasses.
        """
        raise NotImplementedError

    def clean(self, data: List[Any]) -> List[Optional[Any]]:
        """
        The main public transformation API.
        
        It iterates over a list, attempts to clean each item
        using the type's specific logic, and returns a list
        of structured objects or Nones.
        """
        return [self._clean_item(item) for item in data]
