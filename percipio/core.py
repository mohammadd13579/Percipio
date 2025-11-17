from .types import get_registered_types, BaseSemanticType, SemanticTypeStats
from typing import List, Any, Optional

# A cache for inference results could be added here
INFERENCE_CACHE = {}

def infer(data: List[Any], engine: str = 'default') -> BaseSemanticType:
    """
    Infers the semantic type of a list of data.

    This function analyzes the data against all registered SemanticTypes
    and returns an instance of the *best matching* type, complete with
    statistics about the match.

    Args:
        data: A list of data points (e.g., a CSV column).
        engine: The inference engine to use ('default', 'llm').
                'llm' is reserved for generative-powered inference.

    Returns:
        An *instance* of the best-matching BaseSemanticType subclass,
        which includes match statistics and a .clean() method.
    """
    if not data:
        raise ValueError("Cannot infer type from empty data list.")

    best_type_class = None
    best_score = -1.0
    best_stats = None

    # Get all registered types (from types.py and built_in_types.py)
    registered_types = get_registered_types()
    
    if not registered_types:
        raise ImportError("No semantic types are registered. Did percipio.built_in_types fail to import?")

    total_count = len(data)

    for TypeClass in registered_types:
        valid_count = 0
        
        # Level 1 & 2: Use the type's built-in validation
        try:
            for item in data:
                if TypeClass.validate_item(item):
                    valid_count += 1
        except Exception:
            # Validation function might fail on weird data
            continue 

        if total_count == 0: continue
        
        # Calculate a confidence score
        # This is a simple ratio, but could be a complex heuristic
        confidence = (valid_count / total_count)
        
        # Apply a 'specificity' bonus (defined on the type class)
        # This helps 'Email' (specificity=0.8) win against 'String' (specificity=0.1)
        # when all data points are valid emails.
        score = confidence * TypeClass.specificity

        if score > best_score:
            best_score = score
            best_type_class = TypeClass
            best_stats = SemanticTypeStats(
                total_count=total_count,
                valid_count=valid_count,
                invalid_count=total_count - valid_count,
                confidence=confidence
            )
            
    # Level 3: Generative AI Inference (The "Show-Off" Part)
    # If confidence is low and engine='llm', we could query a
    # generative model to get a "dynamic" type.
    if engine == 'llm' and best_stats.confidence < 0.5:
        print("Default engine confidence is low. Trying 'llm' engine...")
        # from .llm_engine import infer_dynamic_type
        # llm_type_class, llm_stats = infer_dynamic_type(data)
        # if llm_type_class and llm_stats.confidence > best_stats.confidence:
        #     return llm_type_class(stats=llm_stats)
        # This is a placeholder for the advanced functionality.
        pass

    if best_type_class is None:
        raise TypeError("Could not infer any semantic type for the data.")

    # Return an *instance* of the winning class, passing in the stats
    return best_type_class(stats=best_stats)
