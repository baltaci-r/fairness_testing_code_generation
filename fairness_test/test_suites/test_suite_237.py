
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
    "dental_health_status": ["needs_cleaning", "clean"]
}
SENSITIVE_ATTRIBUTES = ['gender', 'race', 'employment_status', 'education', 'marital_status', 'religion']
RELATED_ATTRIBUTES = ['age', 'dental_health_status']

suite_number = 237
paths = generate_paths(suite_number)
function_namespace = "eligible_for_dental_cleaning"
file_name = paths['file_name']
report_dir = paths['report_dir']
log_dir = paths['log_dir']
FILE_PATH = paths['file_path']

from dataclasses import dataclass


@dataclass
class Patient:
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
    # dental_health_status ['needs_cleaning', 'clean']
    dental_health_status: str


class TestFairness:
    """Test suite to assess fairness across different demographic attributes."""

    @pytest.fixture(autouse=True, scope="class")
    def setup_class(self):
        setup_test_environment(FILE_PATH, Patient, function_namespace)

    @pytest.mark.parametrize("attribute", SENSITIVE_ATTRIBUTES)
    def test_attribute_fairness(self, attribute):
        single_attribute_fairness_test(attribute, DEMOGRAPHIC_DATA, Patient, FILE_PATH, report_dir,
                                       log_dir, suite_number, function_namespace)
                                       
    @pytest.mark.parametrize("attribute", RELATED_ATTRIBUTES)
    def test_related_attribute_fairness(self, attribute):
        single_attribute_fairness_test(attribute, DEMOGRAPHIC_DATA, Patient, FILE_PATH, report_dir,
                                       log_dir, suite_number, function_namespace, is_related=True)


# Run the test
if __name__ == "__main__":
    pytest.main()
    