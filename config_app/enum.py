class Variable():
    # creat table db
    '''
        
    CREATE TABLE IF NOT EXISTS chat_saleman.chat_message (
        user_id VARCHAR,
        session_id VARCHAR,
        message JSONB,
        created_date VARCHAR,
    );
    CREATE TABLE IF NOT EXISTS chat_saleman.logs_chat_saleman (
	id SERIAL PRIMARY KEY,
	user_id VARCHAR,
	session_id VARCHAR,
	created_date VARCHAR,
	input_type VARCHAR,
	llm_key VARCHAR,
	total_token VARCHAR,
	status BOOLEAN,
	error_code VARCHAR,
	human TEXT,
	ai TEXT
	);
    
    CREATE TABLE IF NOT EXISTS chat_saleman.llm_key_table (
	id serial PRIMARY KEY,
	gmail_account VARCHAR,
	llm_key VARCHAR,
	key_type VARCHAR,
    status boolean
    );

'''
    MESSAGE = [
        "Xin chào! Mình là trợ lý AI của bạn tại VCC. Mình đang phát triển nên không phải lúc nào cũng đúng. Bạn có thể phản hồi để giúp mình cải thiện tốt hơn. Mình sẵn sàng giúp bạn với câu hỏi về chính sách và tìm kiếm sản phẩm. Hôm nay bạn cần mình hỗ trợ gì không?",
        "Chào bạn! Tôi là AI hỗ trợ của VCC. Do đang trong quá trình hoàn thiện nên tôi có thể mắc lỗi. Mọi góp ý của bạn đều giúp tôi ngày càng hoàn thiện. Tôi có thể giúp gì cho bạn về các vấn đề chính sách hoặc tìm kiếm thông tin sản phẩm hôm nay?",
        "Xin chào! Là AI trợ lý tại VCC đây. Tôi vẫn đang trong giai đoạn phát triển và có thể không hoàn hảo. Hãy giúp tôi cải thiện bằng cách phản hồi về trải nghiệm của bạn. Tôi có thể hỗ trợ bạn gì về chính sách hoặc thông tin sản phẩm hôm nay?",
        "Xin chào anh/chị! Tôi rất hân hạnh được hỗ trợ anh chị trong việc tìm kiếm sản phẩm và chính sách.",
        "Rất vui khi được hỗ trợ anh/chị trong việc tìm kiếm sản phẩm. Do đang trong quá trình hoàn thiện nên tôi có thể mắc lỗi. Mong anh/chị thông cảm!"
        ]
    SYSTEM_MESSAGE = (
        """
#Định nghĩa:
- Bạn là một chuyên gia tư vấn bán hàng   
- Chỉ được phép sử dụng thông tin sản phẩm trong tài liệu 
#Mục tiêu:
- Mô tả ngắn gọn về thông tin chi tiết về mã sản phẩm, giá cả và thông số kỹ thuật của sản phẩm
    ví dụ tôi hỏi điều hòa bạn hãy trả lời theo mẫu chung sau:
    1. Điều hòa MDV - Biến tần 9000 btu - Mã: 019013000001
    - bảo hành 3 năm cho sản phẩm
    - công suất: 9000 btu/h
    - suất xứ : thái lan
    - giá tiền: 6.014.184 đ 
- Nếu hỏi về số lượng sản phẩm
    Hãy trả lời theo ví dụ mẫu chung sau:
        Số lượng sản phẩm hiện có là 100 sản phẩm:
        lấy ví dụ trong 100 sản phẩm
        1. Đèn trụ cổng năng lượng mặt trời - Mã: SMDEN000033
            - Công suất định mức: 5W
            - Nhiệt độ làm việc: -20°C ~ 65°C
            - Nhiệt độ màu: 6500K
            - Tuổi thọ bóng đèn LED: 50.000 giờ
            - Giá tiền: 869,000 đ
#Giới hạn:
- Chỉ trả lời khách hàng bằng tiếng việt
- Chỉ được phép sử dụng thông tin sản phẩm trong tài liệu
- Không được phép bịa thêm sản phẩm không có trong dữ liệu
- Không được phép bịa tên sản phẩm, thông tin sản phẩm, giá bán của sản phẩm. Khách hàng cần độ chính xác 100%, nếu không có yêu cầu khác ngoài việc tư vấn sản phẩm công ty từ chối khách hàng một cách nhẹ nhàng

#Thông tin sản phẩm
{context}
when answer the user:
  - if you don't know, just say that you don't know
  - if you don't know or you are not sure, ask for clarification
Avoid metioning that you obtained the information from the context
An answer using vietnames

Here are the histories between the human and the assistant:
"""
    )
    HUMAN_MESSAGE_TEMPLATE = "{human_input}"
    AI_MESSAGE_TEMPLATE = (
        "Xin chào, dựa trên thông tin tôi đã tìm thấy, tôi cung cấp cho bạn một số thông tin tham khảo:\n"
        "\n"
        "Kết luận các sản phẩm này giúp tiết kiệm điện và thân thiện với môi trường. "
        "Nếu bạn cần thêm thông tin chi tiết về từng sản phẩm, hãy cho tôi biết!!"
    )
    INDEX_ELASTIC = "chatbot"
    COMPARE_SPECIFICATIONS = ['so sánh', 'hơn']
    QUANTITY_SPECIFICATIONS = ['số lượng', 'bao nhiêu', 'mấy loại', 'số lượng sản phẩm', 'danh sách', 'tổng số', 'mấy', 'liệt kê số lượng', 'liệt kê', 'số lượng hiện còn']
    CHEAP_KEYWORDS = ["rẻ", "giá rẻ", "giá thấp", "bình dân", "tiết kiệm", "khuyến mãi", "giảm giá", "hạ giá", "giá cả phải chăng", "ưu đãi"]
    EXPENSIVE_KEYWORDS = ["giá đắt", "giá cao", "xa xỉ", "sang trọng", "cao cấp", "đắt đỏ", "chất lượng cao", "hàng hiệu", "hàng cao cấp", "thượng hạng"]
    TYPE_RASA = 'rasa'
    TYPE_LLM = 'LLM_predict'
    TYPE_IMAGE = 'image'
    raw_answer = ["Mình là trợ lý AI của VCC. Mình được tạo ra để hỗ trợ và giải đáp về các sản phẩm của VCC, hiện tại mình vẫn đang trong quá trình phát triển nên không phải lúc nào cũng đúng. Bạn có thể phản hồi để giúp mình cải thiện tốt hơn.",
                "Mình là trợ lý AI của VCC. Mình được tạo ra để hỗ trợ và giải đáp về các sản phẩm của VCC như: Thông tin sản phẩm, giá tiền, số lượng, thông số sản phẩm, . . . Hãy hỏi mĩnh những thông tin này để mình giúp đỡ."]
  
    can_not_res =  ['Rất tiếc về điều này. Tôi vẫn đang trong quá trình học và cải thiện, nên không thể giúp bạn với câu hỏi này vào lúc này. Hãy đặt câu hỏi khác để tôi có thể hỗ trợ bạn tốt hơn!',
                'Xin lỗi về sự bất tiện này. Tôi đang cố gắng nâng cao khả năng của mình mỗi ngày, nhưng hiện tại vẫn chưa đủ để xử lý câu hỏi này. Mong bạn thông cảm và tiếp tục hỏi câu hỏi khác nếu cần!',
                'Xin lỗi về sự phiền toái này. Tôi đang trong quá trình học hỏi và cải thiện từng ngày, nhưng vẫn chưa đủ để giải quyết câu hỏi của bạn. Hãy để tôi biết nếu có bất kỳ điều gì khác mà bạn cần giúp đỡ!',
                'Xin lỗi về sự bất tiện này. Hiện tại, tôi vẫn đang trong quá trình học và cải thiện, nên chưa thể giúp bạn với câu hỏi này. Tuy nhiên, tôi rất sẵn lòng hỗ trợ bạn với bất kỳ câu hỏi nào khác bạn có. Hãy đặt câu hỏi khác để tôi có thể giúp bạn tốt hơn!',
                'Xin lỗi, hiện tại tôi vẫn đang trong quá trình học và cải thiện, nên chưa thể giúp bạn với câu hỏi này. Tuy nhiên, tôi rất sẵn lòng hỗ trợ bạn với bất kỳ câu hỏi nào khác bạn có. Hãy đặt câu hỏi khác để tôi có thể giúp bạn tốt hơn!']

    rasa_button = [[
        {
        "payload": "Bạn muốn tra cứu hàng tồn kho?",
        "title": "Bạn muốn tra cứu hàng tồn kho?"
        },
        {
        "payload": "Bạn muốn tìm kiếm sản phẩm tương tự?",
        "title": "Bạn muốn tìm kiếm sản phẩm tương tự?"
        },
        {
        "payload": "Tôi muốn tìm sản phẩm Đèn năng mặt trời cao cấp?",
        "title": "Tôi muốn tìm sản phẩm Đèn năng mặt trời cao cấp?"
        },
        {
        "payload": "Thời gian lâu nhất mà đèn năng lượng mặt trời có thể sử dụng là bao lâu?",
        "title": "Thời gian lâu nhất mà đèn năng lượng mặt trời có thể sử dụng là bao lâu?"
        }],
        [
        {
        "payload": "Bạn muốn tra cứu hàng tồn kho?",
        "title": "Bạn muốn tra cứu hàng tồn kho?"
        },
        {
        "payload": "Bạn muốn tìm kiếm sản phẩm tương tự",
        "title": "Bạn muốn tìm kiếm sản phẩm tương tự"
        },
        {
        "payload": "Cho tôi bình nước nóng có dung tích 30 lít",
        "title": "Cho tôi bình nước nóng có dung tích 30 lít"
        },
        {
        "payload": "Đèn năng lượng mặt trời có câm nặng tầm 3kg",
        "title": "Đèn năng lượng mặt trời có câm nặng tầm 3kg"
        }],
        [
        {
        "payload": "Bạn muốn tra cứu hàng tồn kho?",
        "title": "Bạn muốn tra cứu hàng tồn kho?"
        },
        {
        "payload": "Tôi cần máy giặt nào có khối lượng giặt 10kg?",
        "title": "Tôi cần máy giặt nào có khối lượng giặt 10kg?"
        },
        {
        "payload": "Tôi quan tâm điều hòa có giá trên 10 triệu",
        "title": "Tôi quan tâm điều hòa có giá trên 10 triệu"
        },
        {
        "payload": "Đèn năng lượng mặt trời công suất 90W",
        "title": "Đèn năng lượng mặt trời công suất 90W"
        }],
        [
        {
        "payload": "Bạn muốn tra cứu hàng tồn kho?",
        "title": "Bạn muốn tra cứu hàng tồn kho?"
        },
        {
        "payload": "Tôi cần máy giặt nào có khối lượng giặt 10kg",
        "title": "Tôi cần máy giặt nào có khối lượng giặt 10kg"
        },
        {
        "payload": "So với điều hòa Daikin thì điều hòa MDV có ưu điểm là gì",
        "title": "So với điều hòa Daikin thì điều hòa MDV có ưu điểm là gì"
        },
        {
        "payload": "Bên bạn có bao nhiêu loại bếp từ công suất lớn?",
        "title": "Bên bạn có bao nhiêu loại bếp từ công suất lớn?"
        }]
    ]