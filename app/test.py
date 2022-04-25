
try:
    from app import app
    import unittest

except Exception as e:
    print("Some Modules are Missing {} ".format(e))

data1 =  {"firstName":"Josh",
        "secondName":"Woodward",
        "email":"14066910@brookes.ac.uk",
        "occupation":"Data Analyst",
        "district":"OX"}

data2 =  {"firstName":"Josh",
        "secondName":"Woodward",
        "email":"14066910@brookes.ac.uk",
        "occupation":"Data Analyst",
        "district":"PO"}

class unitTesting(unittest.TestCase):
    # Check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Post employee details and check response.
    # If reponse returns id then employee has been added.
    def test_employee_post(self):
        tester = app.test_client(self)
        response = tester.post("/addEmployee", json=data1)
        self.assertTrue(b'id' in response.data)

        # Edit employee and check the returning json is correct
    def test_employees_put(self):
        tester = app.test_client(self)
        response = tester.put("/editEmployee/1", json=data2)
        self.assertTrue(b'PO' in response.data)

        # Check if employees return is json
    def test_employees_content(self):
        tester = app.test_client(self)
        response = tester.get("/employees")
        self.assertEqual(response.content_type, "application/json")


class delete(unittest.TestCase):   
    # Delete employee
    def test_employees_delete(self):
        tester = app.test_client(self)
        response = tester.delete("/deleteEmployee/1")
        self.assertEqual(response.content_type, "application/json")


if __name__ == "__main__":
    unittest.main()