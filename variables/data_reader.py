# variables/pandas_data_reader.py
import pandas as pd
import os

# Lấy đường dẫn tuyệt đối của thư mục chứa file pandas_data_reader.py
# current_dir = os.path.dirname(os.path.abspath(__file__))
# data_dir = os.path.join(current_dir, '..', 'data')

users_excel_path = users_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'data_user.xlsx')


# def get_users_data_with_pandas():
#     """
#     Đọc dữ liệu người dùng từ file CSV bằng pandas và trả về list of dictionaries.
#     """
#     try:
#         # Đọc CSV vào DataFrame
#         df = pd.read_csv(users_csv_path)
#         # Chuyển DataFrame thành list of dictionaries
#         # orient='records' sẽ tạo ra một list of dicts, mỗi dict là một hàng
#         return df.to_dict(orient='records')
#     except FileNotFoundError:
#         print(f"Lỗi: Không tìm thấy file CSV tại {_users_csv_path}")
#         return []
#     except Exception as e:
#         print(f"Lỗi khi đọc file CSV với pandas: {e}")
#         return []
def get_users_data_with_pandas(sheet_name='Sheet1'):
    """
    Đọc dữ liệu sản phẩm từ file Excel bằng pandas và trả về list of dictionaries.
    """
    try:
        # Đọc Excel vào DataFrame
        df = pd.read_excel(users_excel_path, sheet_name=sheet_name, engine='openpyxl', header=0)
        # Chuyển DataFrame thành list of dictionaries
        return df.to_dict(orient='records')
    
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file Excel tại {users_excel_path}")
        return []
    except Exception as e:
        print(f"Lỗi khi đọc file Excel với pandas: {e}")
        return []
    
# Hàm get_variables() mà Robot Framework sẽ gọi để lấy các biến động
def get_variables():
    return {
        "ROBOT_USERS_PANDAS": get_users_data_with_pandas(),

    }
    
# print(get_variables())