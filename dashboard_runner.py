from explainerdashboard import ExplainerDashboard
import dash_bootstrap_components as dbc
import sys
from xai_functions import load_model

port = int(sys.argv[1])
explainer = load_model(sys.argv[2])

dashboard = ExplainerDashboard(explainer, ["importances", "model_summary", "contributions", "whatif", "shap_dependence"], 
               title="Leek fertilizer end-user XAI service", 
               bootstrap=dbc.themes.SOLAR,
               hide_header=False, debug=False, use_reloader=False)
print("Starting dashboard on port", port, "for explainer", sys.argv[2], "...")
dashboard.run(port=port)