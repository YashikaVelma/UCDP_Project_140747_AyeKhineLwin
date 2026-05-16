import ollama

def get_ai_analysis(chosen_locations, jmetal_fixed_cost, jmetal_transport_cost, jmetal_total_cost, customer_count):
    user_message = f"""You are a Senior Supply Chain Consultant. We solved an Uncapacitated Facility Location Problem (UCDP) using jMetal's Genetic Algorithm.
    
    Here are the mathematical results from jMetal:
    - Selected locations to open: {chosen_locations}
    - Fixed setup costs: {jmetal_fixed_cost} EUR
    - Variable transportation costs: {jmetal_transport_cost} EUR
    - Total optimized cost: {jmetal_total_cost} EUR
    - Number of customers served: {customer_count}
    
    Please provide a strategic business analysis based on these jMetal numbers.
    Your output must be in STRICT JSON format ONLY, using exactly these keys:
    1. business_justification (Explain why this combination makes business sense in terms of efficiency)
    2. risk_assessment (Identify 1 potential supply chain risk for this setup)
    3. recommendations (Provide 1 strategic next step for the management)
    """
    
    response = ollama.chat(model='qwen2.5:3b', messages=[{'role': 'user', 'content': user_message}])
    return response['message']['content']
