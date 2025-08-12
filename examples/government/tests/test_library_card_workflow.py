"""End-to-end tests for the library card application workflow.

Tests based on scenarios defined in library-card.spec.feature
"""

import pytest
from playwright.sync_api import Page, expect


class TestLibraryCardWorkflow:
    """Test suite for library card application workflow scenarios."""
    
    def test_complete_successful_application(self, page: Page, workflow_url: str):
        """Test complete successful library card application flow."""
        # Start the workflow
        page.goto(workflow_url)
        
        # Personal Details Step
        expect(page.locator("h1")).to_contain_text("Apply for a library card")
        
        # Fill valid personal details
        page.fill("input[name='full_name']", "John Smith")
        page.fill("input[name='date_of_birth']", "1980-03-27")  
        page.fill("input[name='email']", "john.smith@example.com")
        page.fill("input[name='phone']", "07700 900 982")
        page.fill("input[name='street']", "123 Main Street")
        page.fill("input[name='city']", "London")
        page.fill("input[name='postcode']", "SW1A 1AA")
        page.select_option("select[name='proof_doc_type']", "council_tax")
        
        # Submit personal details
        page.click("button[type='submit']")
        
        # Library Preferences Step
        expect(page.locator("h1")).to_contain_text("Choose your library preferences")
        
        page.select_option("select[name='preferred_branch']", "central_library")
        page.select_option("select[name='comms_pref']", "email")
        page.fill("textarea[name='interests']", "Fiction, local history")
        
        page.click("button[type='submit']")
        
        # Terms and Conditions Step
        expect(page.locator("h1")).to_contain_text("Terms and conditions")
        
        # Check all required checkboxes
        page.check("input[name='data_protection']")
        page.check("input[name='code_of_conduct']") 
        page.check("input[name='info_accuracy']")
        # Marketing opt-in is optional
        page.check("input[name='marketing_opt_in']")
        
        page.click("button[type='submit']")
        
        # Application Confirmation Step
        expect(page.locator("h1")).to_contain_text("Library card application submitted")
        
        # Verify confirmation details are shown
        expect(page.locator("body")).to_contain_text("John Smith")
        expect(page.locator("body")).to_contain_text("john.smith@example.com")
        expect(page.locator("body")).to_contain_text("Central Library")
        
        # Verify generated details
        expect(page.locator("body")).to_contain_text("Application reference")
        expect(page.locator("body")).to_contain_text("Library card number")

    def test_personal_details_invalid_postcode(self, page: Page, workflow_url: str):
        """Test personal details form validation with invalid postcode."""
        page.goto(workflow_url)
        
        # Fill form with invalid postcode
        page.fill("input[name='full_name']", "John Smith")
        page.fill("input[name='date_of_birth']", "1980-03-27")
        page.fill("input[name='email']", "john.smith@example.com")  
        page.fill("input[name='phone']", "07700 900 982")
        page.fill("input[name='street']", "123 Main Street")
        page.fill("input[name='city']", "London")
        page.fill("input[name='postcode']", "INVALID")  # Invalid postcode
        page.select_option("select[name='proof_doc_type']", "council_tax")
        
        page.click("button[type='submit']")
        
        # Should remain on personal details page with error
        expect(page.locator("h1")).to_contain_text("Apply for a library card")
        expect(page.locator(".govuk-error-message")).to_contain_text("postcode")

    def test_personal_details_missing_required_field(self, page: Page, workflow_url: str):
        """Test personal details form validation with missing required field."""
        page.goto(workflow_url)
        
        # Fill form but leave email empty (required field)
        page.fill("input[name='full_name']", "John Smith")
        page.fill("input[name='date_of_birth']", "1980-03-27")
        # Skip email - required field
        page.fill("input[name='phone']", "07700 900 982")
        page.fill("input[name='street']", "123 Main Street") 
        page.fill("input[name='city']", "London")
        page.fill("input[name='postcode']", "SW1A 1AA")
        page.select_option("select[name='proof_doc_type']", "council_tax")
        
        page.click("button[type='submit']")
        
        # Should remain on personal details page
        expect(page.locator("h1")).to_contain_text("Apply for a library card")

    def test_personal_details_missing_proof_document(self, page: Page, workflow_url: str):
        """Test personal details form validation with missing proof document selection."""
        page.goto(workflow_url)
        
        # Fill form but don't select proof document type
        page.fill("input[name='full_name']", "John Smith")
        page.fill("input[name='date_of_birth']", "1980-03-27")
        page.fill("input[name='email']", "john.smith@example.com")
        page.fill("input[name='phone']", "07700 900 982")
        page.fill("input[name='street']", "123 Main Street")
        page.fill("input[name='city']", "London")
        page.fill("input[name='postcode']", "SW1A 1AA")
        # Don't select proof_doc_type - required field
        
        page.click("button[type='submit']")
        
        # Should remain on personal details page
        expect(page.locator("h1")).to_contain_text("Apply for a library card")

    def test_library_preferences_missing_required_branch(self, page: Page, workflow_url: str):
        """Test library preferences form validation with missing branch selection."""
        page.goto(workflow_url)
        
        # Complete personal details first
        self._fill_valid_personal_details(page)
        page.click("button[type='submit']")
        
        # On library preferences page, don't select branch
        expect(page.locator("h1")).to_contain_text("Choose your library preferences")
        
        # Don't select preferred_branch - required field
        page.select_option("select[name='comms_pref']", "email")
        
        page.click("button[type='submit']")
        
        # Should remain on library preferences page
        expect(page.locator("h1")).to_contain_text("Choose your library preferences")

    def test_terms_conditions_not_accepted(self, page: Page, workflow_url: str):
        """Test terms and conditions form validation when required terms not accepted."""
        page.goto(workflow_url)
        
        # Complete personal details and preferences
        self._fill_valid_personal_details(page)
        page.click("button[type='submit']")
        
        self._fill_valid_preferences(page)
        page.click("button[type='submit']")
        
        # On terms page, don't check required boxes
        expect(page.locator("h1")).to_contain_text("Terms and conditions")
        
        # Check only one required box, leave others unchecked
        page.check("input[name='data_protection']")
        # Leave code_of_conduct and info_accuracy unchecked
        
        page.click("button[type='submit']")
        
        # Should remain on terms page with error
        expect(page.locator("h1")).to_contain_text("Terms and conditions")

    def test_field_visibility_and_labels(self, page: Page, workflow_url: str):
        """Test that all expected form fields are visible with correct labels."""
        page.goto(workflow_url)
        
        # Personal Details page
        expect(page.locator("label[for='full_name']")).to_contain_text("Full name")
        expect(page.locator("label[for='date_of_birth']")).to_contain_text("Date of birth")
        expect(page.locator("label[for='email']")).to_contain_text("Email address")
        expect(page.locator("label[for='phone']")).to_contain_text("telephone number")
        expect(page.locator("label[for='street']")).to_contain_text("Street")
        expect(page.locator("label[for='city']")).to_contain_text("city")
        expect(page.locator("label[for='postcode']")).to_contain_text("Postcode") 
        expect(page.locator("label[for='proof_doc_type']")).to_contain_text("Proof of address")
        
        # All fields should be visible
        expect(page.locator("input[name='full_name']")).to_be_visible()
        expect(page.locator("input[name='date_of_birth']")).to_be_visible()
        expect(page.locator("input[name='email']")).to_be_visible()
        expect(page.locator("input[name='phone']")).to_be_visible()
        expect(page.locator("input[name='street']")).to_be_visible()
        expect(page.locator("input[name='city']")).to_be_visible()
        expect(page.locator("input[name='postcode']")).to_be_visible()
        expect(page.locator("select[name='proof_doc_type']")).to_be_visible()

    def test_workflow_data_persistence(self, page: Page, workflow_url: str):
        """Test that data persists correctly between workflow steps."""
        page.goto(workflow_url)
        
        # Complete personal details
        page.fill("input[name='full_name']", "Jane Doe")
        page.fill("input[name='email']", "jane.doe@example.com")
        self._fill_valid_personal_details(page, name="Jane Doe", email="jane.doe@example.com")
        page.click("button[type='submit']")
        
        # Complete preferences
        self._fill_valid_preferences(page) 
        page.click("button[type='submit']")
        
        # Complete terms
        self._accept_all_terms(page)
        page.click("button[type='submit']")
        
        # Verify data appears on confirmation page
        expect(page.locator("body")).to_contain_text("Jane Doe")
        expect(page.locator("body")).to_contain_text("jane.doe@example.com")

    # Helper methods for common form filling operations
    def _fill_valid_personal_details(self, page: Page, name="John Smith", email="john.smith@example.com"):
        """Fill personal details form with valid data."""
        page.fill("input[name='full_name']", name)
        page.fill("input[name='date_of_birth']", "1980-03-27")
        page.fill("input[name='email']", email)
        page.fill("input[name='phone']", "07700 900 982")
        page.fill("input[name='street']", "123 Main Street")
        page.fill("input[name='city']", "London")
        page.fill("input[name='postcode']", "SW1A 1AA")
        page.select_option("select[name='proof_doc_type']", "council_tax")

    def _fill_valid_preferences(self, page: Page):
        """Fill library preferences form with valid data."""
        page.select_option("select[name='preferred_branch']", "central_library")
        page.select_option("select[name='comms_pref']", "email")

    def _accept_all_terms(self, page: Page):
        """Accept all required terms and conditions."""
        page.check("input[name='data_protection']")
        page.check("input[name='code_of_conduct']")
        page.check("input[name='info_accuracy']")