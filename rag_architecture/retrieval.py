# import psycopg2
import os,re,ast
import pandas as pd
import time
from config_app.config import get_config
from rag_architecture.few_shot_sentence import find_closest_match
from rag_architecture.indexing_db import init_elastic
from config_app.enum import Variable
import logging
enum = Variable()
config_app = get_config()

ELASTIC_HOST = config_app['parameter']['elastic_url']
number_size_elas = config_app['parameter']['num_size_elas']

df = pd.read_excel(config_app['parameter']['data_private'])

def parse_price_range(price):
    pattern = r"(?P<prefix>\b(dưới|trên|từ|đến|khoảng)\s*)?(?P<number>\d+(?:,\d+)*)\s*(?P<unit>triệu|nghìn|tr|k|kg|l|lít|kw|w|t|btu)?\b"
    print(pattern)
    min_price = 0
    max_price = 100000000
    for match in re.finditer(pattern, price, re.IGNORECASE):
        prefix = match.group('prefix') or ''
        number = float(match.group('number').replace(',', ''))
        unit = match.group('unit') or ''
        if unit.lower() == '':
            return min_price, max_price

        if unit.lower() in ['triệu','tr','t']:
            number *= 1000000
        elif unit.lower() in ['nghìn','k']:
            number *= 1000
        elif unit.lower() in ['kw']:
            number *= 1000

        if prefix.lower().strip() == 'dưới':
            max_price = min(max_price, number)
        elif prefix.lower().strip() == 'trên':
            min_price = min(max_price, number)
        elif prefix.lower().strip() == 'từ':
            min_price = min(max_price, number)
        elif prefix.lower().strip() == 'đến':
            max_price = max(min_price, number)
        else:  # Trường hợp không có từ khóa
            min_price = number * 0.8
            max_price = number * 1.2

    if min_price == float('inf'):
        min_price = 0
    # print('min_price, max_price:',min_price, max_price)
    return min_price, max_price

def search_specifications(client, index_name, product, product_name, specifications, price, power, weight, volume):
    order = "asc"  # Default order
    cheap_keywords = enum.CHEAP_KEYWORDS
    expensive_keywords = enum.EXPENSIVE_KEYWORDS
    word = ""
    for keyword in cheap_keywords:
        if keyword in price.lower():
            order = "asc"
            word = keyword
            price = ""
    for keyword in expensive_keywords:
        if keyword in price.lower():
            order = "desc"
            word = keyword
            price = ""
    
    # Create the Elasticsearch query if a product is found
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "group_product_name": product
                        }
                    },
                    {
                        "match": {
                            "specification": specifications
                        }
                    },
                    {
                        "match": {
                            "group_name": product_name
                        }
                    }
                ]
            }
            },
        "size": number_size_elas,
    }

    if word:
        query["sort"] = [
            {"lifecare_price": {"order": order}}
        ]

    if price :
      min_price, max_price = parse_price_range(price)
      price_filter = {
          "range": {
              "lifecare_price": {
                  "gte": min_price,
                  "lte": max_price
              }
          }
      }
      query["query"]["bool"]["must"].append(price_filter)

    if power:
      min_power, max_power = parse_price_range(power)
      power_filter = {
          "range": {
              "power": {
                  "gte": min_power,
                  "lte": max_power
              }
          }
      }
      query["query"]["bool"]["must"].append(power_filter)

    if weight:
        min_weight, max_weight = parse_price_range(weight)
        weight_filter = {
            "range": {
                "weight": {
                    "gte": min_weight,
                    "lte": max_weight
                }
            }
        }
        query["query"]["bool"]["must"].append(weight_filter)

    if volume:
        min_volume, max_volume = parse_price_range(volume)
        volume_filter = {
            "range": {
                "volume": {
                    "gte": min_volume,
                    "lte": max_volume
                }
            }
        }
        query["query"]["bool"]["must"].append(volume_filter)
    # Execute the search query
    response = client.search(index=index_name, body=query)
    return response
       
