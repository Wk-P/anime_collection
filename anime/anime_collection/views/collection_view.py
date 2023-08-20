from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
import json
import os




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
            # 获取图片
            folder_path = os.path.dirname(".\\anime\\anime_collection\\static\\files\\img\\") # 替换为你要遍历的文件夹路径
            # 获取文件夹中的所有内容（包括子文件夹）
            folder_contents = os.listdir(folder_path)
            
            img_name_src = {}

            with open(json_path, 'r+', encoding='utf-8') as f:
            

                for item in folder_contents:
                    item_path = os.path.join(folder_path, item)

                    # 获取完整文件名
                    full_file_name = os.path.basename(item)

                    # 使用 os.path.splitext() 分割文件名和后缀，然后只保留文件名部分
                    file_name_without_extension = os.path.splitext(full_file_name)[0]

                    img_name_src[f'{file_name_without_extension}'] = item_path
                
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
                            "link": img_name_src[item['title']]
                        })
                    else:
                        anime_data_set.append({
                            "imgSrc": item['cover'],
                            "name": item['title'],
                            "rating": None,
                            "link": img_name_src[item['title']]
                        })
                response = dict()
                response['data'] = anime_data_set
            return JsonResponse(response)
        
        except FileNotFoundError as e:
            print(e)
            return JsonResponse({'StatusCode': 404})
    else:
        return JsonResponse({'StatusCode': 403})