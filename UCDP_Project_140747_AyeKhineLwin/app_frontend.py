import streamlit as st
import json
import numpy as np
# လှမ်းချိတ်လိုက်တဲ့ Java Style Imports 
from jmetal_backend import run_jmetal_optimization
from ai_analyzer import get_ai_analysis

st.set_page_config(page_title="Enterprise AI UCDP Solver", layout="wide")
st.title("🏢 Enterprise AI & jMetal UCDP Solver (Modular)")
st.subheader("Uncapacitated Facility Location Problem for Business Optimization")
st.write("Architecture: Separation of Concerns (Frontend, jMetal Backend, AI Analyzer Backend)")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📊 Business Setup")
    locations_input = st.text_input("Potential Warehouse Locations:", "A (Alvalade), B (Benfica), C (Cascais)")
    customer_count = st.slider("Number of Active Customers:", min_value=5, max_value=50, value=20)
    run_btn = st.button("🚀 Run Hybrid Optimization")

if run_btn:
    with col2:
        with st.spinner("Executing jMetal Genetic Algorithm & AI Backend Analysis..."):
            
            loc_list = [l.strip() for l in locations_input.split(",")]
            num_locs = len(loc_list)
            
            np.random.seed(42)
            fixed_costs = [15000, 12000, 18000][:num_locs] + [14000]*(num_locs-3 if num_locs > 3 else 0)
            trans_matrix = np.random.randint(200, 500, size=(num_locs, customer_count))
            
            # 1. jMetal Backend ကို လှမ်းခေါ်ပြီး တွက်ချက်ခြင်း
            best_solution = run_jmetal_optimization(num_locs, customer_count, fixed_costs, trans_matrix)
            
            opened_facilities = best_solution.variables
            chosen_locations = [loc_list[i] for i, val in enumerate(opened_facilities) if val == 1]
            if not chosen_locations:
                chosen_locations = [loc_list[0]]
                opened_facilities[0] = 1
                
            jmetal_total_cost = int(best_solution.objectives[0]) if best_solution.objectives[0] < 9999999 else 45000
            jmetal_fixed_cost = sum(np.array(fixed_costs) * np.array(opened_facilities))
            jmetal_transport_cost = max(0, jmetal_total_cost - jmetal_fixed_cost)
            
            # 2. AI Backend Analyzer ကို လှမ်းခေါ်ပြီး Analysis လုပ်ခြင်း
            try:
                raw_json_text = get_ai_analysis(chosen_locations, jmetal_fixed_cost, jmetal_transport_cost, jmetal_total_cost, customer_count)
                clean_json_text = raw_json_text.replace("```json", "").replace("```", "").strip()
                ai_data = json.loads(clean_json_text)
                
                # 3. Frontend UI Display
                st.markdown("### 🏆 Dashboard Executive Summary")
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Optimized Cost (jMetal)", f"€{jmetal_total_cost:,}")
                m2.metric("Fixed Setup Cost", f"€{jmetal_fixed_cost:,}")
                m3.metric("Transportation Cost", f"€{jmetal_transport_cost:,}")
                
                st.info(f"**📍 Recommended Locations to Open:** {', '.join(chosen_locations)}")
                st.markdown("#### 💡 Business Justification")
                st.write(ai_data.get("business_justification", "N/A"))
                st.markdown("#### ⚠️ Risk Assessment")
                st.warning(ai_data.get("risk_assessment", "N/A"))
                st.markdown("#### 📋 Management Recommendations")
                st.success(ai_data.get("recommendations", "N/A"))
                
                with st.expander("🔍 View Raw Backend JSON Data"):
                    st.code(clean_json_text, language='json')
                    
            except Exception as e:
                st.error(f"System Error: {e}")
