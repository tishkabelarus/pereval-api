def validate_pereval_data(data):
    """Простая валидация для теста"""
    required_fields = ['beautyTitle', 'title', 'coords', 'level', 'user']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Проверка пользователя
    user = data.get('user', {})
    if not user.get('email') or not user.get('fam') or not user.get('name'):
        return False, "Missing required user fields"
    
    return True, ""