import numpy as np
import pandas as pd
# Set pandas view options
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# filter warnings messages from the notebook
import warnings
warnings.filterwarnings('ignore')
from matminer.data_retrieval.retrieve_Citrine import CitrineDataRetrieval
api_key = 'Pj6qmlJCUkKIledB2mgC3wtt' # Set your Citrine API key here. If set as an environment variable 'CITRINE_KEY', set it to 'None'

c = CitrineDataRetrieval(api_key) # Create an adapter to the Citrine Database.

df = c.get_dataframe(criteria={'data_type': 'EXPERIMENTAL', 'max_results': 100},
                     properties=['Band gap', 'Temperature'],
                     common_fields=['chemicalFormula'])
df.rename(columns={'Band gap': 'Experimental band gap'}, inplace=True) # Rename column
df.head()

from pymatgen.core import Composition
from mp_api.client import MPRester
hjs_matminer_api_key = 'I3hV6Q8Uqnnr7dhlOtJNQIq81JEWDU8t'
mpr = MPRester(hjs_matminer_api_key) # provide your API key here or add it to pymatgen

def get_MP_bandgap(formula):
    """Given a composition, get the band gap energy of the ground-state structure
    at that composition

    Args:
        composition (string) - Chemical formula
    Returns:
        (float) Band gap energy of the ground state structure"""
    # The MPRester requires integer formuals as input
    reduced_formula = Composition(formula).get_integer_formula_and_factor()[0]
    struct_lst = mpr.get_structures(reduced_formula)
    #struct_lst = mpr.get_data(reduced_formula)

    # If there is a structure at this composition, return the band gap energy
    if struct_lst:
        return sorted(struct_lst, key=lambda e: e['energy_per_atom'])[0]['band_gap']

df['Computed band gap'] = df['chemicalFormula'].apply(get_MP_bandgap)