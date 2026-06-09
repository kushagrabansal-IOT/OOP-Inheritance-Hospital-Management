"""
OOP-Inheritance-Hospital-Management
Concepts: Single, Multilevel, Hierarchical Inheritance
Author  : Kushagra Bansal — Project Lab India
Run     : python main.py
"""
from abc import ABC, abstractmethod
from datetime import datetime, date
from enum import Enum

class BloodGroup(Enum):
    A_POS="A+"; A_NEG="A-"; B_POS="B+"; B_NEG="B-"
    AB_POS="AB+"; AB_NEG="AB-"; O_POS="O+"; O_NEG="O-"

class Severity(Enum):
    CRITICAL="CRITICAL"; HIGH="HIGH"; MEDIUM="MEDIUM"; LOW="LOW"


# ── Level 1: Base Class ──────────────────────────────────────
class Person(ABC):
    """Abstract base — every person in the hospital"""
    _id_counter = 1000

    def __init__(self, name, age, gender, phone, email=""):
        Person._id_counter += 1
        self._id     = f"PLI{Person._id_counter:05d}"
        self._name   = name
        self._age    = age
        self._gender = gender
        self._phone  = phone
        self._email  = email
        self._created= datetime.now()

    @property
    def id(self):    return self._id
    @property
    def name(self):  return self._name
    @property
    def age(self):   return self._age
    @property
    def phone(self): return self._phone

    @abstractmethod
    def get_role(self): pass

    @abstractmethod
    def get_info(self): pass

    def __str__(self):
        return f"[{self.get_role()}] {self._id} | {self._name} | Age:{self._age} | Ph:{self._phone}"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id!r}, name={self._name!r})"


# ── Level 2: Direct Inheritors of Person ────────────────────
class Patient(Person):
    """Single Inheritance: Patient extends Person"""

    def __init__(self, name, age, gender, phone, blood_group, email=""):
        super().__init__(name, age, gender, phone, email)
        self._blood_group    = blood_group
        self._medical_history= []
        self._prescriptions  = []
        self._admission_date = None
        self._ward           = None
        self._severity       = Severity.LOW

    @property
    def blood_group(self):  return self._blood_group
    @property
    def severity(self):     return self._severity
    @property
    def is_admitted(self):  return self._admission_date is not None

    def admit(self, ward, severity=Severity.MEDIUM):
        self._admission_date = datetime.now()
        self._ward           = ward
        self._severity       = severity
        ward.add_patient(self)
        print(f"  🏥 {self._name} admitted to {ward.name} | Severity: {severity.value}")

    def discharge(self):
        if self._ward:
            self._ward.remove_patient(self)
        self._admission_date = None
        self._ward           = None
        print(f"  👋 {self._name} discharged successfully")

    def add_medical_record(self, diagnosis, doctor):
        record = {
            "date":      datetime.now().strftime("%Y-%m-%d"),
            "diagnosis": diagnosis,
            "doctor":    doctor.name,
            "doctor_id": doctor.id
        }
        self._medical_history.append(record)

    def add_prescription(self, medication, dosage, doctor):
        rx = {"medication":medication,"dosage":dosage,
              "prescribed_by":doctor.name,"date":datetime.now().strftime("%Y-%m-%d")}
        self._prescriptions.append(rx)

    def get_role(self): return "PATIENT"

    def get_info(self):
        print(f"\n  {'─'*55}")
        print(f"  PATIENT PROFILE")
        print(f"  {'─'*55}")
        print(f"  ID           : {self._id}")
        print(f"  Name         : {self._name}")
        print(f"  Age/Gender   : {self._age} / {self._gender}")
        print(f"  Blood Group  : {self._blood_group.value}")
        print(f"  Status       : {'Admitted' if self.is_admitted else 'Outpatient'}")
        if self.is_admitted:
            print(f"  Ward         : {self._ward.name}")
            print(f"  Severity     : {self._severity.value}")
        if self._medical_history:
            print(f"  Last Diagnosis: {self._medical_history[-1]['diagnosis']}")
        print(f"  {'─'*55}")


