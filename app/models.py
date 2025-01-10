from app import db

# Base class for all generic objects
class GenericObject(db.Model):
    __tablename__ = "generic_object"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # Discriminator column to distinguish object types

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "generic_object",
    }


# SalaryHistory model (doesn't need polymorphism)
class SalaryHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.String(50), nullable=False)


# Address inherits from GenericObject
class Address(GenericObject):
    employee_id = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10))
    city = db.Column(db.String(50))
    street = db.Column(db.String(100))
    house_number = db.Column(db.String(10))
    concern_of = db.Column(db.String(50))
    is_emergency_contact = db.Column(db.Boolean, default=False)

    contact_information = db.relationship(
        "ContactInformation", back_populates="address", uselist=False
    )

    __mapper_args__ = {
        "polymorphic_identity": "address",
    }


# ContactInformation linked to Address
class ContactInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('generic_object.id'))  # Foreign key to GenericObject (Address)
    mobile_number = db.Column(db.String(15))
    landline_number = db.Column(db.String(15))
    email_address = db.Column(db.String(100))

    address = db.relationship("Address", back_populates="contact_information")


# EmergencyContact inherits from Address
class EmergencyContact(Address):
    __mapper_args__ = {
        "polymorphic_identity": "emergency_contact",
    }


# ObjectModel inherits from GenericObject
class ObjectModel(GenericObject):
    related_entries = db.relationship(
        "Entry", backref="object", lazy="dynamic"
    )

    __mapper_args__ = {
        "polymorphic_identity": "object_model",
    }


# Entry model (can serve as a base for extended entries)
class Entry(db.Model):
    __tablename__ = "entry"
    id = db.Column(db.Integer, primary_key=True)
    related_object_id = db.Column(
        db.Integer, db.ForeignKey("generic_object.id", ondelete="CASCADE"), nullable=False
    )
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Polymorphic configuration for Entry extensions
    type = db.Column(db.String(50))
    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "entry",
    }


# Extended Entry Example (if needed later)
class QualityCheckEntry(Entry):
    __mapper_args__ = {
        "polymorphic_identity": "quality_check_entry",
    }
