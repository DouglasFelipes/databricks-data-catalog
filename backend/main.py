"""
Enterprise Data Governance Portal - Backend API
FastAPI + Databricks SQL Connector
Real Unity Catalog Integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
    logging.warning("Databricks SQL Connector not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Enterprise Data Governance API",
    description="Real-time Unity Catalog metadata API",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATABRICKS CONNECTION
# ============================================================================

def get_databricks_connection():
    """Get Databricks SQL connection"""
    if not DATABRICKS_AVAILABLE:
        raise HTTPException(status_code=500, detail="Databricks connector not available")
    
    try:
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME", os.getenv("DATABRICKS_HOST")),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        return connection
    except Exception as e:
        logger.error(f"Connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

def execute_query(query: str) -> List[Dict[str, Any]]:
    """Execute SQL query and return results as list of dicts"""
    connection = get_databricks_connection()
    
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Fetch all rows and convert to list of dicts
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]
        
        cursor.close()
        connection.close()
        
        return result
    except Exception as e:
        logger.error(f"Query execution error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

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
    ordinal_position: int

class InventoryResponse(BaseModel):
    total_table: int
    missing_description_count: int
    documentation_score: float
    catalog_list: List[str]
    table_list: List[TableMetadata]

class LineageResponse(BaseModel):
    catalog: str
    schema: str
    table: str
    column_list: List[ColumnMetadata]

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    databricks_connected: bool

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/api/health", response_model=HealthResponse)
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


@app.get("/api/inventory", response_model=InventoryResponse)
async def get_inventory():
    """
    Get complete inventory of Unity Catalog tables
    Returns: All tables with metadata and quality metrics
    """
    try:
        # Query with calculated missing_description in SQL
        query = """
        SELECT 
            table_catalog as catalog,
            table_schema as schema,
            table_name,
            table_type,
            comment as description,
            CASE 
                WHEN comment IS NULL OR TRIM(comment) = '' THEN true 
                ELSE false 
            END as missing_description
        FROM system.information_schema.tables
        WHERE table_catalog NOT IN ('system', 'information_schema')
        ORDER BY table_catalog, table_schema, table_name
        """
        
        result = execute_query(query)
        
        # Calculate metrics
        total_table = len(result)
        missing_description_count = sum(1 for row in result if row['missing_description'])
        documentation_score = round(
            ((total_table - missing_description_count) / total_table * 100) if total_table > 0 else 0,
            2
        )
        
        # Get unique catalogs
        catalog_list = sorted(list(set(row['catalog'] for row in result)))
        
        # Convert to TableMetadata objects
        table_list = [
            TableMetadata(
                catalog=row['catalog'],
                schema=row['schema'],
                table_name=row['table_name'],
                table_type=row['table_type'],
                description=row['description'],
                missing_description=row['missing_description']
            )
            for row in result
        ]
        
        return InventoryResponse(
            total_table=total_table,
            missing_description_count=missing_description_count,
            documentation_score=documentation_score,
            catalog_list=catalog_list,
            table_list=table_list
        )
    
    except Exception as e:
        logger.error(f"Inventory error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/lineage/{catalog}/{schema}/{table}", response_model=LineageResponse)
async def get_lineage(catalog: str, schema: str, table: str):
    """
    Get column lineage for a specific table
    Returns: Column metadata including types and descriptions
    """
    try:
        query = f"""
        SELECT 
            column_name,
            data_type,
            is_nullable,
            comment as description,
            ordinal_position
        FROM system.information_schema.columns
        WHERE table_catalog = '{catalog}'
        AND table_schema = '{schema}'
        AND table_name = '{table}'
        ORDER BY ordinal_position
        """
        
        result = execute_query(query)
        
        column_list = [
            ColumnMetadata(
                column_name=row['column_name'],
                data_type=row['data_type'],
                is_nullable=row['is_nullable'],
                description=row['description'],
                ordinal_position=row['ordinal_position']
            )
            for row in result
        ]
        
        return LineageResponse(
            catalog=catalog,
            schema=schema,
            table=table,
            column_list=column_list
        )
    
    except Exception as e:
        logger.error(f"Lineage error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/catalog/{catalog}/schema")
async def get_schema_list(catalog: str):
    """Get list of schemas in a catalog"""
    try:
        query = f"""
        SELECT DISTINCT table_schema as schema
        FROM system.information_schema.tables
        WHERE table_catalog = '{catalog}'
        ORDER BY table_schema
        """
        
        result = execute_query(query)
        return {"catalog": catalog, "schema_list": [row['schema'] for row in result]}
    
    except Exception as e:
        logger.error(f"Schema list error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/catalog/{catalog}/schema/{schema}/table")
async def get_table_list(catalog: str, schema: str):
    """Get list of tables in a schema"""
    try:
        query = f"""
        SELECT 
            table_name,
            table_type,
            comment as description
        FROM system.information_schema.tables
        WHERE table_catalog = '{catalog}'
        AND table_schema = '{schema}'
        ORDER BY table_name
        """
        
        result = execute_query(query)
        return {
            "catalog": catalog,
            "schema": schema,
            "table_list": result
        }
    
    except Exception as e:
        logger.error(f"Table list error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Enterprise Data Governance API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "inventory": "/api/inventory",
            "lineage": "/api/lineage/{catalog}/{schema}/{table}",
            "schemas": "/api/catalog/{catalog}/schema",
            "tables": "/api/catalog/{catalog}/schema/{schema}/table"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