class MedicalStaff(Person):
    """Hierarchical Inheritance: MedicalStaff extends Person"""

    def __init__(self, name, age, gender, phone, department, salary, experience_yrs, email=""):
        super().__init__(name, age, gender, phone, email)
        self._department    = department
        self.__salary       = salary      # Private — encapsulation
        self._experience    = experience_yrs
        self._is_on_duty    = False
        self._join_date     = date.today()

    @property
    def department(self):   return self._department
    @property
    def experience(self):   return self._experience
    @property
    def is_on_duty(self):   return self._is_on_duty

    def start_shift(self):
        self._is_on_duty = True
        print(f"  🟢 {self._name} started shift in {self._department}")

    def end_shift(self):
        self._is_on_duty = False
        print(f"  🔴 {self._name} ended shift")

    def get_salary(self): return self.__salary    # Controlled access
    def get_role(self):   return "STAFF"
    def get_info(self):
        print(f"  {self._id} | {self._name} | {self._department} | {self._experience}yr exp")


# ── Level 3: Multilevel Inheritance ─────────────────────────
class Doctor(MedicalStaff):
    """Multilevel: Doctor → MedicalStaff → Person"""

    def __init__(self, name, age, gender, phone, department,
                 salary, experience_yrs, specialization, license_no):
        super().__init__(name, age, gender, phone, department, salary, experience_yrs)
        self.__specialization = specialization
        self.__license_no     = license_no
        self._patients        = []
        self._appointments    = []

    @property
    def specialization(self): return self.__specialization
    @property
    def license_no(self):     return self.__license_no

    def see_patient(self, patient, diagnosis):
        """Examine patient and add to record"""
        if patient not in self._patients:
            self._patients.append(patient)
        patient.add_medical_record(diagnosis, self)
        print(f"  🩺 Dr.{self._name} examined {patient.name}: {diagnosis}")

    def prescribe(self, patient, medication, dosage):
        patient.add_prescription(medication, dosage, self)
        print(f"  💊 Prescribed {medication} ({dosage}) to {patient.name}")

    def get_role(self): return "DOCTOR"

    def get_info(self):
        print(f"\n  DOCTOR: Dr.{self._name} | {self.__specialization}")
        print(f"  License: {self.__license_no} | Dept: {self._department} | {self._experience}yr exp")
        print(f"  Patients seen: {len(self._patients)} | On duty: {self._is_on_duty}")


class Surgeon(Doctor):
    """Multilevel Level 3: Surgeon → Doctor → MedicalStaff → Person"""

    def __init__(self, name, age, gender, phone, department,
                 salary, experience_yrs, specialization, license_no, surgery_type):
        super().__init__(name, age, gender, phone, department,
                        salary, experience_yrs, specialization, license_no)
        self.__surgery_type     = surgery_type
        self.__surgeries_done   = 0

    @property
    def surgeries_done(self): return self.__surgeries_done

    def perform_surgery(self, patient, procedure):
        self.__surgeries_done += 1
        patient.add_medical_record(f"Surgery: {procedure}", self)
        print(f"  🔪 Surgeon Dr.{self.name} performed {procedure} on {patient.name}")
        print(f"     Total surgeries: {self.__surgeries_done}")

    def get_role(self): return "SURGEON"


class Nurse(MedicalStaff):
    """Hierarchical: Nurse → MedicalStaff → Person"""

    def __init__(self, name, age, gender, phone, department,
                 salary, experience_yrs, nurse_grade, ward_assigned):
        super().__init__(name, age, gender, phone, department, salary, experience_yrs)
        self._grade        = nurse_grade
        self._ward_assigned= ward_assigned

    def administer_medication(self, patient, medication):
        print(f"  💉 Nurse {self._name} administered {medication} to {patient.name}")

    def check_vitals(self, patient):
        print(f"  📊 Nurse {self._name} checked vitals of {patient.name}")

    def get_role(self): return "NURSE"
    def get_info(self):
        print(f"  NURSE: {self._name} | Grade: {self._grade} | Ward: {self._ward_assigned}")


class Ward:
    """Manages a hospital ward"""
    def __init__(self, name, ward_type, capacity):
        self.name     = name
        self.type     = ward_type
        self.capacity = capacity
        self._patients= []
        self._staff   = []

    def add_patient(self, patient):
        if len(self._patients) >= self.capacity:
            raise RuntimeError(f"Ward {self.name} is at full capacity")
        self._patients.append(patient)

    def remove_patient(self, patient):
        self._patients.remove(patient)

    def assign_staff(self, staff):
        self._staff.append(staff)

    @property
    def occupancy(self):
        return f"{len(self._patients)}/{self.capacity}"

    def __str__(self):
        return f"Ward[{self.name}] | Type: {self.type} | Occupancy: {self.occupancy}"