def search_prices(client, index_name, product, product_name, price, power, weight, volume):
    order = "asc"  # Default order
    cheap_keywords = enum.CHEAP_KEYWORDS
    expensive_keywords = enum.CHEAP_KEYWORDS
    word = ""
    for keyword in cheap_keywords:
        if keyword in price.lower():
            order = "asc"
            word = keyword
            price = ""
    for keyword in expensive_keywords:
        if keyword in price.lower():
            order = "desc"
            word = keyword
            price = ""
    # Build the base query
    # Create the Elasticsearch query if a product is found
    
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "group_name": product_name
                        }
                    },
                    {
                        "match": {
                            "group_product_name": product
                        }
                    }
                ]
            }
        },
        "size": number_size_elas
    }

    if word:
        query["sort"] = [
            {"lifecare_price": {"order": order}}
        ]

    # Add specifications-based filters
    if price:
        min_price, max_price = parse_price_range(price)
        price_filter = {
            "range": {
                "lifecare_price": {
                    "gte": min_price,
                    "lte": max_price
                }
            }
        }
        query["query"]["bool"]["must"].append(price_filter)

    if power:
        min_power, max_power = parse_price_range(power)
        power_filter = {
            "range": {
                "power": {
                    "gte": min_power,
                    "lte": max_power
                }
            }
        }
        query["query"]["bool"]["must"].append(power_filter)

    if weight:
        min_weight, max_weight = parse_price_range(weight)
        weight_filter = {
            "range": {
                "weight": {
                    "gte": min_weight,
                    "lte": max_weight
                }
            }
        }
        query["query"]["bool"]["must"].append(weight_filter)

    if volume:
        min_volume, max_volume = parse_price_range(volume)
        volume_filter = {
            "range": {
                "volume": {
                    "gte": min_volume,
                    "lte": max_volume
                }
            }
        }
        query["query"]["bool"]["must"].append(volume_filter)


    res = client.search(index=index_name, body=query)

    return res

def search_quantity(client, index_name, product, product_name, price, power, weight, volume):
    query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "group_product_name": product
                            }
                        },
                        {
                            "match": {
                                "group_name": product_name
                            }
                        }
                    ]
                }
                },
            "size": 100,
            }
    if price:
        min_price, max_price = parse_price_range(price)
        price_filter = {
            "range": {
                "lifecare_price": {
                    "gte": min_price,
                    "lte": max_price
                }
            }
        }
        query["query"]["bool"]["must"].append(price_filter)

    if power:
        min_power, max_power = parse_price_range(power)
        power_filter = {
            "range": {
                "power": {
                    "gte": min_power,
                    "lte": max_power
                }
            }
        }
        query["query"]["bool"]["must"].append(power_filter)

    if weight:
        min_weight, max_weight = parse_price_range(weight)
        weight_filter = {
            "range": {
                "weight": {
                    "gte": min_weight,
                    "lte": max_weight
                }
            }
        }
        query["query"]["bool"]["must"].append(weight_filter)

    if volume:
        min_volume, max_volume = parse_price_range(volume)
        volume_filter = {
            "range": {
                "volume": {
                    "gte": min_volume,
                    "lte": max_volume
                }
            }
        }
        query["query"]["bool"]["must"].append(volume_filter)
    res = client.search(index=index_name, body=query)
    return res

def search_compare(client, index_name, product, product_name, price, power, weight, volume):
    query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "group_product_name": product
                            }
                        },
                        {
                            "match": {
                                "product_name": product_name
                            }
                        }
                    ]
                }
                },
            "size": 1,
          }
    if price :
        min_price, max_price = parse_price_range(price)
        price_filter = {
            "range": {
                "lifecare_price": {
                    "gte": min_price,
                    "lte": max_price
                }
            }
        }
        query["query"]["bool"]["must"].append(price_filter)

    if power:
      min_power, max_power = parse_price_range(power)
      power_filter = {
          "range": {
              "power": {
                  "gte": min_power,
                  "lte": max_power
              }
          }
      }
      query["query"]["bool"]["must"].append(power_filter)

    if weight:
        min_weight, max_weight = parse_price_range(weight)
        weight_filter = {
            "range": {
                "weight": {
                    "gte": min_weight,
                    "lte": max_weight
                }
            }
        }
        query["query"]["bool"]["must"].append(weight_filter)

    if volume:
        min_volume, max_volume = parse_price_range(volume)
        volume_filter = {
            "range": {
                "volume": {
                    "gte": min_volume,
                    "lte": max_volume
                }
            }
        }
        query["query"]["bool"]["must"].append(volume_filter)

    res = client.search(index=index_name, body=query)
    return res

def search_product(client, index_name, product_name):
    query = {
        "query": {
            "bool": {
                "must": [
                    
                    {
                        "match": {
                            "product_name": product_name
                        }
                    }
                ]
            }
        }
    }


    res = client.search(index=index_name, body=query)
    return res

