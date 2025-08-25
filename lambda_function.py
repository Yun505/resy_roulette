"""AWS Lambda function for Resy Roulette restaurant recommendation system"""

import json
import os
import logging
from retrieve import ResyRetriever

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    
    Expected event format:
    {
        "date": "2024-12-25",
        "time": "19:00",
        "party_size": 2,
        "location": "New York City, New York",
        "cuisines": "Japanese, Korean, American"
    }
    """
    try:
        # Handle different event types (API Gateway, direct invocation, etc.)
        if 'httpMethod' in event:
            # API Gateway event
            if event['httpMethod'] == 'GET' and event['path'] == '/health':
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'status': 'healthy',
                        'service': 'resy-roulette-lambda'
                    })
                }
            elif event['httpMethod'] == 'POST' and event['path'] == '/restaurant':
                # Parse body from API Gateway
                if 'body' in event:
                    body = event['body']
                    if isinstance(body, str):
                        body = json.loads(body)
                else:
                    body = event
            else:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': 'Endpoint not found'})
                }
        else:
            # Direct Lambda invocation
            body = event
        
        # Extract parameters with defaults
        date = body.get('date', '')
        time = body.get('time', '')
        party_size = int(body.get('party_size', 2))
        location_input = body.get('location', 'New York City, New York')
        cuisines_input = body.get('cuisines', '')
        
        # Parse cuisines
        if cuisines_input:
            cuisines_list = [cuisine.strip() for cuisine in cuisines_input.split(',')]
        else:
            cuisines_list = []
        
        # Get location coordinates
        location = ResyRetriever.get_location(location_input)
        
        # Create ResyRetriever object
        retriever = ResyRetriever(
            date=date,
            party_size=party_size,
            time=time,
            location=location,
            cuisine_list=cuisines_list
        )
        
        # Get restaurants and randomize
        restaurants = retriever.get_restaurants()
        
        if restaurants:
            randomized_restaurant = retriever.randomize_restaurants(restaurants)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': True,
                    'restaurant': {
                        'name': str(randomized_restaurant['name']),
                        'cuisine': randomized_restaurant['cuisine'],
                        'location': randomized_restaurant['location']
                    },
                    'total_restaurants_found': len(restaurants)
                })
            }
        else:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'message': 'No restaurants found for the given criteria',
                    'total_restaurants_found': 0
                })
            }
            
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }
