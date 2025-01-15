from sympy import Interval

# Masse: 800-3000 [kg]
masse = Interval(800, 3000) # Betrachtet einen PKW

# Reibwert
haftreibungReifen = Interval(0.5, 0.9) # Betrachtet einen Gummireifen auf einem Asphalt bei Nässe und Trockenheit
gleitreibungReifen = Interval(0.15, 0.3) # Betrachtet einen Gummireifen auf einem Asphalt bei Nässe und Trockenheit

# Luftwiderstandskoeffizient
cwWert = Interval(0.21, 0.46) # Mögliche Werte bei modernen PKWs

# Stirnfläche des Autos [m²]
stirnflaeche = Interval(1.8, 3.4) # Mögliche Werte bei PKWs bis 3 Tonnen

# Luftdichte [kg/m³]
luftdichte = Interval(1.2922, 1.1455) # 0-35 Grad Celsius

# Kurvenneigung [Grad]
kurvenneigung = Interval(0, 89) # 0-89 Grad

# Lenkwinkel [Grad]
lenkwinkel = Interval(0, 80) # 0-80 Grad