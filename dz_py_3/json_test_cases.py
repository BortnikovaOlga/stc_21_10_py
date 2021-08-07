TEST_CASE_POSITIVE_ONE_PRODUCT = {
    "id": 123,
    "name": "Television",
    "package_params": {"width": 5, "height": 10},
    "location_and_quantity": [
        {"location": "Shop on Lenina", "amount": 7},
        {"location": "Shop in centre", "amount": 3},
    ],
}
TEST_CASE_POSITIVE_N_PRODUCTS = [
    {
        "id": 124,
        "name": "Television",
        "package_params": {"width": 5, "height": 10},
        "location_and_quantity": [
            {"location": "Shop on Lenina", "amount": 7},
            {"location": "Shop in centre", "amount": 3},
        ],
    },
    {
        "id": 124,
        "name": "TV update for test",
        "package_params": {"width": 5, "height": 10},
        "location_and_quantity": [
            {"location": "Shop on Lenina", "amount": 7},
            {"location": "Shop in centre", "amount": 3},
        ],
    },
]
TEST_CASE_NEGATIVE = {"id": 123, "package_params": {"width": 5, "height": 10}}
