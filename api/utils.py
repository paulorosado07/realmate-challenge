def replace_value_type_webhook(value_type):
    return value_type.replace("NEW_CONVERSATION", "OPEN").replace("CLOSE_CONVERSATION", "CLOSED")