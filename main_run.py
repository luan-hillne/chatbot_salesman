import time,os
from chat import predict_rasa_llm,predict_rasa_llm_for_image
from config_app.config import get_config
from utils.get_product_inventory import get_inventory
from utils.google_search import search_google
from utils.api_call import call_api
from datetime import datetime
from rag_architecture.few_shot_sentence import find_closest_match
import pandas as pd
import logging, random
from config_app.enum import Variable
from utils.db_postgresql import DatabaseHandler
enum = Variable()
config_app = get_config()
numberrequest = 0
db_handler = DatabaseHandler()
data_private = config_app['parameter']['data_private']
df = pd.read_excel(data_private)
def save_file(file, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, file.filename)
    with open(file_path, 'wb') as out_file:
        content = file.file.read()
        out_file.write(content)
    return file_path

def handle_request(
    InputText=None,
    IdRequest=None,
    NameBot=None,
    User=None,
    GoodsCode=None,
    ProvinceCode=None,
    ObjectSearch=None,
    PriceSearch=None,
    DescribeSearch=None,
    Image=None,
    Voice=None
    ):
    current_date = datetime.now().strftime("%Y-%m-%d")
    start_time = time.time()
    results = {
        "products": [],
        "product_similarity": [],
        "terms": [],
        "inventory_status": False,
        "similarity_status": False,
        "content": "",
        "status": 200,
        "message": "",
        "time_processing": "",
        "type_input" : "",
        "total_tokens": "",
        "error_code": ""
    }
    image_url = config_app['parameter']['image_url']
    voice_url = config_app['parameter']['voice_url']
    # results['status'] = False
    try:
        if Image:
            logging.info("---SEARCH_IMAGE---")
            print('----Image-----')
            results['type_input'] = 'image'
            img_folder = './data/images/' + User + '/' + current_date
            image_path = save_file(Image, img_folder)
            
            with open(image_path, "rb") as f_image:
                files = {"data_type": f_image}
                # data = {"type": "image"}
                response = call_api(image_url, files=files)

                print('response:', response)
                if response['status'] == 200 and len(response) > 1:
                    objects = response['result']
                    chat_out = predict_rasa_llm_for_image(objects, IdRequest, NameBot, User)
                    results.update({
                        "content": chat_out['out_text'],
                        "terms": chat_out['terms'],
                        "inventory_status": chat_out['inventory_status'],
                        "products": chat_out['products'],
                        "total_tokens": chat_out['total_tokens']
                    })
                    InputText = '-'.join(objects)
                    db_handler.logs_chat_saleman(User, IdRequest, current_date, results['type_input'], results['total_tokens'], "True", results['error_code'], InputText, results['content'])   
                else:
                    results.update({
                        "content": 'Không tìm thấy sản phẩm mà bạn mong muốn.',
                    })
                    results['error_code'] = response

                return results
            
        if Voice:
            logging.info("---Voice---")
            print('----Voice-----')
            results['type_input'] = 'voice'
            
            voice_folder = './data/voices/' + User + '/' + current_date
            voice_path = save_file(Voice, voice_folder)

            with open(voice_path, "rb") as f_wav:
                files = {"speechFile": f_wav}
                # data = {"type": "voice"}
                response = call_api(voice_url, files=files)
                print(response)
                if response['status'] == 200:
                    process_voice = response['content']
                    print('speech_2_text:', process_voice)
                    chat_out = predict_rasa_llm(process_voice, IdRequest, NameBot, User)
            
                    results.update({
                        "content": chat_out['out_text'],
                        "terms": chat_out['terms'],
                        "inventory_status": chat_out['inventory_status'],
                        "products": chat_out['products'],
                        "total_tokens": chat_out['total_tokens']
                    })
                    
                    db_handler.logs_chat_saleman(User, IdRequest, current_date, results['type_input'], results['total_tokens'], 'True', results['error_code'], process_voice, results["content"])
                else:
                    results.update({
                        "content": 'Không tìm thấy sản phẩm mà bạn mong muốn.',
                    })
                    results['error_code'] = response


                return results
        
        elif InputText not in ('terms', None) and InputText != 'similarity_status_true':
            logging.info("---ChatText---")
            print('----ChatText-----')
            results['type_input'] = 'text'
            
            chat_out = predict_rasa_llm(InputText, IdRequest, NameBot, User)
            results.update({
                "content": chat_out['out_text'],
                "terms": chat_out['terms'],
                "inventory_status": chat_out['inventory_status'],
                "similarity_status": chat_out['similarity_status'],
                "products" : chat_out['products'],
                "total_tokens": chat_out['total_tokens']
            })

        elif InputText == 'similarity_status_true':
            results['type_input'] = 'similarity'
            results['similarity_status'] = True
            results['content'] = 'Bạn hãy nhập thông tin về giá hoặc thông số kỹ thuật của sản phẩm bạn đang quan tâm:'
        
        elif ObjectSearch:
            try:
                logging.info("---Similarity---")
                print('----similarity-----')
                results['type_input'] = 'similarity'
                list_product = df["group_name"].unique()
                check_match_product = find_closest_match(ObjectSearch, list_product)
                if check_match_product[1] > 40:
                    search_simi =  search_google(ObjectSearch,PriceSearch, DescribeSearch)
                    results['product_similarity'] = search_simi
                    results.update({
                        "content": 'Tôi đã tìm được những sản phẩm tương tự mà bạn có thể quan tâm:',
                    })
            except:
                results.update({
                    "content": 'Tôi không tìm được những sản phẩm tương tự nào cả!',
                })
                results['error_code'] = "Lỗi tìm kiếm sản phẩm tương tự!"

        # Case 4: GoodsCode is provided and InputText is None
        elif GoodsCode and InputText is None:
            results['type_input'] = 'inventory'
            logging.info("---Inventory---")
            print('----Inventory-----')
            results['content'] = get_inventory(GoodsCode, ProvinceCode)
            InputText = GoodsCode + '-' + ProvinceCode

        elif InputText == 'terms' or InputText == None:
            results['type_input'] = 'first_text'
            results["terms"] = random.choice(enum.rasa_button)
            messages = enum.MESSAGE
            results["content"] = random.choice(messages)
        
        
        db_handler.logs_chat_saleman(User, IdRequest, current_date, results['type_input'], results['total_tokens'], 'True', results['error_code'], InputText, results["content"])

    except Exception as e:
        # results["status"] = 500
        results["content"] = 'Rất tiếc vì sự cố không mong muốn này. Chúng tôi đang nỗ lực khắc phục và sẽ sớm trở lại. Cảm ơn sự thông cảm của bạn!'
        db_handler.logs_chat_saleman(User, IdRequest, current_date, results['type_input'], results['total_tokens'], 'False', 'Lỗi toàn hệ thống!', InputText, results["content"])
    # Set processing time and return results
    results['time_processing'] = time.time() - start_time
    print('results:',results)
    return results
