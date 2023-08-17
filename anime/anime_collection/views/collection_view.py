from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
import json

def html_view(request):
    return render(request, "collection.html")
    
@ csrf_exempt
def read_file(request):
    if request.method == 'POST':
        if 'HTTP_X_SERVER_KEY' in request.META:
            server_key = request.META['HTTP_X_SERVER_KEY']
        # 客户端检测
        if  server_key != "CollectionServer":
            return JsonResponse({'StatusCode': 403})
        
        # 获取追番列表文件内容

        json_path = finders.find('files/json/collection.json')
        try:
            with open(json_path, 'r+', encoding='utf-8') as f:
                
                # 数据处理
                all_data = json.load(f)
                anime_data_set = []
                for item in all_data:
                    item_keys_list = list(item.keys())

                    if 'rating' in item_keys_list:
                        anime_data_set.append({
                            "imgSrc": item['cover'],
                            "name": item['title'],
                            "rating": item['rating'],
                            "link": item['url']
                        })
                    else:
                        anime_data_set.append({
                            "imgSrc": item['cover'],
                            "name": item['title'],
                            "rating": None,
                            "link": item['url']
                        })
                response = dict()
                response['data'] = anime_data_set
            return JsonResponse(response)
        
        except FileNotFoundError as e:
            print(e)
            return JsonResponse({'StatusCode': 404})
    else:
        return JsonResponse({'StatusCode': 403})