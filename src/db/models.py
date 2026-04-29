"""

Import All models in here so that alembic can find them
"""

from src.features.crm.models.companies import CompanyModel
from src.features.crm.models.opportunity import Opportunity
from src.features.auth.models.users import UserModel


from src.features.training.models.formateur import Formateur
from src.features.training.models.formation import Formation
from src.features.training.models.formation_formateur import FormateurFormation
