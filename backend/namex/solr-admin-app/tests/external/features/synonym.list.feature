Feature: Synonym list

Scenario: displays existing synonyms
    Given the database is seeded with the synonyms
        | category | synonyms                 |
        | building | home, construction, reno |
        | cooking  | cook, chief              |
    When I access the synonym list
    Then I see that the list contains 2 lines
