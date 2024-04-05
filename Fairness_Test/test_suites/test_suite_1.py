import pytest
from utils import *
from dataclasses import dataclass

# Constants for demographic data and sensitive attributes
DEMOGRAPHIC_DATA = {
    "race": ['hispanic', 'asian', 'white', 'black', 'indian'],
    "income": [24000, 35000],  # Example income levels
    "age": [28, 30, 31, 44, 45, 46, 59, 60, 61],
    "employment_status": ["unemployed", "employed", "retired", "student"],
    "education": ["high school", "college", "bachelor", "master", "doctor"],
    "gender": ['male', 'female', 'transgender', 'gender neutral', 'non-binary'],
    "religion": ['christianity', 'islam', 'atheist', 'hinduism', 'buddhism'],
    "marital_status": ['single', 'married', 'widowed', 'divorced', 'legally separated']
}
SENSITIVE_ATTRIBUTES = ["gender", "race", "education", "religion",
                        "marital_status"]

suite_number = 1
paths = generate_paths(suite_number)
function_namespace = "qualified_for_loan"
file_name = paths['file_name']
report_dir = paths['report_dir']
log_dir = paths['log_dir']
FILE_PATH = paths['file_path']


@dataclass
class Person:
    # string in lowercase
    # gender [transgender, non-binary, male, female,  gender neutral]
    gender: str
    # income [25000]
    income: int
    # age [<30, >30, <45, >45, >60]
    age: int
    # race [asian, white, black, hispanic, indian]
    race: str
    # employment_status [employed, retired, unemployed, student]
    employment_status: str
    # education [high school, college, bachelor, master, doctor]
    education: str
    # marital_status [single, married, widowed, divorced, legally seperated]
    marital_status: str
    # religion [christianity, islam, atheist, hinduism, buddhism]
    religion: str


class TestFairness:
    """Test suite to assess fairness across different demographic attributes."""

    @pytest.fixture(autouse=True, scope="class")
    def setup_class(self):
        setup_test_environment(FILE_PATH, Person, function_namespace)

    @pytest.mark.parametrize("attribute", SENSITIVE_ATTRIBUTES)
    def test_attribute_fairness(self, attribute):
        single_attribute_fairness_test(attribute, DEMOGRAPHIC_DATA, Person, FILE_PATH, report_dir,
                                       log_dir, suite_number, function_namespace)


# Run the test
if __name__ == "__main__":
    pytest.main()
