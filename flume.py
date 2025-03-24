import boto3
import datetime
import gzip
import json
import os
import uuid

def handler(event, context):

    print(event)

    try:

        if event['queryStringParameters']['verify'] == os.environ['VERIFY']:

            uniq = str(uuid.uuid4())

            if isinstance(event['body'], str):
                data = json.loads(event['body'])
            else:
                data = event['body']

            now = datetime.datetime.now()
            data['@timestamp'] = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+00:00'

            with gzip.open('/tmp/'+uniq+'.json.gz', 'wb') as g:
                g.write(json.dumps(data).encode())
            g.close()

            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            hour = datetime.datetime.now().hour

            s3 = boto3.client('s3')

            bucket = os.environ['BUCKET']
            prefix = os.environ['PREFIX']
            key = f'{prefix}/year={year}/month={month}/day={day}/hour={hour}/{uniq}.json.gz'

            s3.upload_file('/tmp/'+uniq+'.json.gz', bucket, key)

            code = 200
            msg = 'Shipped: '+key

        else:

            code = 404
            msg = 'Where the Internet Ends'

    except:
        
        code = 404
        msg = 'Where the Internet Ends'

    return {
        'statusCode': code,
        'body': json.dumps(msg)
    }