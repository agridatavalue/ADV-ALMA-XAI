import unittest

from src.adv_xai_fulfilment.domain.model.partner import Partner

class TestPartner(unittest.TestCase):
    def test_partner_equality(self):
        partner1 = Partner("partner_123")
        partner2 = Partner("partner_123")
        partner3 = Partner("partner_456")

        self.assertTrue(partner1.is_equal(partner2))
        self.assertFalse(partner1.is_equal(partner3))
        self.assertFalse(partner1.is_equal("not_a_partner")) # type: ignore
        