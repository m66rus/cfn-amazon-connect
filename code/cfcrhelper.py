import json
import logging
import signal
import urllib3

'''
Date: 
dd/mm/yyyy
Description: 
This is a resource helper for CloudFormation to use Lambda functions to exeute resources within Amazon Connect

'''


# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def cr_handler(event, context, create, update, delete):
    """[summary]

    Args:
        event ([type]): [description]
        context ([type]): [description]
        create ([type]): [description]
        update ([type]): [description]
        delete ([type]): [description]
    """   
    
    
    try:
        logger.info('REQUEST RECEIVED:\n %s', event)
        logger.info('REQUEST RECEIVED:\n %s', context)
        if event['RequestType'] == 'Create':
            logger.info('CREATE!')
            
            response_status, physical_resource_id, response_data = create(event, context)
            
            send_response(event, context, response_status, response_data, physical_resource_id)
        elif event['RequestType'] == 'Update':
            logger.info('UPDATE!')
            
            response_status, physical_resource_id, response_data = update(event, context)
             
            send_response(event, context, response_status, response_data, physical_resource_id)
            
        elif event['RequestType'] == 'Delete':
            logger.info('DELETE!')
            
            response_status, physical_resource_id, response_data = delete(event, context)
            
            send_response(event, context, response_status, response_data, physical_resource_id)
        else:
            logger.info('FAILED!')
            physical_resource_id = ""
            send_response(event, context, "FAILED",
                          {"Message": "Unexpected event received from CloudFormation"}, physical_resource_id)
    except Exception as ex: 
        logger.info('FAILED!')
        logger.info('Helper Error: {}'.format(ex))
        
        send_response(event, context, "FAILED", {
            "Message": "Exception during processing"},"")


def send_response(event, context, response_status, response_data, physical_resource_id):
    """[summary]

    Args:
        event ([type]): [description]
        context ([type]): [description]
        response_status ([type]): [description]
        response_data ([type]): [description]
        physical_resource_id ([type]): [description]
    """    
    
    response_body = json.dumps({
        "Status": response_status,
        "Reason": "See the details in CloudWatch Log Stream: " + context.log_stream_name,
        "PhysicalResourceId": physical_resource_id,
        "StackId": event['StackId'],
        "RequestId": event['RequestId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "Data": response_data
    })

    logger.info('ResponseURL: %s', event['ResponseURL'])
    logger.info('ResponseBody: %s', response_body)
    
    http = urllib3.PoolManager()
    
    response = http.request(
        "PUT", event['ResponseURL'], body=response_body,
        headers={"Content-Type": "application/json", "Content-Length": len(response_body)}
    )

    logger.info("Status code: %s", response.status)
    logger.info("Status message: %s", response.data)

# Need to consider timeouts