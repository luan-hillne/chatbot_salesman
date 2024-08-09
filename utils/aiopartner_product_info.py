import schedule
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import pandas as pd

def db():
    host = "10.248.242.90"
    port = 5000
    dbname = "vcc_dw"
    username = "postgres"
    password = "Vcc@123#20200"

    encoded_password = quote_plus(password)
    # Tạo URL kết nối
    dsn = f"postgresql+psycopg2://{username}:{encoded_password}@{host}:{port}/{dbname}"
    # Tạo engine kết nối
    engine = create_engine(dsn)
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    query = "select * from vcc_cntt.online_cntt_ai_project_ds_san_pham_aio_partner"
    result = session.execute(query)
    rows = result.fetchall()
    columns = result.keys()
    # Close the session
    session.close()
    # Convert the result to a Pandas DataFrame
    df = pd.DataFrame(rows, columns=columns)
    return df

def job():
    df = db()
    # Lưu dữ liệu vào file Excel
    file_path = "./ChatBot_Extract_Intent/data/product_final.xlsx"  # Thay đổi đường dẫn này thành đường dẫn của bạn
    df.to_excel(file_path, index=False)
    print(f"Data saved to {file_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

# # Lập lịch để chạy công việc vào lúc 6 giờ sáng hàng ngày
# schedule.every().day.at("18:14").do(job)

# while True:
#     print(time.strftime('%Y-%m-%d %H:%M:%S'))
#     schedule.run_pending()
#     time.sleep(60)  # Chờ 1 phút trước khi kiểm tra lại
job()