"""
IBM Cloud Object Storage Service
Handles file storage and retrieval from IBM COS
"""
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import ibm_boto3
from ibm_botocore.client import Config
from app.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """IBM Cloud Object Storage client wrapper"""
    
    def __init__(self):
        """Initialize IBM COS client"""
        self.client = ibm_boto3.client(
            "s3",
            ibm_api_key_id=settings.ibm_cos_api_key,
            ibm_service_instance_id=settings.ibm_cos_instance_crn,
            config=Config(signature_version="oauth"),
            endpoint_url=settings.ibm_cos_endpoint
        )
        self.bucket_name = settings.ibm_cos_bucket_name
        logger.info(f"Initialized IBM COS client for bucket: {self.bucket_name}")
    
    def upload_file(self, file_path: str, object_key: str) -> str:
        """
        Upload a file to IBM Cloud Object Storage
        
        Args:
            file_path: Local path to the file
            object_key: Key (path) in the bucket
            
        Returns:
            Object URL
        """
        try:
            with open(file_path, 'rb') as file_data:
                self.client.upload_fileobj(
                    Fileobj=file_data,
                    Bucket=self.bucket_name,
                    Key=object_key
                )
            
            url = f"{settings.ibm_cos_endpoint}/{self.bucket_name}/{object_key}"
            logger.info(f"Uploaded file to: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Error uploading file to COS: {e}")
            raise
    
    def download_file(self, object_key: str, local_path: str) -> str:
        """
        Download a file from IBM Cloud Object Storage
        
        Args:
            object_key: Key (path) in the bucket
            local_path: Local path to save the file
            
        Returns:
            Local file path
        """
        try:
            self.client.download_file(
                Bucket=self.bucket_name,
                Key=object_key,
                Filename=local_path
            )
            logger.info(f"Downloaded file from {object_key} to {local_path}")
            return local_path
            
        except Exception as e:
            logger.error(f"Error downloading file from COS: {e}")
            raise
    
    def upload_json(self, data: Dict[Any, Any], object_key: str) -> str:
        """
        Upload JSON data to IBM Cloud Object Storage
        
        Args:
            data: Dictionary to serialize as JSON
            object_key: Key (path) in the bucket
            
        Returns:
            Object URL
        """
        try:
            json_data = json.dumps(data, indent=2, default=str)
            
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=json_data.encode('utf-8'),
                ContentType='application/json'
            )
            
            url = f"{settings.ibm_cos_endpoint}/{self.bucket_name}/{object_key}"
            logger.info(f"Uploaded JSON to: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Error uploading JSON to COS: {e}")
            raise
    
    def download_json(self, object_key: str) -> Dict[Any, Any]:
        """
        Download and parse JSON from IBM Cloud Object Storage
        
        Args:
            object_key: Key (path) in the bucket
            
        Returns:
            Parsed JSON data
        """
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            
            json_data = response['Body'].read().decode('utf-8')
            data = json.loads(json_data)
            logger.info(f"Downloaded JSON from: {object_key}")
            return data
            
        except Exception as e:
            logger.error(f"Error downloading JSON from COS: {e}")
            raise
    
    def list_objects(self, prefix: str = "") -> list:
        """
        List objects in the bucket with optional prefix
        
        Args:
            prefix: Object key prefix to filter by
            
        Returns:
            List of object keys
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            objects = []
            if 'Contents' in response:
                objects = [obj['Key'] for obj in response['Contents']]
            
            logger.info(f"Listed {len(objects)} objects with prefix: {prefix}")
            return objects
            
        except Exception as e:
            logger.error(f"Error listing objects in COS: {e}")
            raise
    
    def delete_object(self, object_key: str) -> bool:
        """
        Delete an object from the bucket
        
        Args:
            object_key: Key (path) in the bucket
            
        Returns:
            True if successful
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            logger.info(f"Deleted object: {object_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting object from COS: {e}")
            raise
    
    def object_exists(self, object_key: str) -> bool:
        """
        Check if an object exists in the bucket
        
        Args:
            object_key: Key (path) in the bucket
            
        Returns:
            True if object exists
        """
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return True
        except:
            return False


# Singleton instance
_storage_service: Optional[StorageService] = None


def get_storage_service() -> StorageService:
    """Get or create the storage service singleton"""
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service

# Made with Bob
