if logged_in_user:
    user_id, *_, role = logged_in_user
    
    if role == "donor":
        donor_dashboard(donation, campaign, event, user_id, db)
    elif role == "organization":
        organization_dashboard(campaign, event, user_id)
    else:
        print(f"❌ Unknown role '{role}'. Access denied.")
else:
    print("❌ Login failed. Please check your credentials.")
