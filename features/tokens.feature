Feature: Push Notification Token Management
  As a mobile app developer
  I want to manage push notification tokens
  So that I can send notifications to users' devices

  Background:
    Given the push notification service is running

  Scenario: Register a new FCM token
    When I register a new FCM token with the following details:
      | user_id    | token           | platform |
      | user123    | fcm_token_123   | fcm     |
    Then the response status code should be 200
    And the response should contain the token details
    And the token should be stored in the database

  Scenario: Register a new APNS token
    When I register a new APNS token with the following details:
      | user_id    | token           | platform |
      | user123    | apns_token_123  | apns    |
    Then the response status code should be 200
    And the response should contain the token details
    And the token should be stored in the database

  Scenario: Retrieve user tokens
    Given the following tokens exist for user "user123":
      | token           | platform |
      | fcm_token_123   | fcm     |
      | apns_token_123  | apns    |
    When I request all tokens for user "user123"
    Then the response status code should be 200
    And the response should contain 2 tokens
    And the tokens should match the stored tokens

  Scenario: Delete a token
    Given a token exists with the following details:
      | user_id    | token           | platform |
      | user123    | fcm_token_123   | fcm     |
    When I delete the token
    Then the response status code should be 200
    And the token should be removed from the database

  Scenario: Register duplicate token
    Given a token exists with the following details:
      | user_id    | token           | platform |
      | user123    | fcm_token_123   | fcm     |
    When I register the same token again
    Then the response status code should be 200
    And the response should contain the same token ID

  Scenario: Delete non-existent token
    When I try to delete a non-existent token
    Then the response status code should be 404

  Scenario: Register token with invalid platform
    When I register a token with an invalid platform:
      | user_id    | token           | platform |
      | user123    | fcm_token_123   | invalid |
    Then the response status code should be 422