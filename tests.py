import sys
import os
from domain.person import Person
from domain.event import Event
from domain.registration import Registration
from validation.person_validator import PersonValidator
from validation.event_validator import EventValidator
from validation.registration_validator import RegistrationValidator
from validation.exceptions import ValidationException
from repository.person_repository import PersonRepository
from repository.person_file_repository import PersonFileRepository
from repository.event_repository import EventRepository
from repository.registration_repository import RegistrationRepository
from repository.exceptions import RepositoryException
from services import MainController

def test_domain():
    # Test Person
    person = Person("123", "John")
    assert person.person_id == "123"
    assert person.name == "John"

    person.name = "Jane"
    assert person.name == "Jane"

    try:
        print(person.__name) 
        assert False, "Should not be able to access private attributes directly!"
    except AttributeError:
        pass

    # Test Event
    event = Event("1", "2025-10-10", "12:00", "Party")
    assert event.event_id == "1"
    assert event.description == "Party"

    event.description = "Big Party"
    assert event.description == "Big Party"

def test_validators():
    """Tests the validators."""
    p_validator = PersonValidator()
    e_validator = EventValidator()

    p_validator.validate(Person("1990101123456", "Valid Name"))

    try:
        p_validator.validate(Person("123", "Invalid"))
        assert False, "ValidationException not raised for short ID"
    except ValidationException as e:
        assert "must be 13 digits" in str(e)

    # Invalid Event
    try:
        e_validator.validate(Event("1", "10-10-2025", "12:00", "Inv"))
        assert False, "ValidationException not raised for wrong date format"
    except ValidationException as e:
        assert "YYYY-MM-DD" in str(e)

def test_repositories():
    """Tests the repositories."""
    p_repo = PersonRepository()
    person = Person("1990101123456", "John")
    
    # Add
    p_repo.add(person)
    assert len(p_repo.get_all()) == 1
    assert p_repo.find_by_id("1990101123456").name == "John"
    
    # Duplicate
    try:
        p_repo.add(Person("1990101123456", "Double"))
        assert False, "RepositoryException not raised for duplicate"
    except RepositoryException as e:
        assert "already exists" in str(e)

    # Delete
    p_repo.delete("1990101123456")
    assert len(p_repo.get_all()) == 0

def test_services():
    """Tests the controller for basic Person/Event operations."""
    p_repo = PersonRepository()
    e_repo = EventRepository()
    r_repo = RegistrationRepository() 
    p_val = PersonValidator()
    e_val = EventValidator()
    r_val = RegistrationValidator() 
    
    controller = MainController(p_repo, e_repo, r_repo, p_val, e_val, r_val)

    controller.add_person("1990101123456", "John Service")
    assert len(p_repo.get_all()) == 1
    assert p_repo.get_all()[0].name == "John Service"

    try:
        controller.add_person("123", "Bad")
        assert False, "Service allowed an invalid ID through"
    except ValidationException:
        pass

def test_person_file_repository():
    """
    Tests the PersonFileRepository specific features:
    """
    
    filename = "person_test_temp.txt"
    if os.path.exists(filename):
        os.remove(filename)
        
    repo1 = PersonFileRepository(filename)
    assert len(repo1.get_all()) == 0
    
    p1 = Person("1111111111111", "Ana")
    repo1.add(p1)
    assert len(repo1.get_all()) == 1

    repo2 = PersonFileRepository(filename)
    assert len(repo2.get_all()) == 1
    assert repo2.find_by_id("1111111111111").name == "Ana"
    
    repo2.update("1111111111111", "Ana Maria")
    repo3 = PersonFileRepository(filename)
    assert repo3.find_by_id("1111111111111").name == "Ana Maria"
    
    repo3.delete("1111111111111")
    repo4 = PersonFileRepository(filename)
    assert len(repo4.get_all()) == 0

    if os.path.exists(filename):
        os.remove(filename)

# ---(Registration) ---

