import requests

def fetch_sales_data(api_key, start_date, end_date):
    if not api_key:
        raise ValueError("API ключ не указан.")

    url = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
        "Content-Type": "application/json; charset=UTF-8"
    }
    params = {"dateFrom": start_date, "dateTo": end_date}

    try:
        response = requests.get(url, params=params, headers=headers)
        
        response.raise_for_status()  
        
        if response.status_code == 401:
            raise ValueError("Неверный API-ключ. Проверьте ваш API-ключ и попробуйте снова.")
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        raise ConnectionError("Ошибка сети попробуйте позже.")
    
    except ValueError as e:
        print(f"Ошибка: {e}")
        raise ValueError(f"Ошибка: {e}")

    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        raise RuntimeError("Произошла неизвестная ошибка. Попробуйте позже.")