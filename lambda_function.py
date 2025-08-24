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
        # Parse the incoming event
        if isinstance(event, str):
            event = json.loads(event)
        
        # Extract parameters with defaults
        date = event.get('date', '')
        time = event.get('time', '')
        party_size = int(event.get('party_size', 2))
        location_input = event.get('location', 'New York City, New York')
        cuisines_input = event.get('cuisines', '')
        
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
