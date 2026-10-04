from backend.ai.service import generate_knowledge

k = generate_knowledge({
    "name": "Smart Irrigation System",
    "description": "An ESP32 reads soil moisture and switches a relay-controlled pump to water plants automatically, so plants are not over or under watered when nobody is home.",
    "components": [{"name": "ESP32"}, {"name": "Soil moisture sensor"}, {"name": "Relay module"}, {"name": "Water pump"}],
    "tasks": [{"title": "Sensor integration", "done": True}, {"title": "Relay control", "done": True}, {"title": "Enclosure", "done": False}],
    "notes": "",
})
print(k.model_dump_json(indent=2))
