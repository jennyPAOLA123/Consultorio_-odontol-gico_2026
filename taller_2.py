from datetime import datetime, timedelta

# --- LÓGICA DE NEGOCIO ---
def obtener_precios():
    return {
        "Particular": {
            "valor_cita": 80000,
            "atenciones": {"Limpieza": 60000, "Calzas": 80000, "Extraccion": 100000, "Diagnostico": 50000}
        },
        "EPS": {
            "valor_cita": 5000, 
            "atenciones": {"Limpieza": 0, "Calzas": 40000, "Extraccion": 40000, "Diagnostico": 0}
        },
        "Prepagada": {
            "valor_cita": 30000, 
            "atenciones": {"Limpieza": 0, "Calzas": 10000, "Extraccion": 10000, "Diagnostico": 0}
        }
    }

def generar_factura(p, tipo):
    print("\n" + "╔" + "═"*48 + "╗")
    print("║" + f"{'FACTURA DE SERVICIOS ODONTOLÓGICOS':^48} " + "║")
    print("╠" + "═"*48 + "╣")
    print(f"║ FECHA: {p['fecha']:<15} HORA: {p['hora']:<15} ║")
    print(f"║ PACIENTE: {p['nombre'][:36]:<37} ║")
    print(f"║ CÉDULA: {p['cedula']:<39} ║")
    print(f"║ TIPO: {tipo:<41} ║")
    status = '🚨 URGENCIA' if p['urgente'] else 'CITA NORMAL'
    print(f"║ ESTADO: {status:<38} ║")
    print("╟" + "─"*48 + "╢")
    print(f"║ DETALLE: {p['procedimientos'][:38]:<38} ║")
    print(f"║ TOTAL A PAGAR: ${p['valor_pagar']:>29,.0f} ║")
    print("╚" + "═"*48 + "╝")

# --- VALIDACIONES ---
def validar_numero(etiqueta, max_digitos=10):
    while True:
        dato = input(f"{etiqueta}: ")
        if dato.isdigit() and len(dato) <= max_digitos:
            return dato
        print(f"Error: Debe ser numérico.")

def validar_tipo_cliente(precios):
    while True:
        tipo = input("  • Tipo (Particular / EPS / Prepagada): ").strip().capitalize()
        if tipo.upper() == "EPS": tipo = "EPS"
        if tipo in precios: return tipo
        print(f"Error: Opción no válida.")

def validar_fecha():
    while True:
        fecha_input = input("  • Fecha de la Cita (DD/MM/AAAA): ")
        try:
            return datetime.strptime(fecha_input, "%d/%m/%Y")
        except ValueError:
            print("    Error: Formato inválido.")

# --- FLUJO PRINCIPAL ---
def ejecutar_consultorio():
    cola_atencion = []      
    pila_contingencia = []  
    precios = obtener_precios()
    proxima_hora_libre = datetime.strptime("08:00", "%H:%M")
    
    print("\n" + "█" + "▀"*60 + "█")
    print("█" + f"{'SISTEMA ODONTOLÓGICO - GESTIÓN 2026':^60}" + "█")
    print("█" + "▄"*60 + "█")
    
    while True:
        es_urgente = input("\n  • ¿Es una URGENCIA médica? (s/n): ").lower() == 's'
        cedula = validar_numero("  • Cédula")
        nombre = input("  • Nombre completo: ").title()
        tipo_cliente = validar_tipo_cliente(precios)
        fecha_dt = validar_fecha()
        hora_asignada = proxima_hora_libre.strftime("%I:%M %p")

        total_procedimientos = 0
        lista_procedimientos = []
        tiene_extraccion = False
        hubo_procedimientos_con_costo = False

        while True:
            print("\n    Opciones: Limpieza, Calzas, Extraccion, Diagnostico")
            atencion = input("    Seleccione Procedimiento: ").strip().capitalize()
            
            if atencion not in precios[tipo_cliente]["atenciones"]:
                print(f"    [!] No existe.")
                continue

            valor_unitario = precios[tipo_cliente]["atenciones"][atencion]
            
            # --- VALIDACIÓN DE CANTIDAD CON LÍMITE DE EXTRACCIONES ---
            if atencion in ["Limpieza", "Diagnostico"]:
                cant = 1
            else:
                while True:
                    try:
                        cant = int(input(f"    ¿Cuántas {atencion}?: "))
                        # Límite de 2 extracciones
                        if atencion == "Extraccion" and cant > 2:
                            print("    [!] Error: El límite máximo permitido es de 2 extracciones.")
                            continue
                        if cant > 0: break
                        else: print("    [!] Error: La cantidad debe ser mayor a 0.")
                    except ValueError:
                        print("    [!] Error: Ingrese un número válido.")

            if atencion == "Extraccion": tiene_extraccion = True
            if valor_unitario > 0: hubo_procedimientos_con_costo = True
            
            total_procedimientos += (valor_unitario * cant)
            lista_procedimientos.append(f"{atencion} (x{cant})" + (" [CUBIERTO]" if valor_unitario == 0 else ""))
            
            if input("    ¿Agregar otro procedimiento? (s/n): ").lower() != 's':
                break

        # Lógica de cobro
        if tipo_cliente == "Particular":
            valor_final = precios[tipo_cliente]["valor_cita"] + total_procedimientos
        else:
            if total_procedimientos == 0:
                valor_final = 0
            elif hubo_procedimientos_con_costo:
                valor_final = total_procedimientos
            else:
                valor_final = precios[tipo_cliente]["valor_cita"]

        datos_paciente = {
            "cedula": cedula, "nombre": nombre, "procedimientos": ", ".join(lista_procedimientos),
            "valor_pagar": valor_final, "urgente": es_urgente, 
            "fecha_dt": fecha_dt, "fecha": fecha_dt.strftime("%d/%m/%Y"), "hora": hora_asignada,
            "tiene_extraccion": tiene_extraccion
        }

        # --- GESTIÓN DE ESTRUCTURAS ---
        cola_atencion.append(datos_paciente)
        
        if es_urgente and tiene_extraccion:
            pila_contingencia.append(datos_paciente)
            pila_contingencia.sort(key=lambda x: x['fecha_dt'], reverse=True)

        generar_factura(datos_paciente, tipo_cliente)
        proxima_hora_libre += timedelta(minutes=30)

        if input("\n¿Registrar otro paciente? (s/n): ").lower() != 's': break

    # --- INFORMES FINALES ---
    # (Se mantienen iguales para mostrar la Cola y la Pila correctamente)
    if cola_atencion:
        print("\n" + "═"*126)
        print(f"{'COLA DE ATENCIÓN DIARIA (ORDEN DE LLEGADA)':^126}")
        print("═"*126)
        for p in cola_atencion:
            print(f"| {p['hora']:<10} | {p['cedula']:<12} | {p['nombre'][:25]:<25} | {p['fecha']:<12} | ${p['valor_pagar']:<8,.0f} | {p['procedimientos'][:35]:<35} |")

    if pila_contingencia:
        print("\n" + "█"*126)
        print(f"{'PILA DE CONTINGENCIA: PRIORIDAD EXTRACCIONES URGENTES':^126}")
        print("█"*126)
        print(f"{'Llamar de arriba hacia abajo (Top de la Pila / Fecha más cercana)':^126}")
        print("-"*126)
        for p in reversed(pila_contingencia):
            print(f"| PRIORIDAD ALTA | {p['cedula']:<12} | {p['nombre'][:25]:<25} | FECHA CITA: {p['fecha']:<12} | TRAMITE: Extracción |")
        print("█"*126)

if __name__ == "__main__":
    ejecutar_consultorio()
