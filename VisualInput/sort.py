import subprocess
import json
import os

def sorting(wine_names):
    results_file = "vivino-results.json"  # File to accumulate results
    sorted_results_file = "sorted-vivino-results.json"  # File to store sorted results
    
    # Clear the results and sorted results files before starting the process
    with open(results_file, "w") as file:
        json.dump([], file)
    
    with open(sorted_results_file, "w") as file:
        json.dump([], file)

    for wine_name in wine_names:
        formatted_name = wine_name.replace(" ", "+").replace("&", "")
        try:
            # Call the Node.js script with a timeout
            subprocess.run(["node", "vivino.js", f"--name={formatted_name}"], timeout=60)  # 60 seconds timeout
            with open("vivino-out.json", "r") as file:
                data = json.load(file)
                if data.get("vinos"):
                    for wine in data["vinos"]:
                        if wine.get("price") is not None and wine.get("average_rating") is not None:
                            with open(results_file, "r+") as results:
                                # Load existing data
                                results_data = json.load(results)
                                # Append new data
                                results_data.append({
                                    "name": wine["name"],
                                    "price": wine["price"],
                                    "average_rating": wine["average_rating"],
                                    "image": wine["thumb"]
                                })
                                # Reset file pointer to the beginning and overwrite file
                                results.seek(0)
                                results.truncate()
                                json.dump(results_data, results, indent=2)
                            break  # Assuming you only want the first valid entry per wine name
        except (subprocess.TimeoutExpired, IOError, json.JSONDecodeError) as e:
            print(f"Skipping {wine_name} due to error: {e}")
    
    # At the end, read and sort the accumulated results
    with open(results_file, "r") as results:
        results_data = json.load(results)
        sorted_wines = sorted(results_data, key=lambda x: x["average_rating"], reverse=True)
        
        # Write the sorted list to the sorted results file
        with open(sorted_results_file, "w") as sorted_results:
            json.dump(sorted_wines, sorted_results, indent=2)

