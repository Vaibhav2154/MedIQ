"""
STEP 7: Query Rewriting Engine

Removes denied fields from queries using sqlglot.
Enforces least privilege at runtime.
"""

from typing import List, Optional
import sqlglot
from sqlglot import exp


def rewrite_query(
    original_sql: str,
    allowed_fields: List[str]
) -> str:
    """
    Rewrite SQL query to include only allowed fields.
    
    STEP 7: Query Rewriting Engine
    
    Operations:
    1. Parse SQL query
    2. Extract selected columns
    3. Filter to allowed_fields
    4. Reconstruct and return SQL
    
    Example:
        Input:  SELECT name, aadhaar, age FROM patients
        Allowed: [age, gender]
        Output: SELECT age FROM patients
    
    Args:
        original_sql: Original SELECT query string
        allowed_fields: List of fields permitted for access
    
    Returns:
        str: Rewritten SQL query with only allowed fields
    
    Raises:
        ValueError: If query cannot be parsed
    """
    
    try:
        # Parse SQL query
        parsed = sqlglot.parse_one(original_sql, read="postgres")
        
        if not isinstance(parsed, exp.Select):
            raise ValueError("Query must be a SELECT statement")
        
        # Extract all selected columns (excluding *)
        selected_cols = []
        cols_to_remove = []
        
        for expr in parsed.expressions:
            if isinstance(expr, exp.Star):
                # SELECT * - need to expand to allowed fields
                selected_cols.append(None)  # Marker for SELECT *
            elif isinstance(expr, exp.Column):
                col_name = expr.name
                selected_cols.append(col_name)
                # Check if column is allowed
                if col_name not in allowed_fields:
                    cols_to_remove.append(col_name)
            elif isinstance(expr, exp.Alias):
                # Handle aliased columns
                col_name = expr.alias
                selected_cols.append(col_name)
                if col_name not in allowed_fields:
                    cols_to_remove.append(col_name)
            else:
                # Other expressions (functions, literals, etc.)
                col_name = expr.alias or str(expr)
                selected_cols.append(col_name)
        
        # If SELECT *, replace with allowed fields
        if None in selected_cols:
            new_expressions = [exp.column(f) for f in allowed_fields]
            parsed.set("expressions", new_expressions)
        else:
            # Remove disallowed columns
            new_expressions = []
            for expr in parsed.expressions:
                col_name = None
                if isinstance(expr, exp.Column):
                    col_name = expr.name
                elif isinstance(expr, exp.Alias):
                    col_name = expr.alias
                else:
                    col_name = expr.alias or str(expr)

                if col_name not in cols_to_remove:
                    new_expressions.append(expr)
            parsed.set("expressions", new_expressions)
        
        # Return rewritten SQL
        return parsed.sql(dialect="postgres")
    
    except Exception as e:
        raise ValueError(f"Failed to rewrite query: {str(e)}")


def extract_columns(sql: str) -> List[str]:
    """
    Extract all selected column names from a SELECT query.
    
    Args:
        sql: SQL query string
    
    Returns:
        List of column names
    """
    
    try:
        parsed = sqlglot.parse_one(sql, read="postgres")
        
        if not isinstance(parsed, exp.Select):
            return []
        
        columns = []
        for expr in parsed.expressions:
            if isinstance(expr, exp.Star):
                columns.append("*")
            elif isinstance(expr, exp.Column):
                columns.append(expr.name)
            elif isinstance(expr, exp.Alias):
                columns.append(expr.alias)
            else:
                columns.append(str(expr))
        
        return columns
    
    except Exception:
        return []


def add_field_filter(
    sql: str,
    field_name: str,
    value: str
) -> str:
    """
    Add a WHERE clause filter to a query.
    
    Args:
        sql: Original SELECT query
        field_name: Field name to filter on
        value: Value to match
    
    Returns:
        str: Modified SQL with WHERE clause
    """
    
    try:
        parsed = sqlglot.parse_one(sql, read="postgres")
        
        # Create new WHERE condition
        condition = exp.EQ(
            this=exp.column(field_name),
            expression=exp.Literal.string(value)
        )
        
        # Add to WHERE clause
        if parsed.args.get("where"):
            # Combine with existing WHERE using AND
            combined = exp.and_(parsed.args.get("where"), condition)
            parsed.set("where", combined)
        else:
            parsed.set("where", condition)
        
        return parsed.sql(dialect="postgres")
    
    except Exception as e:
        raise ValueError(f"Failed to add filter: {str(e)}")


def add_limit(sql: str, limit: int) -> str:
    """
    Add LIMIT clause to a query.
    
    Args:
        sql: Original SELECT query
        limit: Maximum number of rows
    
    Returns:
        str: Modified SQL with LIMIT clause
    """
    
    try:
        parsed = sqlglot.parse_one(sql, read="postgres")
        parsed.set("limit", exp.Limit(expression=exp.Literal.number(limit)))
        return parsed.sql(dialect="postgres")
    
    except Exception as e:
        raise ValueError(f"Failed to add limit: {str(e)}")


def validate_query(sql: str) -> bool:
    """
    Validate that a query is a valid SELECT statement.
    
    Args:
        sql: SQL query string
    
    Returns:
        bool: True if valid SELECT, False otherwise
    """
    
    try:
        parsed = sqlglot.parse_one(sql, read="postgres")
        return isinstance(parsed, exp.Select)
    except Exception:
        return False
