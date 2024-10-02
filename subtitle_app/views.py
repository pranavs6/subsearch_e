# views.py
import os
import tempfile
import boto3
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from subtitle_app.tasks import uploadvideo

print("Views.py is alive!")

@sync_to_async
def fetch_subtitles_from_dynamodb(query_string):
    dynamodb_client = boto3.client("dynamodb")
    table_name = "subsearch_primary"
    results = []

    response = dynamodb_client.scan(
        TableName=table_name,
        FilterExpression='contains(subtitle_string, :query)',
        ExpressionAttributeValues={
            ':query': {'S': query_string.lower()}
        }
    )
    for item in response.get('Items', []):
        subtitlestring_timeframe = item.get('subtitle_string', {}).get('S', '')
        subtitle_timeframe = subtitlestring_timeframe.split("   ->   ")
        subtitlestring = subtitle_timeframe[0]
        timeframe = subtitle_timeframe[1]
        start_time, end_time = timeframe.split(' --> ')
            
        h, m, s = map(float, start_time.replace(',', '.').split(':')) 
        total_start_seconds = int(h) * 3600 + int(m) * 60 + s 
        video_urla = item.get('video_url', {}).get('S', '')
        video_url_key = video_urla.split("/")
        video_key = "https://d3howwcxpx5mdp.cloudfront.net/" + video_url_key[3]
        results.append({'video_url': video_key, 'timeframe': timeframe, 'subtitlestring': subtitlestring, 'start':total_start_seconds - 1})

    return results

@method_decorator(csrf_exempt, name='dispatch')
class SearchSubtitlesView(View):
    async def get(self, request, *args, **kwargs):
        query_string = request.GET.get('query', 'None')
        cache_key = f'search_results_{query_string}'
        results = cache.get(cache_key)
        
        if not results:
            results = await fetch_subtitles_from_dynamodb(query_string)
            cache.set(cache_key, results, timeout=60*15)  # Cache timeout of 15 minutes

        return render(request, 'search_subtitles.html', {'results': results})

def upload_video(request):
    if request.method == "POST" and request.FILES.get("video"):
        video_file = request.FILES["video"]
        temp_dir = tempfile.gettempdir()
        local_video_path = os.path.join(temp_dir, video_file.name)
        # Save the file to the local path
        with open(local_video_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)


        result = uploadvideo.delay(local_video_path)
        print(result)

        return render(request, "upload_video.html", {"message": "Video uploaded successfully!"})

    return render(request, "upload_video.html")