class Hospital:
    """Main hospital management — orchestrates all entities"""

    def __init__(self, name, address):
        self.name    = name
        self.address = address
        self._wards  = {}
        self._doctors= {}
        self._nurses = {}
        self._patients={}

    def add_ward(self, ward):
        self._wards[ward.name] = ward
        print(f"  ✅ Ward added: {ward}")

    def register_doctor(self, doctor):
        self._doctors[doctor.id] = doctor
        print(f"  ✅ Registered: {doctor}")

    def register_nurse(self, nurse):
        self._nurses[nurse.id] = nurse

    def register_patient(self, patient):
        self._patients[patient.id] = patient
        print(f"  ✅ Registered: {patient}")

    def get_ward(self, name): return self._wards.get(name)
    def get_doctor(self, id): return self._doctors.get(id)

    def print_summary(self):
        print(f"\n{'═'*60}")
        print(f"  🏥 {self.name}")
        print(f"  {self.address}")
        print(f"{'═'*60}")
        print(f"  Doctors:  {len(self._doctors)}")
        print(f"  Nurses:   {len(self._nurses)}")
        print(f"  Patients: {len(self._patients)}")
        print(f"  Wards:    {len(self._wards)}")
        for w in self._wards.values():
            print(f"    {w}")
        print(f"{'═'*60}")


if __name__ == "__main__":
    print("═"*60)
    print("  OOP Inheritance — Hospital Management System")
    print("  Project Lab India")
    print("═"*60)

    # Create hospital
    hospital = Hospital("Project Lab India Hospital", "Jaipur, Rajasthan")

    # Create wards
    icu   = Ward("ICU",     "Intensive Care",   10)
    general= Ward("General","General Medicine", 50)
    surgery= Ward("Surgery","Surgical",         20)

    for w in [icu, general, surgery]:
        hospital.add_ward(w)

    # Create doctors (multilevel inheritance chain)
    dr_sharma  = Doctor("Rajesh Sharma", 45, "M", "9876543210",
                        "Cardiology", 150000, 15, "Cardiologist", "MCI12345")
    dr_mehta   = Surgeon("Priya Mehta",  40, "F", "9876543211",
                         "Surgery", 200000, 12, "General Surgeon", "MCI12346", "Laparoscopic")
    dr_kumar   = Doctor("Anil Kumar",   35, "M", "9876543212",
                        "Neurology", 160000, 8,  "Neurologist", "MCI12347")

    # Create nurses
    nurse_geeta= Nurse("Geeta Singh", 28, "F", "9876543213",
                       "ICU", 45000, 3, "Grade-B", "ICU")

    # Register all
    for d in [dr_sharma, dr_mehta, dr_kumar]:
        hospital.register_doctor(d)
    hospital.register_nurse(nurse_geeta)

    # Create patients
    p1 = Patient("Arjun Kapoor", 55, "M", "9999999991", BloodGroup.O_POS)
    p2 = Patient("Sunita Devi",  42, "F", "9999999992", BloodGroup.A_NEG)

    hospital.register_patient(p1)
    hospital.register_patient(p2)

    # Medical operations
    print("\n── Medical Operations ──")
    dr_sharma.start_shift()
    dr_mehta.start_shift()

    p1.admit(icu, Severity.HIGH)
    p2.admit(general, Severity.MEDIUM)

    dr_sharma.see_patient(p1, "Hypertension - Stage 2")
    dr_sharma.prescribe(p1, "Amlodipine", "5mg once daily")

    dr_mehta.perform_surgery(p2, "Appendectomy")
    nurse_geeta.administer_medication(p1, "Amlodipine 5mg")
    nurse_geeta.check_vitals(p1)

    p1.get_info()
    dr_sharma.get_info()
    dr_mehta.get_info()
    hospital.print_summary()

    # Demonstrate inheritance chain
    print("\n── Inheritance Chain ──")
    print(f"  Surgeon MRO: {[c.__name__ for c in Surgeon.__mro__]}")
    print(f"  isinstance(dr_mehta, Doctor):      {isinstance(dr_mehta, Doctor)}")
    print(f"  isinstance(dr_mehta, MedicalStaff):{isinstance(dr_mehta, MedicalStaff)}")
    print(f"  isinstance(dr_mehta, Person):      {isinstance(dr_mehta, Person)}")
    print(f"  isinstance(nurse_geeta, Doctor):   {isinstance(nurse_geeta, Doctor)}")
