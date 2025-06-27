referrals_db = {}  # Replace with Cosmos DB later

def save_referral(user_id, email_list):
    if not isinstance(email_list, list) or len(email_list) != 3:
        return False, "You must provide exactly 3 emails."

    referrals_db[user_id] = {
        "emails": email_list,
        "unlocked": True
    }
    return True, "Referrals submitted successfully."
