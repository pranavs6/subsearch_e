from celery import shared_task
import os
import subprocess
import tempfile
import boto3

print('Tasks.py is alive!')

@shared_task(name='uploadvideo')
def uploadvideo(local_video_path):
    print("Function Called")
    try:
        print("Task received")
 
        s3_client = boto3.client("s3")

 
        response = s3_client.list_objects_v2(Bucket='subsearch-videos-psar')
        s3_count = sum(1 for _ in response.get('Contents', []))
        s3_filename = f"video{s3_count}.mp4"
        
        s3_client.upload_file(local_video_path, "subsearch-videos-psar", s3_filename)
        s3_url = f"https://subsearch-videos-psar.s3.amazonaws.com/{s3_filename}"
        print("Video uploaded successfully")
        acl_command = str("aws s3api put-object-acl --bucket subsearch-videos-psar --key " + s3_filename +" --acl public-read")
        process = subprocess.Popen(acl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        print(f"{s3_filename} is now public")

        with tempfile.NamedTemporaryFile(delete=False, suffix='.srt') as temp_output_file:
            output_file_path = temp_output_file.name
        

        command = f'ccextractor {local_video_path} -o {output_file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()


        if process.returncode != 0:
            raise RuntimeError(f"Subtitle extraction failed: {error.decode('utf-8')}")

        print("Subtitles generated")


        subtitles = []
        with open(output_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if lines[i].strip().isdigit():
                    index = lines[i].strip()
                    timeframe_line = lines[i + 1].strip()
                    subtitle_lines = []
                    i += 2
                    while i < len(lines) and lines[i].strip() != "":
                        subtitle_lines.append(lines[i].strip())
                        i += 1
                    subtitle_text = " ".join(subtitle_lines)
                    subtitles.append((index, timeframe_line, subtitle_text))
                else:
                    i += 1
        print("Subtitles parsed")


        dynamodb_client = boto3.client("dynamodb")
        table_name = s3_filename[:-4] + "_data"
        table = dynamodb_client.create_table(
        TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'subtitle_string',
                    'KeyType': 'HASH'  
                },
                {
                   'AttributeName': 'video_url',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'subtitle_string',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'video_url',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        dynamodb_client.get_waiter('table_exists').wait(TableName=table_name)

        for subtitle in subtitles:
            index, timeframe, subtitle_text = subtitle
            dynamodb_client.put_item(
                TableName=table_name,
                Item={
                    "subtitle_string": {"S": subtitle_text.lower() + "   ->   " + timeframe},
                    "video_url": {"S": s3_url}
                }
            )
        print("Subtitles stored")
        print("Task executed")
        
    except Exception as e:
        print(f"An error occurred in uploadvideo task: {str(e)}")
        raise

    finally:
        try:
            os.remove(output_file_path)
            print(f"Temporary file {output_file_path} deleted")
        except Exception as cleanup_error:
            print(f"Error cleaning up temporary file: {cleanup_error}")

