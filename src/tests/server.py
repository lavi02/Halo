from httpx import AsyncClient
import pytest
import main
import unittest

class TestOptimizeWaypointsTest(unittest.TestCase):

    def setUp(self):
        self.client = AsyncClient(app=main.app, base_url="http://test")

    @pytest.mark.anyio
    async def test_optimize_waypoints_test_success(self):
        test_waypoints = {
            "waypoints": {"A": (0, 0), "B": (1, 1), "C": (2, 2)}
        }

        async with self.client as ac:
            response = await ac.post("/api/v1/optimize_test", json=test_waypoints)

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.json())
            self.assertIn("A", response.json())
            self.assertIn("B", response.json())
            self.assertIn("C", response.json()) 

if __name__ == '__main__':
    unittest.main()
