#!/usr/bin/env python3
"""
Deployment script for AWS Lambda
This script packages your Lambda function with all dependencies
"""

import os
import shutil
import subprocess
import zipfile
from pathlib import Path

def install_requirements():
    """Install requirements to a local directory"""
    print("Installing requirements...")
    
    # Create a temporary directory for dependencies
    if os.path.exists('lambda_package'):
        shutil.rmtree('lambda_package')
    
    os.makedirs('lambda_package')
    
    # Install requirements to the package directory
    subprocess.run([
        'pip', 'install', '-r', 'lambda_requirements.txt', 
        '-t', 'lambda_package'
    ], check=True)
    
    print("Requirements installed successfully!")

def copy_source_files():
    """Copy source files to the package directory"""
    print("Copying source files...")
    
    # Copy the main files
    files_to_copy = [
        'lambda_function.py',
        'retrieve.py',
        '__init__.py'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, 'lambda_package/')
            print(f"Copied {file}")
    
    print("Source files copied successfully!")

def create_zip_package():
    """Create a ZIP file for Lambda deployment"""
    print("Creating ZIP package...")
    
    zip_filename = 'resy_roulette_lambda.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('lambda_package'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'lambda_package')
                zipf.write(file_path, arcname)
    
    print(f"ZIP package created: {zip_filename}")
    return zip_filename

def cleanup():
    """Clean up temporary files"""
    print("Cleaning up...")
    if os.path.exists('lambda_package'):
        shutil.rmtree('lambda_package')
    print("Cleanup complete!")

def main():
    """Main deployment process"""
    print("Starting Lambda deployment process...")
    
    try:
        install_requirements()
        copy_source_files()
        zip_filename = create_zip_package()
        cleanup()
        
        print(f"\n✅ Deployment package ready: {zip_filename}")
        print("\nNext steps:")
        print("1. Upload this ZIP file to AWS Lambda")
        print("2. Set environment variables for your Resy API tokens")
        print("3. Configure the Lambda function settings")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        cleanup()

if __name__ == "__main__":
    main()
