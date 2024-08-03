def suggest_plants(sunlight, watering, size, window_area, dominant_colors):
    plant_suggestions = []
    
    if window_area > 100000:
        plant_suggestions.extend(["Fiddle Leaf Fig 🌿", "Snake Plant 🌵"])
    else:
        plant_suggestions.extend(["ZZ Plant 🪴", "Pothos 🍃"])
    
    if dominant_colors[0][0] > 200:
        plant_suggestions.append("Peace Lily 🌸")

    if sunlight.lower() in ["high", "bright"]:
        plant_suggestions.append("Fiddle Leaf Fig 🌿")
    else:
        plant_suggestions.append("ZZ Plant 🪴")
        
    if watering.lower() in ["weekly", "bi-weekly"]:
        plant_suggestions.append("Pothos 🍃")
    else:
        plant_suggestions.append("Cactus 🌵")
        
    if size.lower() in ["small", "medium"]:
        plant_suggestions.append("Peace Lily 🌸")
    else:
        plant_suggestions.append("Rubber Plant 🌳")
    
    plant_suggestions = list(set(plant_suggestions))
    plant_suggestions.sort()
    
    return plant_suggestions