def test_registration_feature():
    """
    Tests the complete Registration feature flow (Iteration 2).
    """
    
    # 1. Test Domain
    reg = Registration("100", "500", "2025-01-01")
    assert reg.person_id == "100"
    assert reg.event_id == "500"
    
    # 2. Test Validator
    val = RegistrationValidator()
    val.validate(reg)
    try:
        val.validate(Registration("100", "500", "invalid-date"))
        assert False, "Validator failed to catch bad date"
    except ValidationException:
        pass

    # 3. Test Repository
    repo = RegistrationRepository()
    repo.add(reg)
    assert len(repo.get_all()) == 1
    
    # Test duplicate registration
    try:
        repo.add(Registration("100", "500", "2025-02-02"))
        assert False, "Repo failed to catch duplicate registration"
    except RepositoryException:
        pass

    # 4. Test Service (Referential Integrity)
    p_repo = PersonRepository() 
    e_repo = EventRepository()
    r_repo = RegistrationRepository()
    
    p_val = PersonValidator()
    e_val = EventValidator()
    r_val = RegistrationValidator()

    ctrl = MainController(p_repo, e_repo, r_repo, p_val, e_val, r_val)
    
    # Add a person and event so we can register them
    ctrl.add_person("1111111111111", "Test Person")
    ctrl.add_event("999", "2025-01-01", "10:00", "Test Event")
    
    # Test success
    ctrl.register_person_for_event("1111111111111", "999", "2025-01-02")
    assert len(r_repo.get_all()) == 1
    
    # Test fail: Person does not exist
    try:
        ctrl.register_person_for_event("9999999999999", "999", "2025-01-02")
        assert False, "Service allowed registration for non-existent person"
    except RepositoryException as e:
        assert "does not exist" in str(e)

# ---(Reports) ---

def test_reports_feature():
    """
    Tests the reporting features (F4a, F4b, F4c).
    """
    # Setup
    p_repo = PersonRepository()
    e_repo = EventRepository()
    
    r_repo = RegistrationRepository() 
    
    p_val = PersonValidator()
    e_val = EventValidator()
    r_val = RegistrationValidator()
    
    ctrl = MainController(p_repo, e_repo, r_repo, p_val, e_val, r_val)
    
    # -- DATA SETUP --
    # Persons
    p1 = Person("1", "Alice")
    p2 = Person("2", "Bob")
    p3 = Person("3", "Charlie")
    p4 = Person("4", "Dave")
    for p in [p1, p2, p3, p4]: p_repo.add(p)
    
    # Events
    e1 = Event("10", "2025-01-01", "10:00", "Alpha Event")
    e2 = Event("20", "2025-02-02", "12:00", "Beta Event")
    e3 = Event("30", "2025-03-03", "14:00", "Gamma Event")
    for e in [e1, e2, e3]: e_repo.add(e)
    
    # Registrations
    ctrl.register_person_for_event("1", "10", "2025-01-01")
    ctrl.register_person_for_event("1", "20", "2025-01-01")
    
    ctrl.register_person_for_event("2", "10", "2025-01-01")
    ctrl.register_person_for_event("2", "30", "2025-02-01") # Late registration
    
    ctrl.register_person_for_event("3", "10", "2025-01-01")
    ctrl.register_person_for_event("3", "20", "2025-01-01")
    ctrl.register_person_for_event("3", "30", "2025-01-01") # Early registration
    
    # --- TEST F4a: Events for Person (Alice) ---
    events = ctrl.get_events_for_person_ordered("1", sort_by_date=False)
    assert len(events) == 2
    assert events[0].description == "Alpha Event"
    
    # --- TEST F4b: Top 3 Active Persons ---
    top_persons = ctrl.get_most_active_persons()
    assert len(top_persons) == 3
    assert top_persons[0][0].name == "Charlie"
    assert top_persons[0][1] == 3
    assert top_persons[1][0].name == "Alice"
    
    # --- TEST F4c: Top 20% Events ---
    top_events = ctrl.get_top_20_percent_events()
    assert len(top_events) >= 1
    assert top_events[0][0] == "Alpha Event"
    assert top_events[0][1] == 3 # 3 participants
    
    ordered_participants = ctrl.get_persons_for_event_by_reg_date("30")
    assert len(ordered_participants) == 2
    assert ordered_participants[0][0].name == "Charlie" # 2025-01-01
    assert ordered_participants[1][0].name == "Bob"     # 2025-02-01

def run_all_tests():
    """
    Runs all tests.
    """
    test_domain()
    test_validators()
    test_repositories()
    test_services()
    
    test_registration_feature()
    test_person_file_repository()
    
    test_reports_feature()
    
    print("\n--- ALL TESTS PASSED SUCCESSFULLY! ---\n")
    print("-" * 40)