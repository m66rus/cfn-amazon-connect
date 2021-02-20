import cfcrhelper
import logging
import boto3

# Setup logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create(event, context):
    # Cloudformation Create resource step
    
    response_status = "SUCCESS"
    physical_resource_id = '89197905-bb40-4cba-bfd5-b1f99d04ebbe'
    response_data = {"Message": "Resource update successful!"}
    
    return response_status, physical_resource_id, response_data 
    
def update(event, context):
    # Cloudformation Update resource step
    #["ResourceProperties"] current properties
    #["OldResourceProperties"] previous values
    response_status = "SUCCESS"
    physical_resource_id = '89197905-bb40-4cba-bfd5-b1f99d04ebbe'
    response_data = {"Message": "Resource update successful!"}
    
    return response_status, physical_resource_id, response_data

def delete(event, context):
    # Cloudformation Delete resource step
  
    response_status = "SUCCESS"
    physical_resource_id = '89197905-bb40-4cba-bfd5-b1f99d04ebbe'
    response_data = {"Message": "Resource update successful!"}
    
    return response_status, physical_resource_id, response_data    

def handler(event, context):
    """
    Main handler function, passes off it's work to crhelper's cfn_handler
    """
    # update the logger with event info
    #["ResourceProperties"] current properties
    #["OldResourceProperties"] previous values
    
  
    return cfcrhelper.cr_handler(event, context, create, update, delete)
