# Tests for Hospital Management
import sys; sys.path.insert(0,'..')
from main import Patient, Doctor, Surgeon, Nurse, Ward, BloodGroup, Severity

def make_doctor():
    return Doctor('Dr Test',35,'M','1234567890','Surgery',100000,5,'Surgeon','LIC001')

def make_patient():
    return Patient('Patient A',30,'M','9876543210',BloodGroup.A_POS)

def test_inheritance_chain():
    s = Surgeon('Dr S',40,'M','1234','Surgery',200000,10,'Gen Surgeon','L001','Lap')
    assert isinstance(s, Doctor)
    assert isinstance(s, Nurse) == False

def test_patient_admission():
    p = make_patient()
    w = Ward('ICU','Intensive',10)
    assert not p.is_admitted
    p.admit(w)
    assert p.is_admitted
    p.discharge()
    assert not p.is_admitted

def test_doctor_see_patient():
    d = make_doctor()
    p = make_patient()
    d.see_patient(p,'Hypertension')
    assert len(p._medical_history) == 1

def test_ward_capacity():
    import pytest
    w = Ward('Small','Test',1)
    p1 = make_patient(); p2 = Patient('B',25,'F','111',BloodGroup.B_POS)
    p1.admit(w)
    with pytest.raises(RuntimeError): p2.admit(w)
