#!/usr/bin/env python3
"""
Local test script for Lambda function
This helps verify the logic works before deploying to AWS
"""

import json
from lambda_function import lambda_handler

def test_lambda_function():
    """Test the Lambda function with sample data"""
    
    # Sample test event (similar to what API Gateway would send)
    test_event = {
        "date": "2024-12-25",
        "time": "19:00",
        "party_size": 2,
        "location": "New York City, New York",
        "cuisines": "Japanese"
    }
    
    print("🧪 Testing Lambda function locally...")
    print(f"Input: {json.dumps(test_event, indent=2)}")
    print("\n" + "="*50 + "\n")
    
    try:
        # Call the Lambda handler
        result = lambda_handler(test_event, None)
        
        print("✅ Function executed successfully!")
        print(f"Status Code: {result['statusCode']}")
        print(f"Response Body: {json.dumps(json.loads(result['body']), indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Function failed with error: {str(e)}")
        return False

def test_error_handling():
    """Test error handling with invalid input"""
    
    print("\n🧪 Testing error handling...")
    
    # Test with missing required fields
    invalid_event = {
        "date": "invalid-date",
        "party_size": "not-a-number"
    }
    
    try:
        result = lambda_handler(invalid_event, None)
        print(f"Status Code: {result['statusCode']}")
        print(f"Response: {result['body']}")
        
    except Exception as e:
        print(f"Expected error caught: {str(e)}")

if __name__ == "__main__":
    print("🚀 Resy Roulette Lambda Function - Local Test")
    print("="*50)
    
    # Test normal operation
    success = test_lambda_function()
    
    # Test error handling
    test_error_handling()
    
    if success:
        print("\n🎉 All tests passed! Your function is ready for Lambda deployment.")
    else:
        print("\n⚠️  Some tests failed. Please fix issues before deploying.")
