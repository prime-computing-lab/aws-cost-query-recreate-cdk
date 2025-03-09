import json
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    client = boto3.client('ce')
    today = datetime.today().date()
    start_date = today.replace(day=1)  # First day of the month
    end_date = today  # Today

    response = client.get_cost_and_usage(
        TimePeriod={'Start': str(start_date), 'End': str(end_date)},
        Granularity='MONTHLY',
        Metrics=['BlendedCost']
    )

    cost = response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
    
    return {
        'statusCode': 200,
        'body': json.dumps({'AWS Cost (Current Month)': f"${cost}"})
    }
