resources = {
    "Electricista" : 3,
    "Plomero" : 2,
    "Carpintero" : 2,
    "Obrero" : 5,
    "Operador de camión de carga" : 2,
    "Técnico de redes": 3,
    "Técnico de domótica": 3,
    "Camión de carga" : 2,
    "Sensores y dispositivos de domótica" : 5,
    "Materiales de construcción" : 5,
    "Kit de herramientas" : 5,
    "Equipos de red" : 5,
    "Accesorios de fontanería" : 5,
    "Accesorios de electricidad" : 5}

rules = {
    "Electricista": {"include": ["Accesorios de electricidad"], "exclude": ["Plomero", "Accesorios de fontanería"]},
    "Accesorios de electricidad": {"include": ["Electricista"], "exclude": ["Plomero", "Accesorios de fontanería"]},
    "Plomero": {"include": ["Accesorios de fontanería"], "exclude": ["Electricista", "Accesorios de electricidad"]},
    "Accesorios de fontanería": {"include": ["Plomero"], "exclude": ["Electricista", "Accesorios de electricidad"]},
    "Carpintero": {"include": ["Kit de herramientas"], "exclude": ["Plomero", "Accesorios de fontanería"]},
    "Kit de herramientas": {"include": [], "exclude": []},
    "Obrero": {"include": ["Kit de herramientas"], "exclude": []},
    "Materiales de construcción": {"include": ["Obrero", "Camión de carga"], "exclude": []},
    "Operador de camión de carga" : {"include": ["Camión de carga"], "exclude": []},
    "Camión de carga": {"include": ["Operador de camión de carga"], "exclude": []},
    "Técnico de redes": {"include": ["Equipos de red", "Kit de herramientas"], "exclude": []},
    "Equipos de red": {"include": ["Técnico de redes"], "exclude": []},
    "Técnico de domótica": {"include": ["Sensores y dispositivos de domótica", "Kit de herramientas"], "exclude": []},
    "Sensores y dispositivos de domótica": {"include": ["Técnico de domótica"], "exclude": []}}


