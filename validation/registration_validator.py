from validation.exceptions import ValidationException
import re

class RegistrationValidator:   
    def validate(self, registration):
        """
        Validates a given Registration object.

        :param registration: The Registration object to validate.
        :return: None.
        """
        errors = []
        
        if not registration.person_id:
            errors.append("Person ID cannot be empty.")
        if not registration.event_id:
            errors.append("Event ID cannot be empty.")

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", registration.date):
            errors.append("Registration date must be in YYYY-MM-DD format.")

        if errors:
            raise ValidationException("\n".join(errors))