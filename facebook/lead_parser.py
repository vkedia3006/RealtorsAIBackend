def extract_lead_data(value: dict) -> dict | None:
    field_map = {f["name"]: f["values"][0] for f in value.get("field_data", []) if f["values"]}
    name = field_map.get("full_name")
    email = field_map.get("email")
    phone = field_map.get("phone_number")

    if name and email and phone:
        return {
            "name": name,
            "email": email,
            "phone": phone
        }
    return None
