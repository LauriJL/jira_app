import json

from django.test import TestCase
from django.urls import reverse

from .services import DEFAULT_PURPOSE, build_nda, validate


def valid_payload(**overrides):
    payload = {
        "party1_company": "Acme Corp",
        "party1_name": "Ada Lovelace",
        "party1_title": "CEO",
        "party1_notice": "ada@acme.example",
        "party2_company": "Globex LLC",
        "party2_name": "Grace Hopper",
        "party2_title": "CTO",
        "party2_notice": "grace@globex.example",
        "purpose": "Evaluating a potential partnership.",
        "effective_date": "2026-10-09",
        "mnda_term_years": 2,
        "mnda_term_continues": False,
        "confidentiality_years": 3,
        "confidentiality_perpetual": False,
        "governing_law": "Delaware",
        "jurisdiction": "New Castle, DE",
        "modifications": "",
    }
    payload.update(overrides)
    return payload


class GenerateNdaViewTests(TestCase):
    url = reverse("generate-nda")

    def post(self, payload):
        return self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

    def test_generates_filled_nda(self):
        response = self.post(valid_payload())

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("markdown", body)
        self.assertEqual(body["filename"], "Mutual-NDA-Acme-Corp-Globex-LLC.md")

        markdown = body["markdown"]
        self.assertIn("Ada Lovelace", markdown)
        self.assertIn("Grace Hopper", markdown)
        self.assertIn("Acme Corp", markdown)
        self.assertIn("Globex LLC", markdown)
        self.assertIn("October 9, 2026", markdown)
        self.assertIn("Governing Law: Delaware", markdown)
        self.assertIn("courts located in New Castle, DE", markdown)
        self.assertIn("Expires 2 years from Effective Date.", markdown)
        self.assertIn("3 years from Effective Date", markdown)
        self.assertIn("term of 2 years", markdown)
        self.assertIn("period of 3 years", markdown)
        self.assertIn("commences on October 9, 2026", markdown)
        # All template placeholders should be resolved.
        self.assertNotIn("coverpage_link", markdown)
        self.assertNotIn("<label>", markdown)
        self.assertNotIn("[Fill in state]", markdown)
        self.assertNotIn("1 year(s)", markdown)

    def test_missing_required_fields(self):
        response = self.post({})

        self.assertEqual(response.status_code, 400)
        errors = response.json()["errors"]
        self.assertIn("party1_company", errors)
        self.assertIn("party2_name", errors)
        self.assertIn("governing_law", errors)

    def test_continues_and_perpetual_options(self):
        response = self.post(
            valid_payload(mnda_term_continues=True, confidentiality_perpetual=True)
        )

        self.assertEqual(response.status_code, 200)
        markdown = response.json()["markdown"]
        self.assertIn("[x]     Continues until terminated", markdown)
        self.assertIn("[x]     In perpetuity.", markdown)
        self.assertIn("term continuing until terminated", markdown)
        self.assertIn("period continuing in perpetuity", markdown)

    def test_invalid_date(self):
        response = self.post(valid_payload(effective_date="09/10/2026"))

        self.assertEqual(response.status_code, 400)
        self.assertIn("effective_date", response.json()["errors"])

    def test_invalid_json(self):
        response = self.client.post(
            self.url, data="not json", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_only_post_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)


class ValidateServiceTests(TestCase):
    def test_default_purpose_is_used(self):
        data = validate(valid_payload(purpose=""))
        self.assertEqual(data["purpose"], DEFAULT_PURPOSE)

    def test_non_positive_years_rejected(self):
        with self.assertRaises(Exception):
            validate(valid_payload(mnda_term_years=0))

    def test_build_nda_includes_both_sections(self):
        document = build_nda(validate(valid_payload()))
        self.assertIn("# Mutual Non-Disclosure Agreement", document)
        self.assertIn("# Standard Terms", document)
        self.assertIn("---", document)
