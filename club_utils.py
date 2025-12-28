from db import get_connection

def is_club_member(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT 1 FROM club_users WHERE user_id = %s LIMIT 1",
        (user_id,)
    )
    
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result is not None
