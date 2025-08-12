@workflow(name="library-card-application", timeout=300, retry_attempts=3, parallel_execution=false)
Feature: Library card application service
  As a UK resident
  I want to apply for a public library card online
  So that I can access library resources

  Background:
    Given the workflow entry app is "personal-details"

  @app(id="personal-details", skeleton="casa", port=8001, entry_point=true)
  Scenario: Submit personal details successfully
    Given the form "personal-details" has fields:
      | name           | label                | type   | required | notes                                   |
      | full_name      | Full name            | text   | true     |                                          |
      | date_of_birth  | Date of birth        | date   | true     |                                          |
      | email          | Email address        | email  | true     |                                          |
      | phone          | Phone number         | tel    | true     |                                          |
      | street         | Street               | text   | true     |                                          |
      | city           | Town or city         | text   | true     |                                          |
      | postcode       | Postcode             | text   | true     | UK format validation required            |
      | proof_doc_type | Proof of address     | select | true     | values: council_tax, utility_bill, bank_statement |
    And the postcode matches pattern "^[A-Z]{1,2}[0-9][A-Z0-9]?\\s?[0-9][A-Z]{2}$"
    When the user submits valid personal details
    Then route to "library-preferences"
    And emit data "applicant_core" containing:
      | full_name |
      | date_of_birth |
      | email |
      | phone |
      | street |
      | city |
      | postcode |
      | proof_doc_type |

  Scenario: Personal details postcode invalid
    Given the user enters a postcode that does not match the required pattern
    When the user submits the form
    Then remain on "personal-details"
    And show field error "Please enter a valid UK postcode"

  Scenario: Personal details missing proof of address
    Given the user leaves "proof_doc_type" empty
    When the user submits the form
    Then remain on "personal-details"
    And show field error "Select a proof of address document"

  @app(id="library-preferences", skeleton="casa", port=8002)
  Scenario: Submit library preferences successfully
    Given the form "library-preferences" has fields:
      | name                 | label                          | type     | required | notes |
      | preferred_branch     | Preferred branch for collection| select   | true     | values come from router or config |
      | comms_pref           | Communication preference       | select   | true     | values: email, sms, post |
      | interests            | Interest categories            | select   | false    | multi-select allowed |
      | accessibility        | Accessibility requirements     | textarea | false    |                                      |
    When the user submits valid preferences
    Then route to "terms-and-conditions"
    And pass data from "personal-details" to "library-preferences":
      | full_name |
      | email |
      | postcode |

  Scenario: Preferences missing required branch
    Given "preferred_branch" is not selected
    When the user submits the form
    Then remain on "library-preferences"
    And show field error "Select a branch for collection"

  @app(id="terms-and-conditions", skeleton="casa", port=8003)
  Scenario: Accept terms and conditions
    Given the form "terms-and-conditions" has fields:
      | name                 | label                                        | type     | required | value      |
      | data_protection      | I agree to the data protection statement     | checkbox | true     | accepted   |
      | code_of_conduct      | I accept the library code of conduct         | checkbox | true     | accepted   |
      | info_accuracy        | I confirm my information is accurate         | checkbox | true     | accepted   |
      | marketing_opt_in     | I would like to receive marketing updates    | checkbox | false    | subscribed |
    When the user checks all required boxes and submits
    Then route to "application-confirmation"

  Scenario: Terms not accepted
    Given at least one required checkbox is not checked
    When the user submits the form
    Then remain on "terms-and-conditions"
    And show form error "You must accept the required terms to continue"

  @app(id="application-confirmation", skeleton="http_base", port=8004)
  Scenario: Review and confirm application
    Given the confirmation page shows all submitted data using wildcard mapping from prior steps
    And the system can assign a library card number
    When the user confirms the application
    Then complete the workflow with status "success"
    And emit data "registration_result" containing:
      | library_card_number |
      | preferred_branch    |
      | collection_instructions |
      | opening_hours       |

  Scenario: Edit from confirmation returns to previous step
    Given the user is on "application-confirmation"
    When the user chooses to edit "terms-and-conditions"
    Then route to "terms-and-conditions"
    And preserve previously entered data

  # Optional failure branch
  Scenario: Card number assignment fails
    Given the system cannot assign a library card number
    When the user confirms the application
    Then fail the workflow with reason "card_number_generation_failed"