def search_db(demands):
    '''
    
    '''
    #init 
    out_text = ""
    products = []
    product_dict = {}
    index_name = enum.INDEX_ELASTIC
    client = init_elastic(df,index_name, ELASTIC_HOST)
    # client = init_elastic(df, index_name, ELASTIC_CLOUD_ID, ELASTIC_API_KEY)
    product_names = []
    list_product = df['group_name'].unique()
    check_match_product = find_closest_match(demands['object'][0], list_product)
    print('check_match_product',check_match_product)
    if check_match_product[1] < 75:
        # out_text += f"Anh/chị có thể cho tôi biết thêm thông tin chi tiết sản phẩm để tôi có thể hỗ trợ Anh/chị được không?" 
        ok = 0
        return out_text, products, ok
    elif len(demands)>1:
        product_names = demands['object']
        if isinstance(demands['price'], list):
            prices = demands['price']*len(demands['object'])
        else:
            prices = ast.literal_eval(demands['price'])*len(demands['object'])
        power = demands['power']
        weight = demands['weight']
        volume = demands['volume']
        specifications = demands['specifications']
    else:
        product_names = demands['object']
        prices = ['']*len(demands['object'])
        power = ''
        weight = ''
        volume = ''
        specifications = ''
    print('------check object----', product_names)
    result = []
    t1 = time.time()
    quantity_specifications = enum.QUANTITY_SPECIFICATIONS
    compare_specifications = enum.COMPARE_SPECIFICATIONS
    for product_name, price in zip(product_names, prices):
        product_match = find_closest_match(product_name, list_product)[0]
        result_df = df[df['group_name'] == product_match]
        product = result_df['group_product_name'].tolist()[0]
        # full option specifications, giá, công suất, khối lượng, dung tích
        if specifications and (price or power or weight or volume) or specifications:
            # Count quantity each group name
            if specifications in quantity_specifications:
                resp = search_quantity(client, index_name, product, product_name, price, power, weight, volume)
                ok = 1 # count
            elif specifications in compare_specifications:
                resp = search_compare(client, index_name, product, product_name, price, power, weight, volume)
                ok = 2 
            elif len([specifications]) > 1:
                resp = search_specifications(client, index_name, product, product_name, specifications, price, power, weight, volume)
                ok = 2 
            elif price or power or weight or volume:
                resp = search_prices(client, index_name, product, product_name, price,  power, weight, volume)
                ok = 2 
            else:
                resp = search_product(client, index_name, product_name)
                ok = 2
            
        elif price or power or weight or volume:
            resp = search_prices(client, index_name, product, product_name,price,  power, weight, volume)
            ok = 2 
        else:
            resp = search_product(client, index_name, product_name)
            ok = 2

        result.append(resp)

    for product_name, product in zip(product_names, result):
        s_name = product_name
        # Check query is None
        if product['hits']['hits'] == [] and ok != 0:
            out_text += f"không có sản phẩm mà anh/chị cần?"
            break
        cnt = 0
        quantity_name = ""
        for i, hit in enumerate(product['hits']['hits']):
            check_score = hit.get('_score')
            product_details = hit['_source']
            product =  {
                "code" : "",
                "name" : "",
                "link" : ""
            }
            if check_score is None or float(check_score) >= 2.5:
                cnt+=1
                if ok == 2:
                    if len(product_names) > 1 and i < 2:
                        out_text += f"\n{i + 1}. *{product_details['product_name']} - Mã: {product_details['product_code']}\n"
                        out_text += f"  Thông số sản phẩm: {product_details['specification']}\n"
                        out_text +=  " - Giá tiền: {:,.0f} đ*\n".format(product_details['lifecare_price'])
                        product = {
                            "code": product_details['product_info_id'],
                            "name": product_details['product_name'],
                            "link": product_details['file_path']
                        }
                    elif len(product_names) == 1 and i < 4:
                        out_text += f"\n{i + 1}. *{product_details['product_name']} - Mã: {product_details['product_code']}\n"
                        out_text += f"  Thông số sản phẩm: {product_details['specification']}\n"
                        out_text +=  " - Giá tiền: {:,.0f} đ*\n".format(product_details['lifecare_price'])
                        product = {
                            "code": product_details['product_info_id'],
                            "name": product_details['product_name'],
                            "link": product_details['file_path']
                        }
                        product_dict[f'{i+1}'] = product_details['product_name']
                elif ok == 1 and i < 3:
                    quantity_name +=f"  {product_details['product_name']} - Mã: {product_details['product_code']}\n"
                    # quantity_name +=  " -  Giá tiền: {:,.0f} đ*\n".format(product_details['lifecare_price'])
                    quantity_name += f"  Thông số sản phẩm: {product_details['specification']}\n"
                    quantity_name +=  " - Giá tiền: {:,.0f} đ\n".format(product_details['lifecare_price'])
                    # quantity_name += f"  Mã kho: {product_details['product_code']}\n"
                    product = {
                            "code": product_details['product_info_id'],
                            "name": product_details['product_name'],
                            "link": product_details['file_path']
                        }
                if len(products) < 10 and product['code'] != "":
                    products.append(product)
        if ok == 1:
            out_text += f"ví dụ trong {cnt} sản phẩm:"
            out_text += quantity_name
            out_text += f"Hãy trả lời là có {cnt} sản phẩm nhé!"
    print("-----time elastic search-------:",time.time() - t1)
    logging.info(f'======== elasticsearch output ==========:\n{out_text}')
    print('======== elasticsearch output ==========:\n', out_text)
    return out_text, products, ok