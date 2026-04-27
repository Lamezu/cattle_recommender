import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.main_controller import MainController

def verify_integration():
    print("=== TEST DE VERIFICACION DEL BACKEND INTEGRADO ===\n")
    
    try:
        controller = MainController()
        
        # 1. Probar que podemos obtener un granjero real
        farmers = controller.get_farmers()
        if not farmers:
            print("[X] Error: No se encontraron granjeros.")
            return
        test_farmer = farmers[0].farmer_id
        print(f"[OK] Granjero de prueba: {test_farmer}")
        
        # 2. Probar Pestaña Recomendadas
        recs = controller.get_personalized_recommendations(test_farmer)
        print(f"[OK] Recomendaciones personalizadas: {len(recs)} encontradas.")
        
        # 3. Probar Pestaña Más Compradas
        purchased = controller.get_most_purchased()
        print(f"[OK] Mas compradas: {len(purchased)} encontradas.")
        if purchased:
            print(f"    - Ejemplo: {purchased[0].name} (ID: {purchased[0].cow_id})")
            
        # 4. Probar Similares (usando la primera vaca encontrada)
        if purchased:
            sims = controller.get_similar_cows(purchased[0].cow_id)
            print(f"[OK] Similares a {purchased[0].cow_id}: {len(sims)} encontradas.")

        print("\n=== VERIFICACION COMPLETADA CON EXITO ===")
        
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")

if __name__ == "__main__":
    verify_integration()
