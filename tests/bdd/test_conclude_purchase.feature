Feature: Conclude a purchase

  Scenario: Successfully conclude a purchase
    Given an existing purchase with products
    And the purchase has a successful payment
    And the purchase total value is greater than zero
    When I conclude the purchase
    Then the purchase should be concluded successfully
