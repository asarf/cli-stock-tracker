def check_notifications(data, threshold):
    for idx in data:
        if abs(idx["percentage_change"]) >= threshold:
            print(f'[ALERT]: {idx["index_name"]} ({idx["country"]}) changed by {idx["percentage_change"]}%! (Threshold: {threshold}%)')