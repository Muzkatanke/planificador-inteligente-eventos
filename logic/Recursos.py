from logic.Datos import resources, rules

def check_resources_inclusion(new_event_resources, event_actives, alert, available_amount):
    valid = True

    for resource in list(new_event_resources.keys()):
        if resource in rules:
            included = rules[resource]["include"]
            for x in included: 
                if x in new_event_resources:
                    continue
                else:
                    alert(f"ADVERTENCIA: Su evento requiere la inclusión obligatoria del recurso '{x}', ya que {resource} lo necesita para funcionar.")
                    current_availability = available_amount(x, new_event_resources, event_actives, resources)
                    if current_availability <= 0:
                        alert(f"ERROR: El recurso '{x}' no se encuentra actualmente disponible.")
                        valid = False
                    else:
                        new_event_resources[x] = new_event_resources.get(x, 0) + 1
                        alert(f"El recurso '{x}' ha sido incluido automáticamente.")
    return valid

def check_resources_exclusion(new_event_resources):
    excluded_set = set()
    
    for resource in list(new_event_resources.keys()):
        if resource in rules:
            excluded = rules[resource]["exclude"]
            for x in excluded: 
                if x not in new_event_resources:
                    excluded_set.add(x)    
    return excluded_set
 