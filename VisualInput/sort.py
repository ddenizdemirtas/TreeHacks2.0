import subprocess
import json
import os

# Example list of filtered wine names
#wine_names = ['colterenzio pinot grigio', 'graham beck chenin blanc', 'charles & charles syrah rose', 'novelty hill viognier', 'kung fu girl riesling', 'pinot noir', 'bethel heights pinot noir estate', 'boira sangiovese', 'brandborg bench lands pinot noir', 'chesler, cabernet franc, merlot,', 'cabernet sauvignon', 'chianti classico savignola paolina']
wine_names = ['colterenzio pinot grigio']


def get_wine_info(wine_name):
    formatted_name = wine_name.replace(" ", "+")
    try:
        # Call the Node.js script with a timeout
        subprocess.run(["node", "vivino.js", f"--name={formatted_name}"], timeout=60)  # 60 seconds timeout
        with open("vivino-out.json", "r") as file:
            data = json.load(file)
            if data.get("vinos"):
                # Loop through the vinos to find the first one with both price and average_rating
                for wine in data["vinos"]:
                    if wine.get("price") is not None and wine.get("average_rating") is not None:
                        # Return as soon as we find a wine with both fields
                        return {
                            "name": wine["name"],
                            "price": wine["price"],
                            "average_rating": wine["average_rating"]
                        }
    except (subprocess.TimeoutExpired, IOError, json.JSONDecodeError) as e:
        print(f"Skipping {wine_name} due to error: {e}")
    return None

# Ensure vivino-out.json exists to prevent errors
open("vivino-out.json", "w").close()

wines_info = []

for wine_name in wine_names:
    wine_info = get_wine_info(wine_name)
    if wine_info:
        wines_info.append(wine_info)
    # Optionally clear vivino-out.json content for the next iteration
    open("vivino-out.json", "w").close()

# Sort the list of wines based on average rating (descending)
sorted_wines = sorted(wines_info, key=lambda x: x["average_rating"], reverse=True)

# Display the sorted list
print(json.dumps(sorted_wines, indent=2))



