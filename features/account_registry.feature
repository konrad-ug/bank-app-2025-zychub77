Feature: Account registry
Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry
Scenario: User is able to update surname of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "zoe", last name: "kravitz", pesel: "84010112345"
    When I update "name" of account with pesel: "84010112345" to "zoe_new"
    Then Account with pesel "84010112345" has "name" equal to "zoe_new"

Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "john", last name: "snow", pesel: "90010112345"
    Then Account with pesel "90010112345" has "name" equal to "john"
    And Account with pesel "90010112345" has "surname" equal to "snow"
    And Account with pesel "90010112345" exists in registry
Scenario: User is able to delete created account
    Given Account registry is empty
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

Scenario: User is able to post incoming transfers
    Given Account registry is empty
    And I create an account using name: "mila", last name: "jovovich", pesel: "93010112345"
    When I make incoming transfer of "10" to account with pesel: "93010112345"
    And I make incoming transfer of "15" to account with pesel: "93010112345"
    Then Account with pesel "93010112345" has balance equal to "25"

Scenario: User is able to post outgoing transfer
    Given Account registry is empty
    And I create an account using name: "adam", last name: "nowak", pesel: "92010112345"
    And I create an account using name: "ewa", last name: "nowak", pesel: "92010112346"
    When I make incoming transfer of "50" to account with pesel: "92010112345"
    And I make outgoing transfer of "20" from account with pesel: "92010112345" to account with pesel: "92010112346"
    Then Account with pesel "92010112345" has balance equal to "30"
    And Account with pesel "92010112346" has balance equal to "20"
