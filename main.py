from datetime import datetime

# --- LÓGICA DE NEGOCIO ---
def obtener_precios():
    """Retorna el diccionario con la estructura de costos por tipo de cliente."""
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

# --- VALIDACIONES ---
def validar_numero(etiqueta, max_digitos=10):
    while True:
        dato = input(f"{etiqueta}: ")
        if dato.isdigit() and len(dato) <= max_digitos:
            return dato
        print(f"Error: Debe ser numérico (máx {max_digitos} dígitos).")

def validar_fecha():
    while True:
        fecha_input = input("Fecha de la Cita (DD/MM/AAAA): ")
        try:
            fecha_dt = datetime.strptime(fecha_input, "%d/%m/%Y")
            if fecha_dt.year < 2026:
                print("Error: El año debe ser 2026 o posterior.")
                continue
            return fecha_input
        except ValueError:
            print("Error: Formato inválido.")

# --- FLUJO PRINCIPAL ---
def ejecutar_consultorio():
    clientes = []
    precios = obtener_precios()
    
    print("=== SISTEMA ODONTOLÓGICO - REGISTRO DE PACIENTES ===")
    
    while True:
        print("\n" + "="*40)
        print(" INGRESO DE DATOS DEL PACIENTE")
        print("="*40)
        
        # Recolección de datos básicos
        cedula = validar_numero("Cédula")
        nombre = input("Nombre completo: ")
        telefono = validar_numero("Teléfono/Celular")
        
        print("\nOpciones de afiliación: Particular, EPS, Prepagada")
        tipo_cliente = input("Tipo de Cliente: ").strip().capitalize()
        if tipo_cliente not in precios:
            print("Tipo no válido, se asignará Particular por defecto.")
            tipo_cliente = "Particular"

        fecha = validar_fecha()
        
        total_atenciones = 0
        lista_procedimientos = []
        conteo_extracciones = 0

        # Bucle de procedimientos para el mismo paciente
        while True:
            print("\nProcedimientos: Limpieza, Calzas, Extraccion, Diagnostico")
            atencion = input("Seleccione Procedimiento: ").strip().capitalize()
            
            # Obtener precio según tipo de cliente
            valor_unitario = precios[tipo_cliente]["atenciones"].get(atencion, 0)
            
            if atencion in ["Limpieza", "Diagnostico"]:
                cant = 1
            else:
                try:
                    cant = int(input(f"¿Cuántas {atencion} desea realizar?: "))
                except ValueError:
                    cant = 1
            
            if atencion == "Extraccion":
                conteo_extracciones += cant

            subtotal_proc = valor_unitario * cant
            total_atenciones += subtotal_proc
            lista_procedimientos.append(f"{atencion} (x{cant})")
            
            otro_proc = input("¿Desea agregar otro procedimiento a este cliente? (s/n): ").lower()
            if otro_proc != 's':
                break

        # Cálculos económicos
        valor_cita_base = precios[tipo_cliente]["valor_cita"]
        valor_total_cliente = valor_cita_base + total_atenciones

        # --- GENERACIÓN DEL CUADRO DE REGISTRO ---
        print("\n" + "┌" + "─"*50 + "┐")
        print(f"│{'RESUMEN DE REGISTRO':^50}│")
        print("├" + "─"*22 + "┬" + "─"*27 + "┤")
        print(f"│ {'CÉDULA':<20} │ {cedula:<25} │")
        print(f"│ {'NOMBRE':<20} │ {nombre[:25]:<25} │")
        print(f"│ {'CELULAR':<20} │ {telefono:<25} │")
        print(f"│ {'TIPO DE CLIENTE':<20} │ {tipo_cliente:<25} │")
        print(f"│ {'FECHA CITA':<20} │ {fecha:<25} │")
        print(f"│ {'PROCEDIMIENTOS':<20} │ {', '.join(lista_procedimientos)[:25]:<25} │")
        print("├" + "─"*22 + "┼" + "─"*27 + "┤")
        print(f"│ {'TOTAL A PAGAR':<20} │ ${valor_total_cliente:,.0f} {"":<16} │")
        print("└" + "─"*50 + "┘")

        # Guardado en base de datos temporal (lista)
        clientes.append({
            "cedula": cedula,
            "nombre": nombre,
            "tipo_cliente": tipo_cliente,
            "procedimientos": ", ".join(lista_procedimientos),
            "valor_pagar": valor_total_cliente,
            "extracciones": conteo_extracciones,
            "fecha": fecha
        })

        if input("\n¿Registrar un nuevo paciente diferente? (s/n): ").lower() != 's':
            break

    # --- REPORTES FINALES AL CERRAR ---
    if not clientes: return
    
    ingresos_totales = sum(c["valor_pagar"] for c in clientes)
    print(f"\nSISTEMA CERRADO. Total de pacientes atendidos: {len(clientes)}")
    print(f"Ingresos totales del día: ${ingresos_totales:,.0f}")

if __name__ == "__main__":
    ejecutar_consultorio()
    
prueba commit