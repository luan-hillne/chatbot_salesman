import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Cấu hình retry với thư viện requests
def get_session(retries, backoff_factor, status_forcelist):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def call_api(url, files, timeout=30):
    session = get_session(
        retries=5,  # Số lần retry tối đa
        backoff_factor=1,  # Thời gian chờ giữa các lần retry (tăng dần)
        status_forcelist=[500, 502, 503, 504]  # Các mã trạng thái sẽ retry
    )
    
    try:
        response = session.post(url, files=files, timeout=timeout)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Xin lỗi, đã có lỗi HTTP xảy ra: {errh}")
        return 'Rất tiếc vì sự cố không mong muốn này. Chúng tôi đang nỗ lực khắc phục và sẽ sớm trở lại. Cảm ơn sự thông cảm của bạn.'
    except requests.exceptions.ConnectionError as errc:
        print(f"Xin lỗi, không thể kết nối đến máy chủ: {errc}")
        return 'Rất tiếc vì sự cố không mong muốn này. Chúng tôi đang nỗ lực khắc phục và sẽ sớm trở lại. Cảm ơn sự thông cảm của bạn.'
    except requests.exceptions.Timeout as errt:
        print(f"Xin lỗi, yêu cầu đã bị timeout: {errt}")
        return 'Rất tiếc vì sự cố không mong muốn này. Chúng tôi đang nỗ lực khắc phục và sẽ sớm trở lại. Cảm ơn sự thông cảm của bạn.'
    except requests.exceptions.RequestException as err:
        print(f"Xin lỗi, đã có lỗi xảy ra: {err}")
        return 'Rất tiếc vì sự cố không mong muốn này. Chúng tôi đang nỗ lực khắc phục và sẽ sớm trở lại. Cảm ơn sự thông cảm của bạn.'


# # Sử dụng hàm call_api
# url = "http://10.248.243.105:8000/process_image_and_voice/"
# files = {"data_type": open("/home/aiai01/Production/Rasa_LLM_Elasticsearch_update/voices/test.wav", "rb")}
# data = {"type": "voice"}

# response = call_api(url, data=data, files=files)
# if response:
#     print(response)
# else:
#     print("Failed to get a valid response from the API")