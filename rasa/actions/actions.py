from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ExtractNameAction(Action):

    def name(self) -> Text:
        return "action_extract_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = None

        for ent in tracker.latest_message.get("entities", []):
            if ent["entity"] == "user_name":
                user_name = ent["value"]

        # You can now use this name in your bot logic
        if user_name:
            dispatcher.utter_message(text=f"Xin chào {user_name}!\nRất vui được gặp {user_name}.Nếu có câu hỏi hoặc yêu cầu cụ thể nào liên quan đến dịch vụ mua sắm của VCC em sẽ cố gắng giúp anh/chị một cách tốt nhất.!")
        else:
            dispatcher.utter_message(text="Xin chào! Em là VCC AI BOT, trợ lý mua sắm thông minh. Em có thể giúp gì cho anh/chị hôm nay?.")

        return []

#policy_produce
class ExtractProduceAction(Action):

    def name(self) -> Text:
        return "action_extract_produce"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        produce_name_policy = None

        for ent in tracker.latest_message.get("entities", []):
            if ent["entity"] == "produce_name_policy":
                produce_name_policy = ent["value"]

        # You can now use this name in your bot logic
        products = ["bảo hành", "chính sách bảo hành", "bao hanh", "chinh sach bao hanh"]       
        if any(p == produce_name_policy.lower() for p in products):
            dispatcher.utter_message(text=f"""
            Chính sách bảo hành sản phẩm của chúng tôi bao gồm:
            1. Chính sách bảo hành 1 đổi 1
            Thời gian áp dụng: Một đổi một trong vòng 7 ngày kể từ ngày Anh/chị mua hàng và chi phí bảo hành nằm trong 0.5% chi phí giá bán theo quy định TCT.
            Điều kiện: Áp dụng bảo hành đối với các sản phẩm lỗi nằm trong danh sách sản phẩm của VCC. Sản phẩm đổi trả phải giữ nguyên 100% hình dạng ban đầu và hoàn lại đầy đủ phị kiện. Số điện thoại mua sản phẩm trùng khớp với dữ liệu trên hệ thống ghi nhận.
            Lưu ý: Không áp dụng hoàn tiền sản phẩm
            2. Chính sách bảo hành sửa chữa, thay thế linh kiện
            Thời gian: Áp dụng 12 tháng kể từ ngày Anh/chị mua sản phẩm.
            Phạm vi: Áp dụng cho các lỗi kỹ thuật do nhà sản xuất. Không bảo hành đối với các trường hợp do sử dụng, sửa chữa không đúng cách hoặc hỏng hóc do nguyên nhân bên ngoài.
            Điều kiện: Lỗi được xác nhận và kiểm tra bởi nhân sự triển khai tại các CNCT. Số điện thoại mua sản phẩm trùng khớp với dữ liệu trên hệ thống ghi nhận.
            Lưu ý: Để đảm bảo quyền lợi quý khách cần cung cấp hình ảnh/clip sản phẩm lỗi khi yêu cầu bảo hành.
            """)
        else:
            dispatcher.utter_message(text="Anh/chị xin thông cảm! Em không hiểu yêu cầu đưa ra.")

        return []
    


class ExtractProduceInventory(Action):

    def name(self) -> Text:
        return "action_extract_produce_inventory"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        produce_name_inventory = None

        for ent in tracker.latest_message.get("entities", []):
            if ent["entity"] == "produce_name_inventory":
                produce_name_inventory = ent["value"]

        # You can now use this name in your bot logic
        products = ["kho", "tồn kho", "sản phẩm tồn kho", "ton kho", "trong kho"]       
        if any(p == produce_name_inventory.lower() for p in products):
            dispatcher.utter_message(text=f"""
                Anh/chị vui lòng nhập mã hoặc tên sản phẩm và mã tỉnh theo mẫu sau:
                """)
        else:
            dispatcher.utter_message(text="Anh/chị xin thông cảm! Hiện tại hàng đã hết hãy liên hệ chi nhánh để bổ sung thêm hàng.")

        return []
    

class ExtractSearchProductSimilar(Action):

    def name(self) -> Text:
        return "action_search_product_similar"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        search_product_similar = None

        for ent in tracker.latest_message.get("entities", []):
            if ent["entity"] == "search_product_similar":
                search_product_similar = ent["value"]

        # You can now use this name in your bot logic
        products = ["tương tự", "sản phẩm tương tự"]       
        if any(p == search_product_similar.lower() for p in products):
            dispatcher.utter_message(text="""
                Anh/chị vui lòng nhập thông tin sản phẩm để tìm sản phẩm tương tự.
                """)
        else:
            dispatcher.utter_message(text="Anh/chị xin thông cảm! Hiện tại em không tìm thấy sản phẩm tương tự.")

        return []