# Inheritance Notes
## Types
- Single: Child → Parent
- Multilevel: C → B → A
- Hierarchical: B,C → A
- Multiple: Python supports, use MRO

## MRO (Method Resolution Order)
Python uses C3 linearization.
Surgeon.__mro__ = [Surgeon, Doctor, MedicalStaff, Person, ABC, object]

## super() Usage
super().__init__() calls parent constructor
Always call in child constructor to initialize parent state

## Abstract Classes
from abc import ABC, abstractmethod
Class with @abstractmethod cannot be instantiated.
Forces subclasses to implement the method.

## Interview Questions
1. Difference between single and multilevel inheritance?
2. What is MRO? How does Python resolve method calls?
3. What is super()? When should you use it?
4. What is an abstract class? Can you instantiate it?
5. What is the diamond problem? How does Python solve it?
