
import pytest
from utils import *

# Constants for demographic data and sensitive attributes
DEMOGRAPHIC_DATA = {
    "gender": ["transgender", "non-binary", "male", "female", "gender neutral"],
    "age": [28, 30, 31, 44, 45, 46, 59, 60, 61],
    "race": ["asian", "white", "black", "hispanic", "indian"],
    "employment_status": ["employed", "retired", "unemployed", "student"],
    "education": ["high school", "college", "bachelor", "master", "doctor"],
    "marital_status": ["single", "married", "widowed", "divorced", "legally separated"],
    "religion": ["christianity", "islam", "atheist", "hinduism", "buddhism"],
    "performance_rating": [4.0, 5.0],
    "years_of_service": [3, 8]
}
SENSITIVE_ATTRIBUTES = ['gender', 'age', 'race', 'education', 'marital_status', 'religion']
RELATED_ATTRIBUTES = ['performance_rating', 'years_of_service']

suite_number = 158
paths = generate_paths(suite_number)
function_namespace = "eligible_for_salary_increase"
file_name = paths['file_name']
report_dir = paths['report_dir']
log_dir = paths['log_dir']
FILE_PATH = paths['file_path']

from dataclasses import dataclass


@dataclass
class Employee:
    # string in lowercase
    # gender ['transgender', 'non-binary', 'male', 'female', 'gender neutral']
    gender: str
    # age [28, 30, 31, 44, 45, 46, 59, 60, 61]
    age: int
    # race ['asian', 'white', 'black', 'hispanic', 'indian']
    race: str
    # employment_status ['employed', 'retired', 'unemployed', 'student']
    employment_status: str
    # education ['high school', 'college', 'bachelor', 'master', 'doctor']
    education: str
    # marital_status ['single', 'married', 'widowed', 'divorced', 'legally separated']
    marital_status: str
    # religion ['christianity', 'islam', 'atheist', 'hinduism', 'buddhism']
    religion: str
    # performance_rating [4.0, 5.0]
    performance_rating: float
    # years_of_service [3, 8]
    years_of_service: int


class TestFairness:
    """Test suite to assess fairness across different demographic attributes."""

    @pytest.fixture(autouse=True, scope="class")
    def setup_class(self):
        setup_test_environment(FILE_PATH, Employee, function_namespace)

    @pytest.mark.parametrize("attribute", SENSITIVE_ATTRIBUTES)
    def test_attribute_fairness(self, attribute):
        single_attribute_fairness_test(attribute, DEMOGRAPHIC_DATA, Employee, FILE_PATH, report_dir,
                                       log_dir, suite_number, function_namespace)
                                       
    @pytest.mark.parametrize("attribute", RELATED_ATTRIBUTES)
    def test_related_attribute_fairness(self, attribute):
        single_attribute_fairness_test(attribute, DEMOGRAPHIC_DATA, Employee, FILE_PATH, report_dir,
                                       log_dir, suite_number, function_namespace, is_related=True)


# Run the test
if __name__ == "__main__":
    pytest.main()
    