"""
Enterprise Data Governance Portal - Backend API
FastAPI + Databricks SQL Connector
"""
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import logging

# Databricks SQL Connector
try:
    from databricks import sql
    DATABRICKS_AVAILABLE = True
except ImportError:
    DATABRICKS_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_databricks_connection():
    """Get Databricks SQL connection"""
    if not DATABRICKS_AVAILABLE:
        raise HTTPException(status_code=500, detail="Databricks connector not available")
    
    # Get credentials from environment
    server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    token = os.getenv("DATABRICKS_TOKEN")
    
    # Validate credentials
    if not all([server_hostname, http_path, token]):
        missing = []
        if not server_hostname: missing.append("DATABRICKS_SERVER_HOSTNAME")
        if not http_path: missing.append("DATABRICKS_HTTP_PATH")
        if not token: missing.append("DATABRICKS_TOKEN")
        raise HTTPException(
            status_code=500, 
            detail=f"Missing environment variables: {', '.join(missing)}"
        )
    
    try:
        connection = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=token
        )
        return connection
    except Exception as e:
        logger.error(f"Connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")

def execute_query(query: str) -> List[Dict[str, Any]]:
    """Execute SQL query and return results"""
    connection = get_databricks_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]
        cursor.close()
        connection.close()
        return result
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

class TableMetadata(BaseModel):
    catalog: str
    schema: str
    table_name: str
    table_type: str
    description: Optional[str]
    missing_description: bool

class ColumnMetadata(BaseModel):
    column_name: str
    data_type: str
    is_nullable: str
    description: Optional[str]

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    databricks_connected: bool

async def health_check():
    """Health check endpoint"""
    databricks_connected = False
    try:
        connection = get_databricks_connection()
        connection.close()
        databricks_connected = True
    except:
        pass
    
    return HealthResponse(
        status="healthy" if databricks_connected else "degraded",
        timestamp=datetime.now().isoformat(),
        databricks_connected=databricks_connected
    )

async def get_inventory():
    """Get Unity Catalog inventory"""
    try:
        query = """
        SELECT 
            table_catalog as catalog,
            table_schema as schema,
            table_name,
            table_type,
            comment as description,
            CASE WHEN comment IS NULL OR TRIM(comment) = '' THEN true ELSE false END as missing_description
        FROM system.information_schema.tables
        WHERE table_catalog NOT IN ('system', 'information_schema')
        ORDER BY table_catalog, table_schema, table_name
        """
        result = execute_query(query)
        total = len(result)
        missing = sum(1 for r in result if r['missing_description'])
        
        return {
            "total_table": total,
            "missing_description_count": missing,
            "documentation_score": round((total - missing) / total * 100, 2) if total > 0 else 0,
            "catalog_list": sorted(list(set(r['catalog'] for r in result))),
            "table_list": result
        }
    except Exception as e:
        logger.error(f"Inventory error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_lineage(catalog: str, schema: str, table: str):
    """Get table column metadata"""
    try:
        query = f"""
        SELECT column_name, data_type, is_nullable, comment as description
        FROM system.information_schema.columns
        WHERE table_catalog = '{catalog}' AND table_schema = '{schema}' AND table_name = '{table}'
        ORDER BY ordinal_position
        """
        result = execute_query(query)
        return {"catalog": catalog, "schema": schema, "table": table, "column_list": result}
    except Exception as e:
        logger.error(f"Lineage error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def root():
    return {"message": "Data Governance API", "version": "1.0.0"}
