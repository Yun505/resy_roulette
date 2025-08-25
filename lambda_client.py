"""
Lambda API Client for Resy Roulette
Handles communication with the deployed AWS Lambda function
"""

import requests
import json
import logging
from typing import Dict, Any, Optional

class LambdaClient:
    """Client for communicating with the deployed Lambda function"""
    
    def __init__(self, api_gateway_url: str):
        """
        Initialize the Lambda client
        
        Args:
            api_gateway_url: The API Gateway URL where your Lambda is deployed
        """
        self.api_url = api_gateway_url.rstrip('/')
        self.logger = logging.getLogger(__name__)
    
    def get_restaurant(self, date: str, party_size: int, time: str, 
                       location: str, cuisines: str) -> Optional[Dict[str, Any]]:
        """
        Get restaurant recommendation from Lambda
        
        Args:
            date: Date in YYYY-MM-DD format
            party_size: Number of people
            time: Time in HH:MM format
            location: Location string
            cuisines: Comma-separated cuisine types
            
        Returns:
            Dictionary with restaurant data or None if failed
        """
        try:
            # Prepare the request payload
            payload = {
                "date": date,
                "party_size": party_size,
                "time": time,
                "location": location,
                "cuisines": cuisines
            }
            
            self.logger.info(f"Sending request to Lambda: {payload}")
            
            # Make the request to Lambda
            response = requests.post(
                f"{self.api_url}/restaurant",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"Lambda response: {result}")
                
                # Handle API Gateway response structure
                if 'body' in result:
                    # API Gateway response - parse the body
                    try:
                        body_data = json.loads(result['body'])
                        if body_data.get('success'):
                            return body_data
                        else:
                            self.logger.warning(f"Lambda body returned success=False: {body_data}")
                            return None
                    except json.JSONDecodeError:
                        self.logger.error(f"Failed to parse Lambda body: {result['body']}")
                        return None
                else:
                    # Direct Lambda response
                    if result.get('success'):
                        return result
                    else:
                        self.logger.warning(f"Lambda returned success=False: {result}")
                        return None
            else:
                self.logger.error(f"Lambda request failed with status {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request to Lambda failed: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse Lambda response: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in Lambda client: {e}")
            return None
    
    def health_check(self) -> bool:
        """Check if the Lambda API is accessible"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            return response.status_code == 200
        except:
            return False



