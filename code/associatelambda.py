import cfcrhelper
import logging
import boto3

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def create(event, context):
    # Cloudformation Create resource step
    # Initialise
    response_status = "SUCCESS"
    physical_resource_id = "99"
    response_data = {}
    
    # TODO add check for InstanceId is not null if it is return FAILED
    # TODO check mandatory attributes are not empty
    # TODO Exception handling 
    logger.debug("Associate a Lambda Function: {}".format(event))
    
     
    try:
        client = boto3.client("connect")
        
        response = client.associate_lambda_function(
            InstanceId=event["ResourceProperties"]["InstanceId"],
            FunctionArn=event["ResourceProperties"]["LambdaFunctionArn"]
        )
        
        logger.debug("response: {}".format(response))
        if response["ResponseMetadata"]["HTTPStatusCode"] == "200":
            
            response_data = {
                "FunctionName": event["ResourceProperties"]["LambdaName"],
                "Message": "Created"
            }
        else:
            response_status = "FAILED"
            response_data = {
                "Message": "Error in Create() function not associated"
            }
            logger.debug('response:\n %s', response)
            
        
        physical_resource_id = event["ResourceProperties"]["LambdaFunctionArn"]
                
    except Exception as ex: 
        response_status = "FAILED"
        response_data = { 
            "Message": "Error in except"
            }
        logger.debug("Exception: \n {}".format(ex))
        
        # TODO add response_data contents
         
    
    return response_status, physical_resource_id, response_data



def update(event, context):
    # Cloudformation Update resource step
    
    
    response_status = "SUCCESS"
    physical_resource_id = event["PhysicalResourceId"]
    response_data = {
        "Message" : "No update function available"
    }
    
    
    return response_status, physical_resource_id, response_data    

def delete(event, context):
    # Cloudformation Delete resource step
    
    # TODO add check for InstanceId is not null if it is return FAILED
    # TODO check mandatory attributes are not empty
    # TODO Exception handling
    response_status = "SUCCESS"
    physical_resource_id = event["PhysicalResourceId"]
    response_data = {}
    
    client = boto3.client("connect")
    
    logger.debug("Assoicate Lambda: {}".format(event))
  
    try:
        response = client.disassociate_lambda_function(
            InstanceId=event["ResourceProperties"]["InstanceId"],
            FunctionArn=physical_resource_id
        )
        # Check response was successful
        if response["ResponseMetadata"]["HTTPStatusCode"] != "200":
            
            response_status = "FAILED"
            response_data = {
                "Message": "Error in Delete() function"
            }
            logger.debug('response:\n %s', response)
                
    except:
        response_status = "FAILED"
        logger.debug("Exception: FAILED!")
        # TODO add response_data contents
        
            

    
    return response_status, physical_resource_id, response_data    


def handler(event, context):
    """
    Main handler function, passes off it's work to crhelper's cfn_handler
    """
    # update the logger with event info
    logger.debug("Event: {}".format(event))
    
  
    return cfcrhelper.cr_handler(event, context, create, update, delete)

