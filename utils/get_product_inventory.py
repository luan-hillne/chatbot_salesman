import requests
import pandas as pd

# from config_app.config import get_config
# config_app = get_config()

# URL của API

# data_private = config_app['parameter']['data_private']
# df = pd.read_excel(data_private)
# Dữ liệu cần gửi trong yêu cầu POST
def get_inventory(msp,mt=None):
    print('============get_inventory============')
    url = "http://wms.congtrinhviettel.com.vn/wms-service/service/magentoSyncApiWs/getListRemainStockV2"
    results = {'terms': [], 'out_text': '', 'inventory_status': False, 'products': [], 'object_product': '', 'similarity_status': False}
    if mt:
        payload = {
            "source": {
                "goodsCode": msp.upper(),
                "provinceCode": mt.upper()
            }
        }
    else:
        payload = {
            "source": {
                "goodsCode": msp.upper(),
                "provinceCode": mt
            }
        }
    # Headers nếu có (ở đây để trống nếu không yêu cầu)
    headers = {
        "Content-Type": "application/json"
    }
    # if msp.upper() not in df['group_product_code']:
    #     results['inventory_status'] = True
    #     results['out_text'] = "Anh/chị vui lòng nhập mã sản phẩm và mã tỉnh theo mẫu sau:"
    #     return "Mã sản phẩm của bạn không đúng, vui lòng nhập lại mã!"
    # Gửi yêu cầu POST đến API
    response = requests.post(url, json=payload, headers=headers,timeout=60)

    # Kiểm tra mã trạng thái của phản hồi
    if response.status_code == 200:
            # Chuyển đổi phản hồi sang dạng JSON
        response_data = response.json()
        
        if len(response_data['data']) == 0:
            in_stock_out = in_stock(msp)
            return f"Anh/chị xin thông cảm! Hiện tại hàng tại {mt} đã hết hãy liên hệ chi nhánh để bổ sung thêm hàng " + in_stock_out
        # Kiểm tra nếu có dữ liệu trong phần 'data'
        if 'data' in response_data and response_data['data'] is not None:
            # Duyệt qua từng mục trong danh sách 'data'
            info_strings = []
            num = 0
            for item in response_data['data']:
                # Xử lý từng mục trong danh sách
                amount = item["amount"] if item["amount"] is not None else ""
                goods_name = item["goodsName"] if item["goodsName"] is not None else ""
                stock_name = item["stockName"] if item["stockName"] is not None else ""
                stock_code = item["stockCode"] if item["stockCode"] is not None else ""
                # In hoặc xử lý thông tin từng mục
                if stock_name != '' or stock_code !='':
                    if num <= 15:
                        info_string = (
                            f"Tên Kho: {stock_name}\n"
                            f"Mã kho: {stock_code}\n"
                            f"SL: {int(amount)}\n"
                            "---------"
                        )
                        info_strings.append(info_string)
                    num += 1
                # Kết hợp các chuỗi thành một chuỗi duy nhất
            final_string = "\n".join(info_strings)
            return final_string
    else:
        # In lỗi nếu có
        return "Hiện tại tôi không thể tra cứu thông tin hàng tồn kho của sản phẩm bạn đang mong muốn, xin vui lòng thử lại sau."


def in_stock(msp):
    print('============in_stock============')
    url = "http://wms.congtrinhviettel.com.vn/wms-service/service/magentoSyncApiWs/getListRemainStockV2GroupByProvince"
    payload = {
        "source": {
            "goodsCode": msp.upper(),
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers,timeout=60)

    if response.status_code == 200:
        response_data = response.json()
        if len(response_data['data']) == 0:
            return 'hoặc kiểm tra lại thông tin sản phẩm muốn tra cứu.'
        if 'data' in response_data and response_data['data'] is not None:
            info_strings = []
            num = 0
            total_amount = 0
            for item in response_data['data']:
                amount = item["amount"] if item["amount"] is not None else ""
                total_amount += amount
                goods_code = item["goodsCode"] if item["goodsCode"] is not None else ""
                goods_name = item["goodsName"] if item["goodsName"] is not None else ""
                province_code = item["provinceCode"] if item["provinceCode"] is not None else ""
                if province_code != '' or amount !='':
                    if num <= 15:
                        info_string = (
                            f"CNCT: {province_code}\n"
                            f"SP: {goods_name}\n"
                            f"SL: {int(amount)}\n"
                            "---------"
                        )
                        info_strings.append(info_string)
                    num += 1
            final_string = "\n".join(info_strings)
            return f'\n\nTổng số lượng hàng hóa trên cả nước là {int(total_amount)} (ngoại trừ kho kv)\n' + "---------\n"+ final_string
    else:
        return "Hiện tại tôi không thể tra cứu thông tin hàng tồn kho của sản phẩm bạn đang mong muốn, xin vui lòng thử lại sau."

# print(get_inventory('wifi tenda f3','H'))