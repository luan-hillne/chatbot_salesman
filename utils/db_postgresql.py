import psycopg2
import json
import logging
class DatabaseHandler:
    def __init__(self):
        dbname = "ai_services"
        user = "ai_chatbot_admin"
        password = "Vcc#2024#"
        host = "10.248.243.162"
        port = "5432"
        # self.shema = "chat_saleman"
        self.conn = psycopg2.connect( f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
            
    def insert_user(self, user_id, user_name, address, gender, role):
        check_user_query = "SELECT user_id FROM chat_saleman.users WHERE user_id = %s"
        with self.conn.cursor() as cur:
            cur.execute(check_user_query, (user_id,))
            user = cur.fetchone()

            if user is None:
                insert_user_query = """
                INSERT INTO chat_saleman.users (user_id, user_name, address, gender, role) VALUES (%s, %s, %s, %s, %s) RETURNING user_id;
                """
                
                with self.conn.cursor() as cur:
                    cur.execute(insert_user_query, (user_id, user_name, address, gender, role))
                    self.conn.commit()
            logging.info('======== insert_user sucessfully! ==========}')
            print("insert_user sucessfully!")

    def insert_chat_message(self, user_id, session_id, created_date, message):
        try:
            check_session_query = "SELECT session_id, message FROM chat_saleman.chat_message WHERE session_id = %s"
            
            with self.conn.cursor() as cur:
                cur.execute(check_session_query, (session_id,))
                session = cur.fetchone()
                # print('session', session)
                if session:
                    # print('message', message)
                    # message_to_list = current_message + message
                    # # message_to_list.append(message)
                    # # updated_message_str = json.dumps(updated_message)
                    # print('message', message_to_list)
                    update_chat_message_query = """
                        UPDATE chat_saleman.chat_message
                        SET message = %s
                        WHERE session_id = %s;
                    """
                    cur.execute(update_chat_message_query, (json.dumps(message), session_id))
                    self.conn.commit()
                else:
                    insert_chat_message_query = """INSERT INTO chat_saleman.chat_message (user_id, session_id, created_date, message) VALUES (%s, %s, %s, %s);"""
                    
                    with self.conn.cursor() as cur:
                        cur.execute(insert_chat_message_query, (user_id, session_id, created_date, json.dumps(message)))
                        self.conn.commit()
                logging.info('======== insert_chat_message sucessfully! ==========}')
                print("insert_chat_message sucessfully!")
        except Exception as e:
            print("insert_chat_message: ",e)
    
    def logs_chat_saleman(self, user_id, session_id, created_date, input_type, total_token, status, error_code, human, ai):
        try:        
            insert_user_query = """
            INSERT INTO chat_saleman.logs_chat_saleman (user_id, session_id, created_date, input_type, total_token, status, error_code, human, ai) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            with self.conn.cursor() as cur:
                cur.execute(insert_user_query, (user_id, session_id, created_date, input_type, total_token, status, error_code, human, ai))
                self.conn.commit()
            logging.info('======== logs_chat_saleman sucessfully! ==========}')
            print('logs_chat_saleman sucessfully!')
        except Exception as e:
            print("logs_chat_saleman: ",e)
            
    def llm_key_table(self):
        
        check_session_query = "SELECT llm_key FROM chat_saleman.llm_key_table where status = true"
        with self.conn.cursor() as cur:
            cur.execute(check_session_query)
            self.conn.commit()
            llm_key = cur.fetchall()
            # print(llm_key[0][0])
            return llm_key
    
# Usage example
# db_handler = DatabaseHandler()
# user_id = '6534623'
# session_id = '02496'
# human = 'human'
# ai = 'ai'
# message = {'recipient_id': 'test', 'text': 'LLM_predict'}
# db_handler.insert_user(user_id, '','VCC center','Nam', 'job')
# db_handler.insert_chat_message(user_id, session_id,  '2024-07-25 11:05:00', message)
# db_handler.logs_chat_saleman(user_id, session_id, '2024-07-25 11:05:00', 'image','3242', '0', 'failed update table!',  human, ai)

# print(db_handler.llm_key_table())