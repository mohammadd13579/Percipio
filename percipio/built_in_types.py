"""
This module defines the built-in SemanticTypes for percipio.
Importing this module (which __init__.py does) will automatically
register them with the inference engine.
"""

import re
from .types import BaseSemanticType, register_type
from typing import Any, Optional, Dict

# --- Base Generic Types ---

@register_type
class StringType(BaseSemanticType):
    """The most generic type. Matches any string."""
    name: str = "String"
    specificity: float = 0.1 # Very low, a "catch-all"
    
    @classmethod
    def validate_item(cls, item: Any) -> bool:
        return isinstance(item, str)
        
    def _clean_item(self, item: Any) -> Optional[str]:
        if isinstance(item, str):
            return item.strip()
        return None

@register_type
class IntegerType(BaseSemanticType):
    """Matches integers, including as strings."""
    name: str = "Integer"
    specificity: float = 0.5
    
    @classmethod
    def validate_item(cls, item: Any) -> bool:
        if isinstance(item, int):
            return True
        if isinstance(item, str):
            return item.strip().isdigit()
        return False
        
    def _clean_item(self, item: Any) -> Optional[int]:
        try:
            return int(item)
        except (ValueError, TypeError):
            return None

# --- Specific Semantic Types ---

@register_type
class EmailType(BaseSemanticType):
    """Matches email addresses."""
    name: str = "Email"
    specificity: float = 0.8 # High specificity
    # A simple but effective regex for validation
    regex: re.Pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    
    @classmethod
    def validate_item(cls, item: Any) -> bool:
        return isinstance(item, str) and bool(cls.regex.match(item))
        
    def _clean_item(self, item: Any) -> Optional[Dict[str, str]]:
        if not self.validate_item(item):
            return None
        
        username, domain = item.strip().lower().split('@')
        return {
            "username": username,
            "domain": domain,
            "raw": item
        }

@register_type
class CurrencyType(BaseSemanticType):
    """
    Matches currency strings like "$5.00", "£20.50", "15.00 €", "¥1000".
    This is a great example of a complex semantic type.
    """
    name: str = "Currency"
    specificity: float = 0.7
    
    # Regex to find currency symbols and amounts
    # It allows symbols before or after, and handles commas.
    regex: re.Pattern = re.compile(
        r"^(?P<symbol>[$\£\€\¥])?\s*(?P<amount>[\d,]+(?:\.\d{1,2})?)\s*(?P<symbol_post>[$\£\€\¥])?$"
    )
    
    # Mapping of symbols to standard codes
    SYMBOL_MAP = {
        "$": "USD",
        "£": "GBP",
        "€": "EUR",
        "¥": "JPY",
    }
    
    @classmethod
    def validate_item(cls, item: Any) -> bool:
        return isinstance(item, str) and bool(cls.regex.match(item.strip()))
        
    def _clean_item(self, item: Any) -> Optional[Dict[str, Any]]:
        if not isinstance(item, str):
            return None
            
        match = self.regex.match(item.strip())
        if not match:
            return None
        
        try:
            parts = match.groupdict()
            symbol = parts.get("symbol") or parts.get("symbol_post")
            amount_str = parts.get("amount", "0").replace(",", "")
            amount_float = float(amount_str)
            
            return {
                "amount": amount_float,
                "currency_symbol": symbol,
                "currency_code": self.SYMBOL_MAP.get(symbol, "UNKNOWN"),
                "raw": item
            }
        except (ValueError, TypeError):
            return None
