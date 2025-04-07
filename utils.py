from tabulate import tabulate

def display_indices_table(data):
    table = [[
        idx["country"], idx["index_name"], idx["current_value"], 
        f'{idx["percentage_change"]}% {"+" if idx["percentage_change"] >=0 else "-"}'
    ] for idx in data]

    print(tabulate(table, headers=["Country", "Index", "Current Value", "% Change"], tablefmt="simple"))