"""
Seed the database with a small number of SAMPLE/DEMO schemes.

IMPORTANT: These are fictional demo schemes with invented eligibility
rules, created for learning/testing purposes only. They are NOT real
government schemes and must never be presented as official.
"""
from app import create_app
from app.extensions import db
from app.models import EligibilityRule, RequiredDocument, Scheme

app = create_app()


def seed():
    with app.app_context():
        if Scheme.query.first():
            print("Schemes already exist. Skipping seed to avoid duplicates.")
            return

        student_scheme = Scheme(
            name="[DEMO] Student Scholarship Scheme",
            description="A sample scholarship scheme for demo/testing purposes only.",
            benefits="Fictional benefit: annual scholarship amount (demo data).",
            category="Education",
            status="active",
        )
        farmer_scheme = Scheme(
            name="[DEMO] Farmer Support Scheme",
            description="A sample income-support scheme for demo/testing purposes only.",
            benefits="Fictional benefit: seasonal support payment (demo data).",
            category="Agriculture",
            status="active",
        )
        women_scheme = Scheme(
            name="[DEMO] Women Entrepreneur Scheme",
            description="A sample scheme supporting women-owned businesses, for demo/testing only.",
            benefits="Fictional benefit: low-interest business loan (demo data).",
            category="Business",
            status="active",
        )

        db.session.add_all([student_scheme, farmer_scheme, women_scheme])
        db.session.commit()

        db.session.add_all(
            [
                EligibilityRule(scheme_id=student_scheme.scheme_id, field_name="age", operator=">=", expected_value="18"),
                EligibilityRule(scheme_id=student_scheme.scheme_id, field_name="income", operator="<=", expected_value="500000"),
                EligibilityRule(scheme_id=student_scheme.scheme_id, field_name="occupation", operator="==", expected_value="Student"),

                EligibilityRule(scheme_id=farmer_scheme.scheme_id, field_name="age", operator=">=", expected_value="21"),
                EligibilityRule(scheme_id=farmer_scheme.scheme_id, field_name="occupation", operator="==", expected_value="Farmer"),

                EligibilityRule(scheme_id=women_scheme.scheme_id, field_name="age", operator=">=", expected_value="18"),
                EligibilityRule(scheme_id=women_scheme.scheme_id, field_name="gender", operator="==", expected_value="Female"),
                EligibilityRule(scheme_id=women_scheme.scheme_id, field_name="income", operator="<=", expected_value="800000"),
            ]
        )

        db.session.add_all(
            [
                RequiredDocument(scheme_id=student_scheme.scheme_id, document_name="Aadhaar Card (demo)", mandatory=True),
                RequiredDocument(scheme_id=student_scheme.scheme_id, document_name="Income Certificate (demo)", mandatory=True),
                RequiredDocument(scheme_id=student_scheme.scheme_id, document_name="Student ID (demo)", mandatory=True),

                RequiredDocument(scheme_id=farmer_scheme.scheme_id, document_name="Land Ownership Document (demo)", mandatory=True),
                RequiredDocument(scheme_id=farmer_scheme.scheme_id, document_name="Aadhaar Card (demo)", mandatory=True),

                RequiredDocument(scheme_id=women_scheme.scheme_id, document_name="Business Registration (demo)", mandatory=True),
                RequiredDocument(scheme_id=women_scheme.scheme_id, document_name="Aadhaar Card (demo)", mandatory=True),
                RequiredDocument(scheme_id=women_scheme.scheme_id, document_name="Bank Statement (demo)", mandatory=False),
            ]
        )

        db.session.commit()
        print(f"Seeded {Scheme.query.count()} demo schemes.")


if __name__ == "__main__":
    seed()