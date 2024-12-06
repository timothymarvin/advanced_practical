import unittest
from .product_discount import Product, DiscountedPrice

class TestProduct(unittest.TestCase):
    def test_total_calculation(self):
        product = Product("Phone", 200, 3)
        self.assertEqual(product.calculate_total_price(), 600)

    def test_name_validation(self):
        with self.assertRaises(ValueError):
            Product("TV", 500, 2)  # Invalid name: Too short

        with self.assertRaises(ValueError):
            Product("A" * 26, 500, 2)  # Invalid name: Too long

    def test_price_validation(self):
        with self.assertRaises(ValueError):
            Product("Phone", -100, 3)  # Negative price


class TestDiscountedPrice(unittest.TestCase):
    def test_discounted_total(self):
        discounted_product = DiscountedPrice("Television", 1000, 1, 20)  # Changed "TV" to "Television"
        self.assertEqual(discounted_product.calculate_total_price(), 800)

    def test_discount_validation(self):
        with self.assertRaises(ValueError):
            DiscountedPrice("Television", 1000, 1, -10)  # Invalid discount

        with self.assertRaises(ValueError):
            DiscountedPrice("Television", 1000, 1, 110)  # Invalid discount


if __name__ == "__main__":
    unittest.main()
