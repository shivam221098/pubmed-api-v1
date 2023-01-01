from api import API
max_results = 1_00_000  # upto this number we want results

params = {
    "term": """("Diffuse Large B-cell Lymphoma" [MeSH] OR "Diffuse, Large B-Cell, Lymphoma" [MeSH] OR "Diffuse Large 
    B Cell Lymphoma" [MeSH] OR "Lymphoma, Large Cell, Diffuse" [MeSH] OR "Lymphoma, Large-Cell, Diffuse" OR "Diffuse 
    Large-Cell Lymphoma" [MeSH] OR "Diffuse Large Cell Lymphoma" [MeSH] OR "Diffuse Large-Cell Lymphomas" [MeSH] OR 
    "Lymphoma, Large Lymphoid, Diffuse" OR "Large Lymphoid Lymphoma, Diffuse" [MeSH] OR "Large-Cell Lymphoma, 
    Diffuse" [MeSH] OR "Large Cell Lymphoma, Diffuse" [MeSH] OR "Lymphoma, Diffuse Large-Cell" [MeSH] OR "Lymphoma, 
    Diffuse Large Cell" [MeSH] OR "Diffuse Large B-cell Lymphoma" [Title/Abstract] OR "Diffuse Large B Cell Lymphoma" 
    [Title/Abstract]  OR "Diffuse Large-Cell Lymphoma" [Title/Abstract] OR "Diffuse Large Cell Lymphoma" [
    Title/Abstract] OR "Diffuse Large-Cell Lymphomas" [Title/Abstract] OR "Diffuse Large Cell Lymphomas" [
    Title/Abstract] OR "DLBCL" [Title/Abstract] AND ("Epidemiology"[MeSH] OR "Prevalence"[MeSH] OR "Incidence"[MeSH] 
    OR "Epidemiology"[Title/Abstract] OR "endemics"[Title/Abstract] OR "epidemics"[Title/Abstract] OR "frequency"[
    Title/Abstract] OR "incidence"[Title/Abstract] OR "morbidity"[Title/Abstract] OR "occurrence"[Title/Abstract] OR 
    "outbreaks"[Title/Abstract] OR "Prevalence"[Title/Abstract] OR "surveillance"[Title/Abstract] OR 
    "epidemiological"[Title/Abstract] OR "epidemiologic"[Title/Abstract] OR "Incidence"[Title/Abstract] OR "age of 
    onset"[MeSH] OR "undiagnosed disease"[MeSH] OR "life expectancy"[MeSH] OR "disease hotspots"[MeSH] OR "medical 
    geography"[MeSH] OR "life expectancy"[MeSH]))""",
    "retmax": max_results
}
x = API().get_response(params=params)
print(x)